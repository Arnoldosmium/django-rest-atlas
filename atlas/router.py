"""
:author Arnold Lin
Router solution for class-based views
"""
from django.urls import re_path


class PathModule(object):
    def __init__(self):
        self.urlpatterns = list()

    def route(self, url_path, **kwargs):
        """
        Decorator: Add a class-based view
        :param url_path: regex path for this view
        :param kwargs: extra args pass to re_path
        :return: original class-based view
        """
        pattern = self.urlpatterns
        def _decorator(obj_class):
            pattern.append(
                re_path(
                    url_path,
                    obj_class.as_view(),
                    **kwargs
                )
            )
            return obj_class
        return _decorator

    def get_urlpatterns(self):
        """
        Returns all collected routes
        :return: all collected routes
        """
        return list(self.urlpatterns)
