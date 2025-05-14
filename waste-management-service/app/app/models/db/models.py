from sqlalchemy import TIMESTAMP, Column, Integer, String, BigInteger, DATETIME, UUID
from ...database import Base


class MissedWastePickups(Base):
    __tablename__ = "missed_waste_pickups"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    description = Column(String, index=False)
    date = Column(TIMESTAMP, index=True)
    address = Column(String, index=False)
    status = Column(Integer, index=False)
    userId = Column(BigInteger, index=True)
