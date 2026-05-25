from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AttachmentBase(BaseModel):
	email_id: int
	filename: str
	content_type: Optional[str] = None
	size: Optional[int] = None
	storage_url: Optional[str] = None

class AttachmentCreate(AttachmentBase):
	pass

class AttachmentOut(AttachmentBase):
	id: int
	uploaded_at: datetime

	class Config:
		orm_mode = True
