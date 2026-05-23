import os
from datetime import datetime, timedelta, timezone
from typing import Optional, Tuple
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from backend.models.user import User
from backend.models.auth import RefreshToken
from backend.schemas.user import UserCreate

# Configuration (In production, load these strictly via pydantic-settings)
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-super-secret-production-key-change-me")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

# Password Hashing Context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ==========================================
# 1. PASSWORD CRYPTOGRAPHY
# ==========================================

def get_password_hash(password: str) -> str:
    """Generates a secure secure hash from a plain text password."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain text password against its stored hash."""
    return pwd_context.verify(plain_password, hashed_password)


# ==========================================
# 2. TOKEN GENERATION & MANAGEMENT
# ==========================================

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Generates a short-lived JWT access token."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    
    to_encode.update({
        "exp": expire,
        "type": "access"
    })
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(db: Session, user_id: int) -> str:
    """
    Generates a secure, long-lived refresh token, stores its metadata 
    in the database for tracking/revocation, and returns the token string.
    """
    expires_delta = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    expires_at = datetime.now(timezone.utc) + expires_delta
    
    # Payload contains minimal data; the unique tracking string is tied to the DB record
    token_payload = {
        "sub": str(user_id),
        "exp": expires_at,
        "type": "refresh"
    }
    token_str = jwt.encode(token_payload, SECRET_KEY, algorithm=ALGORITHM)
    
    # Persist token tracking metadata to allow stateful revocation
    db_refresh_token = RefreshToken(
        token=token_str,
        user_id=user_id,
        expires_at=expires_at
    )
    db.add(db_refresh_token)
    db.commit()
    
    return token_str


# ==========================================
# 3. AUTHENTICATION, REFRESH & REVOCATION
# ==========================================

def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    """Authenticates a user against credentials. Returns User object if valid, else None."""
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


def rotate_refresh_token(db: Session, refresh_token_str: str) -> Tuple[str, str]:
    """
    Validates an existing refresh token, revokes it to prevent reuse (Token Rotation),
    and issues a brand new Access/Refresh token pair.
    """
    try:
        payload = jwt.decode(refresh_token_str, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "refresh":
            raise ValueError("Invalid token type")
        user_id = int(payload.get("sub"))
    except (JWTError, ValueError, TypeError):
        raise ValueError("Invalid or expired refresh token structure")

    # DB Lookup to verify state (ensure it hasn't been explicitly revoked or already rotated)
    db_token = db.query(RefreshToken).filter(
        RefreshToken.token == refresh_token_str,
        RefreshToken.revoked == False,
        RefreshToken.expires_at > datetime.now(timezone.utc)
    ).first()

    if not db_token:
        # Security Alert Trigger: Token reuse detected or explicitly revoked token being traded.
        # In a paranoid security environment, you'd revoke ALL active tokens for this user_id here.
        raise ValueError("Token is revoked, expired, or invalid")

    # 1. Revoke the used token (Enforce Refresh Token Rotation)
    db_token.revoked = True
    db.commit()

    # 2. Issue new pairs
    new_access_token = create_access_token(data={"sub": str(user_id)})
    new_refresh_token = create_refresh_token(db, user_id=user_id)

    return new_access_token, new_refresh_token


def revoke_refresh_token(db: Session, refresh_token_str: str) -> bool:
    """Explicitly revokes a single refresh token (typically used during Logout)."""
    db_token = db.query(RefreshToken).filter(RefreshToken.token == refresh_token_str).first()
    if db_token:
        db_token.revoked = True
        db.commit()
        return True
    return False


def revoke_all_user_tokens(db: Session, user_id: int) -> int:
    """Revokes every active token for a user. (Use during forced logouts or password resets)."""
    updated_count = db.query(RefreshToken).filter(
        RefreshToken.user_id == user_id, 
        RefreshToken.revoked == False
    ).update({RefreshToken.revoked: True}, synchronize_session=False)
    db.commit()
    return updated_count


# ==========================================
# 4. USER PROVISIONING
# ==========================================

def create_user(db: Session, user: UserCreate) -> User:
    """Creates a new user account with securely pre-hashed passwords."""
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user