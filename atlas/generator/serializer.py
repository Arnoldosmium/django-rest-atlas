"""
Defines all serializer for endpoint yaml definition files
"""
import re

TYPE_CHOICES = {
    "int",
    "integer",
    "numeric",
    "double",
    "boolean",
    "string",
    "date",
    "datetime",
    "timestamp",
    "uuid",
}

TYPE_DECORATOR = {
    "optional",
    "list",
    "map",
    "set",
}


class FieldType:
    _RE_COMPLEX_TYPE = re.compile("^([a-z]+?)<([a-z, ]+)>$")

    def __init__(self, value_type, optional=False, key_type=None, collection_type=None):
        self.value_type = value_type
        self.optional = optional and key_type is None and collection_type is None
        self.key_type = key_type
        self.collection_type = collection_type

    @staticmethod
    def parse(text):
        text = text.lower()
        if text in TYPE_CHOICES:
            return FieldType(text)

        if "<" in text and ">" in text:
            m = FieldType._RE_COMPLEX_TYPE.match(text)
            if not m:
                raise ValueError("'%s' is not a valid type expression" % text)

            decorator = m.group(1)
            value_type = m.group(2)

            if decorator not in TYPE_DECORATOR:
                raise ValueError("'%s' is not a valid type decorator, valid options are %s"
                                 % (decorator, TYPE_DECORATOR))

            if decorator == "map":
                value_types = [s.strip() for s in value_type.split(",")]
                if len(value_types) != 2:
                    raise ValueError("'%s' is not a valid key-value type expression" % value_type)
                key_type, value_type = value_types
                if key_type not in TYPE_CHOICES or value_type not in TYPE_CHOICES:
                    raise ValueError("%s contains invalid value type" % value_types)
                return FieldType(key_type=key_type, value_type=value_type, collection_type=decorator)

            if value_type not in TYPE_CHOICES:
                raise ValueError("'%s' is not a valid type" % value_type)

            if decorator == "optional":
                return FieldType(value_type, optional=True)

            return FieldType(value_type, collection_type=decorator)

        raise ValueError("'%s' is not a valid type expression" % text)


class BaseSerializer:
    def require_not_null(self, value, field_name=""):
        assert value is not None, "Field {} of {} cannot be null".format(field_name, self.__class__.__name__)
        return value

    def require_of_type(self, value, type, field_name=""):
        if value is None:
            return value
        assert isinstance(value, type), "Field {} of {} has to be {} type".format(
            field_name, self.__class__.__name__, type.__class__.__name__)
        return value

    def validate(self):
        return True


class BaseApiField(BaseSerializer):
    def __init__(self, type, group=None, description=None, fields=None):
        self.group = group
        self.type = self.require_not_null(type, "type")  # allow more complex structure like optional<string>
        self.description = description
        self.fields = {key: self.__class__(**field) for key, field in fields.items()} if fields else {}

    @property
    def parsed_type(self):
        return FieldType.parse(self.type)


class ApiHeaderField(BaseApiField):
    def __init__(self, type, group=None, description=None, fields=None, default=None):
        super().__init__(type, group, description, fields)
        self.default = default


class ApiParamsField(BaseApiField):
    def __init__(self, type, group=None, description=None, fields=None, restrictToValues=None, default=None):
        super().__init__(type, group, description, fields)
        self.default = default
        self.restrictToValues = self.require_of_type(restrictToValues, list, "restrictToValues") or []


class ApiErrorsField(BaseApiField):
    pass


class ApiSuccessField(BaseApiField):
    pass


class ApiSerializer(BaseSerializer):
    def __init__(self, title, path, method, description=None, permission=None,
                 headers=None, params=None, returns=None, errors=None):
        self.method = self.require_not_null(method, "method")
        self.path = self.require_not_null(path, "path")
        self.title = self.require_not_null(title, "title")
        self.description = description
        self.permission = permission
        self.headers = {key: ApiHeaderField(**field) for key, field in headers.items()} if headers else {}
        self.params = {key: ApiParamsField(**field) for key, field in params.items()} if params else {}
        self.returns = {key: ApiSuccessField(**field) for key, field in returns.items()} if returns else {}
        self.errors = {key: ApiErrorsField(**field) for key, field in errors.items()} if errors else {}

    @staticmethod
    def load_apis(apis):
        return {key: ApiSerializer(title=field.get("title", key), **field) for key, field in apis.items()}
