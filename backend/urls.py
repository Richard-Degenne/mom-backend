from django.conf.urls import url

from .views import views_user, views_event

app_name='backend'

urlpatterns = [
        ########
        # USER #
        ########
        #/user/<pk_user>/events
        url('user/(?P<user_pk>[0-9]+)/events', views_user.user_events, name='user_events'),
        # /user/<pk_user>
        url(r'user/(?P<user_pk>[0-9]+)', views_user.user_details, name='user_details'),
        # /register
        url(r'register', views_user.user_register, name='user_register'),
        # /sign_in
        url(r'sign_in', views_user.user_sign_in, name='sign_in'),

        #########
        # EVENT #
        #########
        # /event/<pk_event>
        url(r'event/(?P<event_pk>[0-9]+)', views_event.event_details, name='event_details'),
        # /event/create
        url(r'event/create', views_event.event_create, name='event_create'),
]
