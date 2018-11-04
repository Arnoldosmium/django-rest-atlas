import yaml
from atlas.generator.serializer import ApiSerializer, FieldType


def test_field_type_parse():
    t1 = FieldType.parse("STRING")
    assert t1.value_type == "string" and not t1.optional and t1.collection_type is None
    t2 = FieldType.parse("optional<string>")
    assert t2.value_type == "string" and t2.optional and t2.collection_type is None
    t3 = FieldType.parse("map<string, integer>")
    assert t3.value_type == "integer" and t3.key_type == "string" and not t3.optional and t3.collection_type == "map"
    t4 = FieldType.parse("set<UUID>")
    assert t4.value_type == "uuid" and t4.key_type is None and not t4.optional and t4.collection_type == "set"

    def assert_parse_error(text):
        try:
            _ = FieldType.parse(text)
            raise Exception("Shall not pass!")
        except ValueError:
            pass

    for text in ["no_type", "n123<string>", "optional<integer,string>", "list<nothing>"]:
        assert_parse_error(text)


def test_api_serializer():
    obj = yaml.load("""\
title: TestGet
method: GET
path: /api/get
description: |
    description
params:
    id1:
        type: optional<Number>
        description: ID one.
    id2:
        type: object
        description: ID two.
        fields:
            id21:
                type: UUID
                description: ID2.1
returns:
    rtn1:
        type: string
        description: random return
    """)
    serialized = ApiSerializer(**obj)

    assert all(obj[k] == serialized.__getattribute__(k) for k in "title method path description".split())
    assert serialized.params['id2'].fields['id21'].type == "UUID"
    assert serialized.permission is None
    assert serialized.headers == serialized.errors == {}

