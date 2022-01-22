from app.shared.models import db
from app.models.mixins import ModelMixin


class DiscountCode(ModelMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(255), nullable=False)
    brand_id = db.Column(db.Integer, db.ForeignKey("brand.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    usable = db.Column(db.Boolean, default=True)
