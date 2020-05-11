"""
    smorest_sfs.modules.projects.models
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    项目的ORM模块
"""
from smorest_sfs.extensions.sqla import Model, SurrogatePK, db


class Project(Model, SurrogatePK):
    """
    项目

    :attr name: str(128) 项目名称
    """

    __tablename__ = "projects"

    name = db.Column(db.String(length=128), nullable=False, doc="项目名称")

    def __repr__(self) -> str:
        return self.name