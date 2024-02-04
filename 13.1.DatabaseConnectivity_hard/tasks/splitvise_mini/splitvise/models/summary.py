from sqlalchemy import Integer, Column, ForeignKey, Numeric

from .base import Base


class Summary(Base):  # type: ignore
    __tablename__ = 'summaries'

    summary_id = Column(Integer, primary_key=True)
    trip_id = Column(Integer, ForeignKey('trips.trip_id'))
    user_from_id = Column(Integer, ForeignKey('users.user_id'))
    user_to_id = Column(Integer, ForeignKey('users.user_id'))
    value = Column(Numeric)

    def __repr__(self) -> str:
        return (f'<Summary summary_id={self.summary_id}, trip_id={self.trip_id},'
                f'user_from_id={self.user_from_id}, user_to_id={self.user_to_id},'
                f'value={self.value}>')
