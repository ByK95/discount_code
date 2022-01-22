import unittest


from app.manage import app
from app.shared.models import db
from app.models.user import User


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.db = db
        self.client = app.test_client()
        self.app.config.update({
            "TESTING": True,
            "WTF_CSRF_ENABLED": True,
            "SECURITY_EMAIL_VALIDATOR_ARGS": {"check_deliverability": False},
            "SECURITY_PASSWORD_HASH": "plaintext",
            'WTF_CSRF_ENABLED': False
        })

        with app.app_context():
            db.session.close()
            db.drop_all()
            db.create_all()

    def run(self, result=None):
        with app.app_context():
            super().run(result=result)


if __name__ == "__main__":
    unittest.main()
