from app.shared.models import db
from app.models.user import User, Role
from flask_security import SQLAlchemyUserDatastore


user_datastore = SQLAlchemyUserDatastore(db, User, Role)
