"""
Provides generic filtering backends that can be used to filter the results
returned by list views.
"""
from __future__ import unicode_literals

from rest_framework.compat import guardian, get_model_name

from .BaseFilterBackend import BaseFilterBackend


class DjangoObjectPermissionsFilter(BaseFilterBackend):
    """
    A filter backend that limits results to those where the requesting user
    has read object level permissions.
    """
    def __init__(self):
        assert guardian, 'Using DjangoObjectPermissionsFilter, but django-guardian is not installed'

    perm_format = '%(app_label)s.view_%(model_name)s'

    def filter_queryset(self, request, queryset, view):
        user = request.user
        model_cls = queryset.model
        kwargs = {
            'app_label': model_cls._meta.app_label,
            'model_name': get_model_name(model_cls)
        }
        permission = self.perm_format % kwargs
        return guardian.shortcuts.get_objects_for_user(user, permission, queryset)