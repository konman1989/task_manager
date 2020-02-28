from models import User


def test_get_user_from_db(init_database):
    user1 = User.query.get(12345)
    user2 = User.query.get(678910)

    assert user1.chat_id == 12345
    assert user2.chat_id == 678910
    assert user1.username == 'Constantine'
    assert user2.username == 'Steve'





