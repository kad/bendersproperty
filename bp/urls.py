# vim: sw=4 ts=4 expandtab ai
#
# This file is part of Bender's Property
# Copyright (C) 2009 Bender's Property development team. All rights reserved.
#
from django.conf.urls.defaults import *

urlpatterns = patterns('bendersproperty.bp.views',
    (r'^$', 'index'),
    (r'^summary|land_marketplace|property_marketplace|charts|leaderboard$', 'canvas'),
    (r'^friends$', 'friends'),
    (r'^invite$', 'invite'),
    (r'^help$', 'help'),
    # Define other pages you want to create here
)
