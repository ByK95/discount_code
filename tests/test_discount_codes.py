import json
from unittest import mock

from app.shared.user_datastore import user_datastore
from app.tests.test_base import BaseTestCase
from app.models.brand import Brand
from app.models.discount_code import DiscountCode
from app.models.user import User

from app.worker.tasks import generate_discount_codes


class AuthMixin(object):
    def authenticate(self):
        response = self.client.post(
            "/login?include_auth_token",
            json={"email": self.user.email, "password": self.user.password}
        )
        return response.json.get("response", {}).get("user", {}).get("authentication_token")

class DiscountCodeTestCase(AuthMixin, BaseTestCase):
    def setUp(self):
        super().setUp()
        self.user = user_datastore.create_user(
            email="test@me.com",
            name="test",
            surname="test",
            password="password"
        )
        self.user.save()
        self.brand = Brand(name="papple")
        self.brand.save()
        self.code = DiscountCode(code="m1macio", brand_id=self.brand.id)
        self.code.save()
        self.token = self.authenticate()

    def test_get_discount_code(self):
        response = self.client.post(
            "/api/discount_codes/",
            json={"brand_id": "1"}
        )
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.json["id"], self.code.id)
        self.assertEqual(response.json["code"], self.code.code)
        self.assertEqual(response.json["brand_id"], self.code.brand_id)

    def test_non_available_discount_code(self):
        response = self.client.post(
            "/api/discount_codes/",
            json={"brand_id": "2"}
        )
        
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json)

    def test_non_available_discount_code(self):
        response = self.client.post(
            "/api/discount_codes/",
            json={"brand_id": "2"}
        )
        
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json)

    @mock.patch("app.resources.discount_codes.celery")
    def test_discount_code_generation(self, mock_celery):
        mock_celery.send_task().id = 1

        response = self.client.post(
            "/api/discount_codes/generate",
            json={"brand_id": "1", "count": 10}
        )

        self.assertEqual(response.status_code, 200)
        
    def test_discount_code_generator_task(self):
        data = {'brand_id': 1, 'count': 1}

        generate_discount_codes(data=data)

        codes = DiscountCode.query.all()
        self.assertEqual(len(codes), 2)
        
    