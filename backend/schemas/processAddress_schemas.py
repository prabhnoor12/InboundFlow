from pydantic import BaseModel
from datetime import datetime

class ProcessAddressBase(BaseModel):
	user_id: int
	email_address: str
	is_active: bool = True

class ProcessAddressCreate(ProcessAddressBase):
	id: int

class ProcessAddressOut(ProcessAddressBase):
	id: int
	created_at: datetime

	class Config:
		orm_mode = True
