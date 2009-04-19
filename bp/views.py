# vim: sw=4 ts=4 expandtab ai
#
# This file is part of Bender's Property
# Copyright (C) 2009 Bender's Property development team. All rights reserved.
#
from django.http import HttpResponse
from django.views.generic.simple import direct_to_template

# Import the Django helpers
import facebook.djangofb as facebook
from facebook import FacebookError

# The User model defined in models.py
from models import User


@facebook.require_login()
def ajax(request):
    return HttpResponse('hello world')

# We'll require login for our canvas page. This
# isn't necessarily a good idea, as we might want
# to let users see the page without granting our app
# access to their info. See the wiki for details on how
# to do this.
@facebook.require_login()
def canvas(request):
    # Get the User object for the currently logged in user
    user = User.objects.get_current()

    # Check if we were POSTed the user's new language of choice
    if 'language' in request.POST:
        user.language = request.POST['language'][:64]
        user.save()

    friends = request.facebook.friends.getAppUsers()

    # User is guaranteed to be logged in, so pass canvas.fbml
    # an extra 'fbuser' parameter that is the User object for
    # the currently logged in user.
    return direct_to_template(request, 'canvas.fbml', extra_context={'fbuser': user, 'friends': friends })

@facebook.require_login()
def index(request):
    # Default page
    return direct_to_template(request, 'index.fbml', extra_context={'uid': request.facebook.uid})

@facebook.require_login()
def invite(request):
    try:
        friends = request.facebook.friends.getAppUsers()
    except FacebookError, exc:
        friends = []

    return direct_to_template(request, 'invite.fbml',
        extra_context={'uid': request.facebook.uid, 'friends': friends, 'add_url': request.facebook.get_add_url(), })

@facebook.require_login()
def help(request):
    return direct_to_template(request, 'help.fbml')

