# vim: sw=4 ts=4 expandtab ai
#
# This file is part of Bender's Property
# Copyright (C) 2009 Bender's Property development team. All rights reserved.
#
from django.conf.urls.defaults import *

urlpatterns = patterns('bendersproperty.bp.views',
    (r'^$', 'index'),
    (r'^land_marketplace|property_marketplace|charts|leaderboard$', 'canvas'),
    (r'^summary$', 'summary'),
    (r'^friends$', 'friends'),
    (r'^invite$', 'invite'),
    (r'^help$', 'help'),
    (r'^set_trade$', 'set_trade'),
    (r'^dump$', 'dump'),
    (r'^post_remove$', 'post_remove'),
    (r'^post_auth$', 'post_auth'),
    # Define other pages you want to create here
)
