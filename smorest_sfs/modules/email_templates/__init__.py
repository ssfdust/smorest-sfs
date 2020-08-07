"""
    app.modules.email_templates
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    电子邮件模板模块

    电子邮件模板
"""

from typing import Dict

from flask_smorest import Blueprint

blp = Blueprint(
    "EmailTemplate", __name__, url_prefix="/email_templates", description="电子邮件模板模块"
)

ma_mapping: Dict[str, str] = dict(
    [
        (
            "smorest_sfs.modules.email_templates.models.EmailTemplate",
            "smorest_sfs.modules.email_templates.schemas.EmailTemplateSchema",
        )
    ]
)
