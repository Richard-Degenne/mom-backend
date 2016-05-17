from django.conf.urls import url

from . import views

app_name='backend'

urlpatterns = [
        # /user/<pk_user>
        url(r'user/(?P<user_pk>[0-9]+)', views.user_details, name='user_details'),
        # /register
        url(r'register', views.user_register, name='user_register')
]
