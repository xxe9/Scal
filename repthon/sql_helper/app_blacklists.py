from sqlalchemy import Column, String, UnicodeText

from . import BASE, SESSION


class App_BlackList(BASE):
    __tablename__ = "app_blacklist"
    chat_id = Column(String(14), primary_key=True)
    first_name = Column(UnicodeText)
    username = Column(UnicodeText)
    reason = Column(UnicodeText)
    date = Column(UnicodeText)

    def __init__(self, chat_id, first_name, username, reason, date):
        self.chat_id = str(chat_id)
        self.username = username
        self.reason = reason
        self.date = date
        self.first_name = first_name

    def __repr__(self):
        return "<BL %s>" % self.chat_id


App_BlackList.__table__.create(bind=SESSION.get_bind(), checkfirst=True)


def add_user_to_bl(
    chat_id: int, first_name: str, username: str, reason: str, date: str
):
    """add the user to the blacklist"""
    to_check = check_is_black_list(chat_id)
    if not to_check:
        __user = App_BlackList(str(chat_id), first_name, username, reason, date)
        SESSION.add(__user)
        SESSION.commit()
    rem = SESSION.query(App_BlackList).get(str(chat_id))
    SESSION.delete(rem)
    SESSION.commit()
    user = App_BlackList(str(chat_id), first_name, username, reason, date)
    SESSION.add(user)
    SESSION.commit()
    return True


def check_is_black_list(chat_id: int):
    """check if user_id is blacklisted"""
    try:
        return SESSION.query(App_BlackList).get(str(chat_id))
    finally:
        SESSION.close()


def rem_user_from_bl(chat_id: int):
    """remove the user from the blacklist"""
    if s__ := SESSION.query(App_BlackList).get(str(chat_id)):
        SESSION.delete(s__)
        SESSION.commit()
        return True
    SESSION.close()
    return False


def get_all_bl_users():
    try:
        return SESSION.query(App_BlackList).all()
    except BaseException:
        return None
    finally:
        SESSION.close()
