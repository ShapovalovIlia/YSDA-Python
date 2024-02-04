from sqlalchemy import Integer, Column, ForeignKey, DateTime, Boolean, String

from .base import Base


class Event(Base):  # type: ignore
    __tablename__ = 'events'

    event_id = Column(Integer, primary_key=True)
    trip_id = Column(Integer, ForeignKey('trips.trip_id'))
    title = Column(String)
    happened_datetime = Column(DateTime)
    settled_up = Column(Boolean)

    def __repr__(self) -> str:
        return (f'<Event event_id={self.event_id}, trip_id={self.trip_id}, title={self.title},'
                f'happened_datetime={self.happened_datetime}>')
