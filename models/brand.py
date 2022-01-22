from app.shared.models import db
from app.models.mixins import ModelMixin


class Brand(ModelMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    discount_codes = db.relationship("DiscountCode", backref="brand", lazy=True)
