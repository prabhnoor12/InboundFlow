from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class InboundEmailBase(BaseModel):
	user_id: int
	from_address: str
	to_address: str
	subject: Optional[str] = None
	body_text: Optional[str] = None
	body_html: Optional[str] = None
	status: Optional[str] = "received"
	raw_headers: Optional[str] = None
	sanitized: Optional[bool] = False

class InboundEmailCreate(InboundEmailBase):
	pass

class InboundEmailOut(InboundEmailBase):
	id: int
	received_at: datetime
	created_at: datetime
	attachments: List['AttachmentOut'] = []

	class Config:
		orm_mode = True
