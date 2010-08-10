from django.conf.urls.defaults import *

from .views import handle_token

urlpatterns = patterns('',
    url(r'^token/(.*)/$', handle_token, name='token_handle'),
)
