from app.shared.models import db
from app.models.mixins import ModelMixin
from flask_security.models import fsqla_v2 as fsqla


class User(ModelMixin, db.Model, fsqla.FsUserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    surname = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    discount_codes = db.relationship("DiscountCode", backref="user", lazy=True)

    def __repr__(self):
        return "<User %r>" % self.name


class Role(db.Model, fsqla.FsRoleMixin):
    pass
