# Authentication Routes for FastAPI
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.schemas.user import UserCreate, UserOut
from backend.crud import auth_crud
from backend.utils.httpsHandler import HTTPSHandler

router = APIRouter(prefix="/auth", tags=["auth"])

# Dependency to enforce HTTPS
async def enforce_https(request: Request):
	await HTTPSHandler.enforce_https(request)

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED, dependencies=[Depends(enforce_https)])
def register(user: UserCreate, db: Session = Depends(get_db)):
	db_user = db.query(auth_crud.User).filter(auth_crud.User.username == user.username).first()
	if db_user:
		raise HTTPException(status_code=400, detail="Username already registered")
	return auth_crud.create_user(db, user)


@router.post("/login", status_code=200, dependencies=[Depends(enforce_https)])
def login(user: UserCreate, db: Session = Depends(get_db)):
	db_user = auth_crud.authenticate_user(db, user.username, user.password)
	if not db_user:
		raise HTTPException(status_code=401, detail="Invalid credentials")
	access_token = auth_crud.create_access_token({"sub": str(db_user.id)})
	refresh_token = auth_crud.create_refresh_token(db, user_id=db_user.id)
	return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.post("/refresh", status_code=200, dependencies=[Depends(enforce_https)])
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
	try:
		access_token, new_refresh_token = auth_crud.rotate_refresh_token(db, refresh_token)
		return {"access_token": access_token, "refresh_token": new_refresh_token, "token_type": "bearer"}
	except ValueError as e:
		raise HTTPException(status_code=401, detail=str(e))


@router.post("/logout", status_code=204, dependencies=[Depends(enforce_https)])
def logout(refresh_token: str, db: Session = Depends(get_db)):
	if not auth_crud.revoke_refresh_token(db, refresh_token):
		raise HTTPException(status_code=400, detail="Invalid refresh token or already revoked")
	return


@router.post("/logout_all", status_code=204, dependencies=[Depends(enforce_https)])
def logout_all(user_id: int, db: Session = Depends(get_db)):
	count = auth_crud.revoke_all_user_tokens(db, user_id)
	if count == 0:
		raise HTTPException(status_code=400, detail="No active tokens found for user")
	return
