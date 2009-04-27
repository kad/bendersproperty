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
            user.hours = 6
            user.last_reset = datetime.now()
            user.last_rent_collected = datetime.now()
            pass
        return user

class Trade(models.Model):
    """ Trades (Builder/Plumber/Electrican/Plasterer/Decorator) """
    name = models.CharField(blank=False, unique=True)


class FBUser(models.Model):
    """A simple User model for Facebook users."""
    # Add the custom manager
    objects = FBUserManager()

    # We use the user's UID as the primary key in our database.
    id = BigPositiveIntegerField(primary_key=True)

    cash = BigPositiveIntegerField(default=35000)
    last_rent_collected = models.DateTimeField()

    trade = models.ForeignKey(Trade)
    hour_rate = models.IntegerField(default=0)

    exp_builder = models.IntegerField(default=0)
    exp_plumber = models.IntegerField(default=0)
    exp_electrician = models.IntegerField(default=0)
    exp_plasterer = models.IntegerField(default=0)
    exp_decorator = models.IntegerField(default=0)

    hours = models.IntegerField(default=6)
    reserved_hours = models.IntegerField(default=0)
    last_reset = models.DateTimeField()


