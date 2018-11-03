"""
Defines all serializer for endpoint yaml definition files
"""

TYPE_CHOICES = (
    "int",
    "numeric",
    "boolean",
    "string",
    "datetime",
    "uuid",
)


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
    def __init__(self, method, path, title, description=None, permission=None,
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
