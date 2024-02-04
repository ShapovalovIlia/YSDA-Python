from sqlalchemy import Column, Integer, ForeignKey, Numeric

from .base import Base


class Expense(Base):  # type: ignore
    __tablename__ = 'expenses'

    expense_id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('events.event_id'))
    payer_id = Column(Integer, ForeignKey('users.user_id'))
    value = Column(Numeric)

    def __repr__(self) -> str:
        return (f'<Expense expense_id={self.expense_id}, event_id={self.event_id},'
                f'player_id={self.player_id}, value={self.value}>')
