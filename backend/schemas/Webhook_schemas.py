from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum

class WebhookStatus(str, Enum):
	pending = "pending"
	success = "success"
	failed = "failed"

class WebhookDeliveryBase(BaseModel):
	email_id: int
	target_url: str
	status: WebhookStatus = WebhookStatus.pending
	attempt_count: int = 0
	last_attempt_at: Optional[datetime] = None
	next_attempt_at: Optional[datetime] = None
	response_code: Optional[int] = None
	response_body: Optional[str] = None

class WebhookDeliveryCreate(WebhookDeliveryBase):
	pass

class WebhookDeliveryOut(WebhookDeliveryBase):
	id: int
	created_at: datetime

	class Config:
		orm_mode = True
