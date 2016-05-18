from django.conf.urls import url

from .views import views_user

app_name='backend'

urlpatterns = [
        # /user/<pk_user>
        url(r'user/(?P<user_pk>[0-9]+)', views_user.user_details, name='user_details'),
        # /register
        url(r'register', views_user.user_register, name='user_register'),
        # /sign_in
        url(r'sign_in', views_user.user_sign_in, name='sign_in'),
]
