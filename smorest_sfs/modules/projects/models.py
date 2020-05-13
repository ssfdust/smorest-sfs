"""
    smorest_sfs.modules.projects.models
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    项目的ORM模块
"""
from smorest_sfs.extensions.marshal import not_empty
from smorest_sfs.extensions.sqla import Model, SurrogatePK, db


class Project(Model, SurrogatePK):
    """
    项目

    Attribute:
        name (str): 项目名称，禁止非空，非值，最大长度128
    """

    __tablename__ = "projects"

    name = db.Column(
        db.String(length=128),
        nullable=False,
        doc="项目名称",
        info={"marshmallow": {"validate": [not_empty]}},
    )

    def __repr__(self) -> str:
        return self.name
