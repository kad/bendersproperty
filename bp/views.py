# vim: sw=4 ts=4 expandtab ai
#
# This file is part of Bender's Property
# Copyright (C) 2009 Bender's Property development team. All rights reserved.
#
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.views.generic.simple import direct_to_template, redirect_to
from django.conf import settings

# Import the Django helpers
import facebook.djangofb as facebook
from facebook import FacebookError

# The User model defined in models.py
from models import FBUser, Trade

@facebook.require_login()
def ajax(request):
    return HttpResponse('hello world')

def app_base_path(request):
    return request.path[:request.path.find('/',1)+1]

# We'll require login for our canvas page. This
# isn't necessarily a good idea, as we might want
# to let users see the page without granting our app
# access to their info. See the wiki for details on how
# to do this.
@facebook.require_login()
def canvas(request):
    # Get the User object for the currently logged in user
    user = FBUser.objects.get_current()

    # Check if we were POSTed the user's new language of choice
    #if 'language' in request.POST:
    #    user.language = request.POST['language'][:64]
    #    user.save()

    # User is guaranteed to be logged in, so pass canvas.fbml
    # an extra 'fbuser' parameter that is the User object for
    # the currently logged in user.
    return direct_to_template(request, 'canvas.fbml', extra_context={'fbuser': user, 'current_page': 'land_market' })

@facebook.require_login()
def dump(request):
    # Default page
    try:
        #obj = request.facebook.application.getPublicInfo(application_id=26646015029)
        #obj = request.facebook.application.getPublicInfo(application_id=70364136730)
        #obj = request.facebook.application.getPublicInfo(application_canvas_name='property-ladder')
        #obj = request.facebook.application.getPublicInfo(application_api_key='8ed20e0c7c6fce5a401647cd83f463ba')
        #obj = request.facebook.stream.get()
        #obj = request.facebook.__dict__
        #obj = len(request.facebook._friends)
        #obj = request.facebook.friends.getLists()
        #obj = request.facebook.friends.get(flid=105202265658L)
        #obj = FBUser.objects.get_current()
        obj = request.REQUEST.items()
    except Exception, exj:
        obj = str(exj.__class__)+str(exj)
    #obj = None
    return direct_to_template(request, 'dump.fbml', extra_context={'uid': request.facebook.uid, 'current_page': 'index', 'obj': obj })

@facebook.require_login()
def index(request):
    return HttpResponseRedirect('summary')

@facebook.require_login()
def summary(request):
    user = FBUser.objects.get_current()
    if not user.trade:
        return HttpResponseRedirect('set_trade')
    return direct_to_template(request, 'summary.fbml', extra_context={'uid': request.facebook.uid, 'current_page': 'index', 'fbuser': user })


@facebook.require_login()
def set_trade(request):
    user = FBUser.objects.get_current()
    if 'trade' not in request.GET:
        return direct_to_template(request, 'set_trade.fbml', extra_context={'uid': request.facebook.uid, 'current_page': 'set_trade', 'trades': Trade.objects.order_by('id') })
    elif not user.trade:
        try:
            user.trade = Trade.objects.get(pk=int(request.GET['trade']))
            user.save()
        except Trade.DoesNotExist, exc:
            pass
    #return redirect_to(request, app_base_path(request))
    return HttpResponseRedirect(app_base_path(request))
    #return HttpResponsePermanentRedirect(app_base_path(request))


@facebook.require_login()
def invite(request):
    try:
        friends = request.facebook.friends.getAppUsers()
    except FacebookError, exc:
        friends = []

    return direct_to_template(request, 'invite.fbml',
        extra_context={'uid': request.facebook.uid, 'friends': friends, 'add_url': request.facebook.get_add_url(), 'current_page': 'invite'})

@facebook.require_login()
def help(request):
    return direct_to_template(request, 'help.fbml', extra_context={'current_page': 'help'})

@facebook.require_login()
def friends(request):
    ufriends = request.facebook.friends.getAppUsers()
    ufriends.append(request.facebook.uid)
    return direct_to_template(request, 'friends.fbml', extra_context={'current_page': 'friends', 'friends': ufriends, 'uid': request.facebook.uid })

