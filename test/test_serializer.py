import yaml
from atlas.generator.serializer import ApiSerializer


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

