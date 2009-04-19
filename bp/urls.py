from django.conf.urls.defaults import *

urlpatterns = patterns('bendersproperty.bp.views',
    (r'^$', 'index'),
    (r'^summary$', 'index'),
    (r'^invite$', 'invite'),
    (r'^help$', 'help'),
    # Define other pages you want to create here
)

