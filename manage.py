import os
from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from flasgger import Swagger
from flask_security.models import fsqla_v2 as fsqla
from flask_security import Security, SQLAlchemyUserDatastore, hash_password

from app.shared.models import db
from app.shared.user_datastore import user_datastore
from app.models.brand import Brand
from app.models.discount_code import DiscountCode
from app.models.user import User, Role

from app.resources.discount_codes import DiscountCodeUserViewSet, DiscountCodeGenerateViewSet


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", 'pf9Wkove4IKEAXvy-cQkeDPhv9Cb3Ag-wyJILbq_dFw')
app.config['SECURITY_PASSWORD_SALT'] = os.environ.get("SECURITY_PASSWORD_SALT", '146585145368132386173505678016728509634')
app.config['WTF_CSRF_ENABLED'] = False
api = Api(app)
db.init_app(app)
security = Security(app, user_datastore)
migrate = Migrate(app, db)
swagger = Swagger(app)


@app.before_first_request
def create_user():
    if not user_datastore.find_user(email="test@me.com"):
        user_datastore.create_user(
            email="test@me.com",
            name="test",
            surname="test",
            password=hash_password("password"))
    db.session.commit()


api.add_resource(DiscountCodeUserViewSet, "/api/discount_codes/")
api.add_resource(DiscountCodeGenerateViewSet, "/api/discount_codes/generate")


if __name__ == "__main__":
    app.run(debug=True)
