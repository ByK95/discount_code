from flask import request, abort
from flask_restful import Resource
from sqlalchemy.orm import joinedload
from flask_restful import Resource, fields, marshal
from flask_restful import reqparse, abort, Api, Resource
from flasgger import swag_from
from marshmallow import ValidationError
from flask_security import auth_required, current_user

from app.shared.models import db
from app.shared.tasks import celery
from app.models.brand import Brand
from app.models.discount_code import DiscountCode
from app.resources.schemas import DiscountCodeSchema, DiscountCodeUserSchema


class DiscountCodeUserViewSet(Resource):
    schema = DiscountCodeUserSchema()

    @auth_required()
    @swag_from("docs/discount_user.yml")
    def post(self, *args, **kwargs):
        item_json = request.get_json()
        try:
            validated_data = self.schema.load(item_json)
        except ValidationError as err:
            return err.messages, 400
        
        code = DiscountCode.query.filter(
            DiscountCode.user == None,
            DiscountCode.brand_id == validated_data.get('brand_id')
        ).first()

        if not code:
            return {"error": "No code available for this brand"}, 400

        code.user_id = current_user.id
        code.save()
        return self.schema.dump(code)


class DiscountCodeGenerateViewSet(Resource):
    schema = DiscountCodeSchema()

    @auth_required()
    @swag_from("docs/discount_generate_codes.yml")
    def post(self, *args, **kwargs):
        item_json = request.get_json()
        try:
            validated_data = self.schema.load(item_json)
        except ValidationError as err:
            return err.messages, 400

        brand = Brand.query.filter(
            Brand.id == validated_data['brand_id'],
        ).first()
        if not brand:
            return {"error": "Brand not found"}, 400
        
        promise = celery.send_task(
            "tasks.generate_discount_codes",
            kwargs={"data": validated_data}
        )
        validated_data["promise"] = promise.id
        return validated_data, 200
