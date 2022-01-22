# -*- coding: utf-8 -*-
import sys

sys.path.append("/")

from app.shared.models import db
from app.models.brand import Brand
from app.models.discount_code import DiscountCode
from app.models.user import User
from app.manage import app


def seed():
    a = User(name="user", surname="test", email="a@a.com")
    a.save()
    brand = Brand(name="papple")
    brand.save()
    code = DiscountCode(code="m1macio", brand_id=brand.id)
    code.save()



def truncate_all():
    models = [DiscountCode, Brand, User]
    for model in models:
        db.session.query(model).delete()
        db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        truncate_all()
        seed()
