# vim: sw=4 ts=4 expandtab ai
#
# This file is part of Bender's Property
# Copyright (C) 2009 Bender's Property development team. All rights reserved.
#
from django.db import models

# get_facebook_client lets us get the current Facebook object
# from outside of a view, which lets us have cleaner code
from facebook.djangofb import get_facebook_client

from django.db.models.fields import PositiveIntegerField
from django.conf import settings

from datetime import datetime

class BigPositiveIntegerField(PositiveIntegerField):
    empty_strings_allowed=False
    def get_internal_type(self):
        return "BigPositiveIntegerField"

    def db_type(self):
        if  settings.DATABASE_ENGINE == 'oracle':
            return 'NUMBER(19) UNSIGNED'
        else:
            return 'bigint unsigned'

class FBUserManager(models.Manager):
    """Custom manager for a Facebook User."""

    def get_current(self):
        """Gets a FBUser object for the logged-in Facebook user."""
        facebook = get_facebook_client()
        user, created = self.get_or_create(id=int(facebook.uid))
        if created:
            # we could do some custom actions for new users here...
            pass
        return user

class Trade(models.Model):
    """ Trades (Builder/Plumber/Electrican/Plasterer/Decorator) """
    name = models.CharField(blank=False, unique=True, max_length=32)

    def __unicode__(self):
        return self.name

class FBUser(models.Model):
    """A simple User model for Facebook users."""
    # Add the custom manager
    objects = FBUserManager()

    # We use the user's UID as the primary key in our database.
    id = BigPositiveIntegerField(primary_key=True)
    # Timestamp when user added application
    app_added = models.DateTimeField(default=datetime.now)
    # User's cash
    cash = BigPositiveIntegerField(default=35000)
    value = BigPositiveIntegerField(default=0)
    # Last time when user collected rent
    last_rent_collected = models.DateTimeField(default=datetime.now)

    trade = models.ForeignKey(Trade, null=True, blank=True, default=None)
    hour_rate = models.IntegerField(default=0)
    hours = models.FloatField(default=6)
    reserved_hours = models.IntegerField(default=0)
    last_reset = models.DateTimeField(default=datetime.now)

    # Collected expirience
    exp_builder = models.IntegerField(default=0)
    exp_plumber = models.IntegerField(default=0)
    exp_electrician = models.IntegerField(default=0)
    exp_plasterer = models.IntegerField(default=0)
    exp_decorator = models.IntegerField(default=0)

    max_cache = BigPositiveIntegerField(default=35000)
    max_value = BigPositiveIntegerField(default=0)

    def __unicode__(self):
        return u'%d' % self.id

class LandRegion(models.Model):
    """ Land region Downtown/Suburbs/Beachfront/Countryside/Desert/Industrial """
    name = models.CharField(blank=False, unique=True, max_length=32)

    def __unicode__(self):
        return self.name

class PropertyType(models.Model):
    """ Property type: rental/tourist/commercial """
    name = models.CharField(blank=False, unique=True, max_length=32)

    def __unicode__(self):
        return self.name

class PropertyKind(models.Model):
    """ What kind of property do we have """
    name = models.CharField(blank=False, unique=True, max_length=64)
    size = models.IntegerField(default=0, blank=False, null=False)
    region = models.ForeignKey(LandRegion, blank=False, null=False)
    type = models.ForeignKey(PropertyType, blank=False, null=False)
    cost = models.IntegerField(default=0, blank=False, null=False)
    rent = models.IntegerField(default=0, blank=False, null=False)
    value = models.IntegerField(default=0, blank=False, null=False)

    require_builder = models.IntegerField(default=0, blank=False, null=False)
    require_plumber = models.IntegerField(default=0, blank=False, null=False)
    require_electrician = models.IntegerField(default=0, blank=False, null=False)
    require_plasterer = models.IntegerField(default=0, blank=False, null=False)
    require_decorator = models.IntegerField(default=0, blank=False, null=False)

    def __unicode__(self):
        return self.name

