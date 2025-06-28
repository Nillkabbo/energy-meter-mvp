from sqlalchemy import Column, String, Text, Integer, BigInteger, DateTime
from sqlalchemy.sql import func
from database import Base
import uuid

class Job(Base):
    __tablename__ = 'jobs'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    smart_meter_id = Column(String, nullable=False)
    start_datetime = Column(String, nullable=False)
    end_datetime = Column(String, nullable=False)
    status = Column(String, nullable=False, default='pending')
    created_at = Column(DateTime, server_default=func.current_timestamp())
    updated_at = Column(DateTime, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    file_path = Column(String)
    error_message = Column(Text)
    record_count = Column(Integer)
    file_size_bytes = Column(BigInteger) 