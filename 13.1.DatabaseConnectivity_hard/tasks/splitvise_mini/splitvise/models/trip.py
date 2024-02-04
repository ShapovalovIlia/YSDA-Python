from sqlalchemy import Column, Integer, String, DateTime, Table, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base

UserTrip = Table(
    'users_trips', Base.metadata,
    Column('user_id', ForeignKey('users.user_id'), primary_key=True),
    Column('trip_id', ForeignKey('trips.trip_id'), primary_key=True)
)


class Trip(Base):  # type: ignore
    __tablename__ = 'trips'

    trip_id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    created_timestamp = Column(DateTime)

    users = relationship('User', secondary=UserTrip, back_populates='trips')

    def __repr__(self) -> str:
        return (f'<Trip trip_id={self.trip_id}, title={self.title}, description={self.description},'
                f'created_timestamp={self.created_timestamp}>')
