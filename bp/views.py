# vim: sw=4 ts=4 expandtab ai
#
# This file is part of Bender's Property
# Copyright (C) 2009 Bender's Property development team. All rights reserved.
#
from django.http import HttpResponse
from django.views.generic.simple import direct_to_template
from django.conf import settings

# Import the Django helpers
import facebook.djangofb as facebook
from facebook import FacebookError

# The User model defined in models.py
from models import FBUser, Trade
from pprint import pprint

from django.utils.translation import to_locale
DEFAULT_LOCALE = to_locale(settings.LANGUAGE_CODE)


@facebook.require_login()
def ajax(request):
    return HttpResponse('hello world')

def post_remove(request):
    # Callback when user removes app
    print "Request:"
    pprint(request.REQUEST.items())
    print "FB:"
    pprint(request.facebook.__dict__)
    return HttpResponse('hello world')

def post_auth(request):
    # Callback when user adds app
    print "Request:"
    pprint(request.REQUEST.items())
    print "FB:"
    pprint(request.facebook.__dict__)
    return HttpResponse('hello world')

def render_game_page(request, template, extra_context=None, mimetype=None, **kwargs):
    """ Same as direct_to_template, but adds defaults to context if not there """
    if not extra_context:
        extra_context = {}
    if 'locale' not in extra_context:
        extra_context['locale'] = request.REQUEST.get('fb_sig_locale', DEFAULT_LOCALE)
    return direct_to_template(request, template, extra_context=extra_context, mimetype=mimetype, **kwargs)

def render_game_userpage(request, template, extra_context=None, mimetype=None, **kwargs):
    """ Same as direct_to_template, but add fbuser to context if not there """
    if not extra_context:
        extra_context = {}
    if 'fbuser' not in extra_context:
        extra_context['fbuser'] = FBUser.objects.get_current()
    return render_game_page(request, template, extra_context=extra_context, mimetype=mimetype, **kwargs)


# We'll require login for our canvas page. This
# isn't necessarily a good idea, as we might want
# to let users see the page without granting our app
# access to their info. See the wiki for details on how
# to do this.
@facebook.require_login()
def canvas(request):
    # Get the User object for the currently logged in user
    user = FBUser.objects.get_current()

    # User is guaranteed to be logged in, so pass canvas.fbml
    # an extra 'fbuser' parameter that is the User object for
    # the currently logged in user.
    return render_game_userpage(request, 'canvas.fbml')

@facebook.require_login()
def dump(request):
    print "Request:"
    pprint(request.REQUEST.items())
    print "FB:"
    pprint(request.facebook.__dict__)
    print "IP: %s for %s" % (request.META['REMOTE_ADDR'], request.META['HTTP_X_FB_USER_REMOTE_ADDR'])
    # Default page
    try:
        #obj = request.facebook.application.getPublicInfo(application_id=26646015029)
        #obj = request.facebook.application.getPublicInfo(application_id=70364136730)
        #obj = request.facebook.application.getPublicInfo(application_canvas_name='benders-property')
        #obj = request.facebook.stream.get()
        #obj = request.facebook.__dict__
        #obj = len(request.facebook._friends)
        #obj = request.facebook.friends.getLists()
        #obj = request.facebook.friends.get(flid=105202265658L)
        #obj = FBUser.objects.get_current()
        #obj = request.facebook.__dict__
        #obj = request.REQUEST.items()
        obj = request.META.items()
    except Exception, exj:
        obj = str(exj.__class__)+str(exj)
    #obj = None
    return render_game_page(request, 'dump.fbml', extra_context={'uid': request.facebook.uid, 'obj': obj })

@facebook.require_login()
def index(request):
    # Do something better later
    return request.facebook.redirect('summary')

@facebook.require_login()
def summary(request):
    user = FBUser.objects.get_current()
    if not user.trade:
        #return HttpResponseRedirect('set_trade')
        return request.facebook.redirect('set_trade')
    return render_game_userpage(request, 'summary.fbml', extra_context={'uid': request.facebook.uid, 'fbuser': user})

@facebook.require_login()
def set_trade(request):
    user = FBUser.objects.get_current()
    pprint(request.REQUEST.items())
    if 'trade' not in request.REQUEST:
        return render_game_userpage(request, 'set_trade.fbml', extra_context={'uid': request.facebook.uid, 'trades': Trade.objects.order_by('id')})
    #elif not user.trade:
    elif True:
        try:
            user.trade = Trade.objects.get(pk=int(request.REQUEST['trade']))
            user.save()
        except Trade.DoesNotExist, exc:
            pass
    return request.facebook.redirect(request.facebook.get_app_url())

@facebook.require_login()
def invite(request):
    try:
        friends = request.facebook.friends.getAppUsers()
    except FacebookError, exc:
        friends = []
    return render_game_page(request, 'invite.fbml',
        extra_context={'uid': request.facebook.uid, 'friends': friends, 'add_url': request.facebook.get_add_url()})

@facebook.require_login()
def help(request):
    return render_game_page(request, 'help.fbml')

@facebook.require_login()
def friends(request):
    ufriends = [] + request.facebook.friends.getAppUsers() + [request.facebook.uid]
    ofriends = FBUser.objects.filter(id__in=ufriends).order_by("-value")
    return render_game_userpage(request, 'friends.fbml', extra_context={'friends': ofriends, 'uid': request.facebook.uid })

