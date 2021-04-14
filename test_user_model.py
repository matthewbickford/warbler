"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ["DATABASE_URL"] = "postgresql:///warbler_test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data


db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        u1 = User.signup("test1", "email1@email.com", "password", None)
        uid1 = 1111
        u1.id = uid1

        u2 = User.signup("test2", "email2@email.com", "password", None)
        uid2 = 2222
        u2.id = uid2

        db.session.commit()

        u1 = User.query.get(uid1)
        u2 = User.query.get(uid2)

        self.u1 = u1
        self.uid1 = uid1

        self.u2 = u2
        self.uid2 = uid2

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_user_model(self):
        """Does basic model work?"""

        user1 = User(
            email="test@test.com", username="testuser", password="HASHED_PASSWORD"
        )

        db.session.add(user1)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(user1.messages), 0)
        self.assertEqual(len(user1.followers), 0)

    def test_repr(self):
        """Does the repr method work as expected?"""

        user1 = User(
            email="test@test.com", username="testuser", password="HASHED_PASSWORD"
        )

        db.session.add(user1)
        db.session.commit()

        # User repr should match
        self.assertEqual(
            repr(user1), f"<User #{user1.id}: {user1.username}, {user1.email}>"
        )

    def test_is_following(self):
        """Does method successfully detect follows"""

        self.u1.following.append(self.u2)
        db.session.commit()

        self.assertTrue(self.u1.is_following(self.u2))
        self.assertFalse(self.u2.is_following(self.u1))

    def test_is_followed_by(self):
        """Does is_followed_by work as expected?"""

        self.u2.following.append(self.u1)
        db.session.commit()

        self.assertTrue(self.u1.is_followed_by(self.u2))
        self.assertFalse(self.u2.is_followed_by(self.u1))

    def test_signup_user(self):
        """Does User.create successfully create new user when given valid credentials?"""

        new_user = User.signup("new_user", "testemail@email.com", "password", None)
        uid = 666
        new_user.id = uid

        db.session.commit(uid)

        self.assertTrue(new_user)

        u_test = User.query.get(uid)
        self.assertIsNotNone(u_test)
        self.assertEqual(u_test.username, "new_user")
        self.assertEqual(u_test.email, "testemail@email.com")
        self.assertNotEqual(u_test.password, "password")


def test_invalid_username(self):
    bad_user = User.signup(None, "testemail.@email.com", "password", None):
    uid = 89989898
    invalid.id = uid
    with self.assertRaises(exc.IntegrityError) as context:
        db.session.commit()


def test_invalid_email(self):
    bad_user = User.signup("test", None, "password", None):
    uid = 89989898
    invalid.id = uid
    with self.assertRaises(exc.IntegrityError) as context:
        db.session.commit()


def test_valid_authentication(self):
    u = User.authenticate(self.u1.username, "password")
    self.assertIsNotNone(u)
    self.assertEqual(u.id, self.uid1)


def test_invalid_username(self):
    self.assertFalse(User.authenticate("badusername", "password"))


def test_wrong_password(self):
    self.assertFalse(User.authenticate(self.u1.username, "badpassword"))