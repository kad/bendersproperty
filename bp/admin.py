# vim: sw=4 ts=4 expandtab ai
#
# This file is part of Bender's Property
# Copyright (C) 2009 Bender's Property development team. All rights reserved.
#
from django.contrib import admin

from models import FBUser, Trade, LandRegion, PropertyType, PropertyKind
for cls in (Trade, LandRegion, PropertyType):
    admin.site.register(cls)

class FBUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'cash', 'value', 'rent', 'hour_rate', 'max_cash', 'max_value')
    ordering = ('-value', '-cash', '-rent', 'id', )

class PropertyKindAdmin(admin.ModelAdmin):
    list_display = ('name', 'size', 'region', 'type', 'value', 'cost', 'rent', 'require_builder', 'require_plumber', 'require_electrician', 'require_plasterer', 'require_decorator')
    ordering = ('size', '-value', '-rent', '-cost', )

admin.site.register(FBUser, FBUserAdmin)
admin.site.register(PropertyKind, PropertyKindAdmin)
