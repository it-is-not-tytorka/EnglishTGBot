from sqlalchemy import Integer, String, Boolean, Date, ARRAY, Tuple
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class User(Base):
    """
    A model which represents a user in a database.

    Contains his id, names and scores.
    cur_scores is a count of scores which allow to spend on hits by command /spend.
    spent_scores is a count of scores which already was spent on hits by command /spend.
    """
    __tablename__ = "users"
    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String)
    first_name: Mapped[str] = mapped_column(String, nullable=True)
    last_name: Mapped[str] = mapped_column(String, nullable=True)
    pref_order: Mapped[str] = mapped_column(String, default='decr')  # decreasing or increasing order of words
    current_state: Mapped[str] = mapped_column(String, default='start')
    # TODO I want user to keep his current word list but there's problem to have an array so i need to found out solution
    # current_word_list: Mapped[list] = mapped_column(ARRAY(String, as_tuple=True), server_default="{}")
    current_page: Mapped[int] = mapped_column(Integer, default=0)


class UserManager:
    """
    This class manage operations with users.
    Add a user to a database, check his presence to a database, get and change user's attributes.
    """

    def __init__(self, db_engine, db_session) -> None:
        self.db_engine = db_engine
        self.db_session = db_session

    def add_user(
        self,
        user_id: int,
        username: str,
        first_name: str,
        last_name: str,
        pref_order: str = 'decr',
        current_state: str = 'start',
    ) -> None:
        user = User(
            user_id=user_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
            pref_order=pref_order,
            current_state=current_state,
        )
        self.db_session.add(user)
        self.db_session.commit()

    def get_user(self, user_id: int):
        user = (
            self.db_session.execute(
                self.db_session.query(User).where(User.user_id == user_id)
            )
            .scalars()
            .all()
        )
        return False if len(user) == 0 else user[0]

    @staticmethod
    def set_state(user: User, state: str):
        setattr(user, 'current_state', state)

    @staticmethod
    def get_state(user: User):
        return getattr(user, 'current_state', None)

    @staticmethod
    def set_word_list(user: User, word_list: list):
        setattr(user, 'current_word_list', word_list)

    @staticmethod
    def get_page(user: User):
        return getattr(user, 'current_page', 0)

    def increase_page(self, user: User):
        # TODO i want to do function that allow user go from the last page to the first if he increases page staying on the last one
        # because now there will be an error if user increases page staying on the last
        return setattr(user, 'current_page', self.get_page(user) + 1)

    @staticmethod
    def get_word_list(user: User):
        return getattr(user, 'current_word_list', [])