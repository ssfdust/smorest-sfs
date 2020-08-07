"""测试Schema用例"""
from marshmallow import Schema, fields


class GrandChildSchema(Schema):

    name_3 = fields.Str()


class ChildSchema(Schema):

    name_2 = fields.Str()
    code_2 = fields.Str()

    grand_children = fields.List(fields.Nested(GrandChildSchema))


class ParentSchema(Schema):

    name = fields.Str()
    code = fields.Str()

    children = fields.List(fields.Nested(ChildSchema))


class NameOnlySchema(Schema):

    name = fields.Str()
