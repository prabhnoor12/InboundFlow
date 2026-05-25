from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum

class RetryStatus(str, Enum):
	pending = "pending"
	success = "success"
	failed = "failed"

class RetryQueueBase(BaseModel):
	webhook_delivery_id: int
	scheduled_for: datetime
	retry_count: int = 0
	status: RetryStatus = RetryStatus.pending

class RetryQueueCreate(RetryQueueBase):
	pass

class RetryQueueOut(RetryQueueBase):
	id: int
	created_at: datetime

	class Config:
		orm_mode = True
