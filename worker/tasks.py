import sys
sys.path.append('/')

import time
import os
from celery import Celery
from celery.utils.log import get_task_logger

from app.models.discount_code import DiscountCode
from app.manage import app as web_app
from app.worker.utils import generate_code


logger = get_task_logger(__name__)

app = Celery("tasks", broker=os.environ["CELERY_BROKER_URL"], backend="rpc://")


@app.task()
def generate_discount_codes(data):
    logger.info("Generating codes - Starting work ", data)
    count = data.get('count', 0)
    brand_id = data['brand_id']
    with web_app.app_context():
        for i in range(count):
            code = DiscountCode(code=generate_code(6), brand_id=brand_id)
            code.save()
