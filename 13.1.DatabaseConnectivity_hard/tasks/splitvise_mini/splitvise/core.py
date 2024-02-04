import typing as tp
from decimal import Decimal
from datetime import datetime

from .models.base import Session
from .models import User, Expense, Trip, Debt, Event, Summary
from .exceptions import SplitViseException

MoneyType = Decimal


#
def create_user(
        username: str,
        *,
        session: Session
) -> User:
    """
    Create new User; validate user exists
    :param username: username to create
    :param session: active session to perform operations with
    :return: orm User object
    :exception: username already taken
    """
    if session.query(User).filter_by(username=username).first():
        raise SplitViseException('Username already taken')
    user = User(username=username)
    session.add(user)
    session.commit()

    return user


def create_event(
        trip_id: int,
        people_debt: tp.Mapping[int, MoneyType],
        people_payment: tp.Mapping[int, MoneyType],
        title: str,
        *,
        session: Session
) -> Event:
    """
    Create Event in database, automatically creates Debts and Expenses; validates sum
    :param trip_id: Trip.trip_id from the database
    :param people_debt: mapping of User.user_id to theirs debt in that event
    :param people_payment: mapping of User.user_id to theirs payments in that event
    :param title: title of the event
    :param session: active session to perform operations with
    :return: orm Event object
    :exception: Trip not found by id, Can not create debt for user not in trip,
                Can not create payment for user not in trip, Sum of debts and sum of payments are not equal
    """
    trip = session.query(Trip).filter_by(trip_id=trip_id).first()
    if not trip:
        raise SplitViseException('Trip not found by id')
    trip_user_ids = set()

    for user in trip.users:
        trip_user_ids.add(user.user_id)
    for user_id in people_debt.keys():
        if user_id not in trip_user_ids:
            raise SplitViseException('Can not create debt for user not in trip')
    for user_id in people_payment.keys():
        if user_id not in trip_user_ids:
            raise SplitViseException('Can not create payment for user not in trip')

    sum_of_debts = MoneyType(0)
    sum_of_payments = MoneyType(0)

    for user_id, val in people_payment.items():
        sum_of_payments += val
    for user_id, val in people_debt.items():
        sum_of_debts += val
    if sum_of_debts != sum_of_payments:
        raise SplitViseException('Sum of debts and sum of payments are not equal')
    event = Event(
        trip_id=trip_id,
        title=title,
        happened_datetime=datetime.now()
    )
    session.add(event)
    session.commit()
    for user_id, val in people_payment.items():
        session.add(Expense(event_id=event.event_id, payer_id=user_id, value=val))
    for user_id, val in people_debt.items():
        session.add(Debt(event_id=event.event_id, debtor_id=user_id, value=val))
    session.commit()

    return event


def create_trip(
        creator_id: int,
        title: str,
        description: str,
        *,
        session: Session
) -> Trip:
    """
    Create Trip. Automatically add creator to the trip. Validate input: the title should not be empty and the creator
    should exist in the users table
    :param creator_id: User.user_id from the database to create trip by
    :param title: Title of the trip
    :param description: Long (or not so long) description of the trip
    :param session: active session to perform operations with
    :return: orm Trip object
    :exception: Title of a trip should not be empty, User not found by id
    """
    if not title:
        raise SplitViseException('Title of a trip should not be empty')
    creator = session.query(User).filter_by(user_id=creator_id).first()

    if not creator:
        raise SplitViseException('User not found by id')

    trip = Trip(title=title, description=description, users=[creator], created_timestamp=datetime.now())
    session.add(trip)
    session.commit()
    return trip


def add_user_to_trip(
        guest_id: int,
        trip_id: int,
        *,
        session: Session
) -> None:
    """
    Mark that the user with guest_id takes part in the trip. Check that the user and the trip do exist and the user has
    not been added to the trip yet.
    :param guest_id: User.user_id from the database to add to the trip
    :param trip_id: Trip.trip_id from the database
    :param session: active session to perform operations with
    :return: None
    :exception: Trip not found by id, User already in trip
    """
    user = session.query(User).filter_by(user_id=guest_id).first()
    trip = session.query(Trip).filter_by(trip_id=trip_id).first()
    if not user:
        raise SplitViseException('User not found by id')
    if not trip:
        raise SplitViseException('Trip not found by id')
    if user in trip.users:
        raise SplitViseException('User already in trip')
    trip.users.append(user)
    session.commit()


def get_trip_users(
        trip_id: int,
        *,
        session: Session
) -> list[User]:
    """
    Get Users from Trip; validate Trip exists
    :param trip_id: Trip.trip_id from the database
    :param session: active session to perform operations with
    :return: list of orm User objects
    :exception: Trip not found by id
    """
    trip = session.query(Trip).filter_by(trip_id=trip_id).first()
    if not trip:
        raise SplitViseException('Trip not found by id')

    return trip.users


def make_summary(
        trip_id: int,
        *,
        session: Session
) -> None:
    """
    Make trip summary. Mark all the events of the trip as settled up. Validate at least the existence of the trip
    being calculated
    :param trip_id: Trip.trip_id from the database
    :param session: active session to perform operations with
    :return: None
    :exception: Trip not found by id
    """
    trip = session.query(Trip).filter_by(trip_id=trip_id).first()
    if not trip:
        raise SplitViseException('Trip not found by id')

    total: dict[int, MoneyType] = {}
    events = session.query(Event).filter_by(trip_id=trip_id).all()
    for event in events:
        event.settled_up = True
        expenses = session.query(Expense).filter_by(event_id=event.event_id).all()
        for exp in expenses:
            total[exp.payer_id] = total.get(exp.payer_id, MoneyType(0)) + MoneyType(exp.value)

    for event in events:
        debts = session.query(Debt).filter_by(event_id=event.event_id).all()
        for debt in debts:
            total[debt.debtor_id] = total.get(debt.debtor_id, MoneyType(0)) - MoneyType(debt.value)

    diffs: list[list[int | MoneyType]] = []
    for user_id, value in total.items():
        diffs.append([value, user_id])
    diffs.sort()
    right_pointer = len(diffs) - 1
    for left_pointer in range(0, len(diffs)):
        if left_pointer >= right_pointer:
            break

        while diffs[left_pointer][0] < MoneyType(0):
            add = min(-diffs[left_pointer][0], diffs[right_pointer][0])
            diffs[left_pointer][0] += add
            diffs[right_pointer][0] -= add
            session.add(Summary(trip_id=trip_id, user_from_id=diffs[right_pointer][1],
                                user_to_id=diffs[left_pointer][1], value=add))
            if diffs[right_pointer][0] == MoneyType(0):
                right_pointer -= 1

    session.commit()
