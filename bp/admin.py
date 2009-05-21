# vim: sw=4 ts=4 expandtab ai
#
# This file is part of Bender's Property
# Copyright (C) 2009 Bender's Property development team. All rights reserved.
#
from django.contrib import admin

from models import FBUser, Trade, LandRegion, PropertyType, PropertyKind
for cls in (FBUser, Trade, LandRegion, PropertyType, PropertyKind):
    admin.site.register(cls)

