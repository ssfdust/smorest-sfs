"""
    smorest_sfs.extensions.sqla.db
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    db实例模块
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(model_class=object)
