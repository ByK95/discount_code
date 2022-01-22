from flask_sqlalchemy import SQLAlchemy
from flask_security.models import fsqla_v2 as fsqla

db = SQLAlchemy()
fsqla.FsModels.set_db_info(db)
