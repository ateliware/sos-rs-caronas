from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group

from apps.core.models import CustomGroup

admin.site.unregister(Group)
admin.site.register(CustomGroup, GroupAdmin)
