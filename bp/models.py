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

class BigPositiveIntegerField(PositiveIntegerField):
    empty_strings_allowed=False
    def get_internal_type(self):
        return "BigPositiveIntegerField"

    def db_type(self):
        if  settings.DATABASE_ENGINE == 'oracle':
            return 'NUMBER(19) UNSIGNED'
        else:
            return 'bigint unsigned'

class UserManager(models.Manager):
    """Custom manager for a Facebook User."""

    def get_current(self):
        """Gets a User object for the logged-in Facebook user."""
        facebook = get_facebook_client()
        user, created = self.get_or_create(id=int(facebook.uid))
        if created:
            # we could do some custom actions for new users here...
            pass
        return user

class User(models.Model):
    """A simple User model for Facebook users."""

    # We use the user's UID as the primary key in our database.
    id = BigPositiveIntegerField(primary_key=True)

    # TODO: The data that you want to store for each user would go here.
    # For this sample, we let users let people know their favorite progamming
    # language, in the spirit of Extended Info.
    language = models.CharField(default='Python', max_length=64)

    # Add the custom manager
    objects = UserManager()
