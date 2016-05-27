from django.conf.urls import url

from .views import views_user, views_event, views_status, views_task, views_task_item, views_comment

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
        # /event/<pk_event>/statuses
        url(r'event/(?P<event_pk>[0-9]+)/statuses', views_event.event_statuses, name='event_statuses'),
        # /event/<pk_event>/tasks
        url(r'event/(?P<event_pk>[0-9]+)/tasks', views_event.event_tasks, name='event_tasks'),
        # /event/<pk_event>
        url(r'event/(?P<event_pk>[0-9]+)', views_event.event_details, name='event_details'),
        # /event/create
        url(r'event/create', views_event.event_create, name='event_create'),

        ########
        # TASK #
        ########
        # /task/<pk_task>/items
        url(r'task/(?P<task_pk>[0-9]+)/items', views_task.task_items, name='task_items'),
        # /task/<pk_task>/comments
        url(r'task/(?P<task_pk>[0-9]+)/comments', views_task.task_comments, name='task_comments'),
        # /task/<pk_task>/add_user
        url(r'task/(?P<task_pk>[0-9]+)/add_user', views_task.task_add_user, name='task_add_user'),
        # /task/<pk_task>
        url(r'task/(?P<task_pk>[0-9]+)', views_task.task_details, name='task_details'),
        # /task/create
        url(r'task/create', views_task.task_create, name='task_create'),

        #############
        # TASK ITEM #
        #############
        # /task_item/<pk_task_item>
        url(r'task_item/(?P<task_item_pk>[0-9]+)', views_task_item.task_item_details, name='task_item_details'),
        # /task_item/create
        url(r'task_item/create', views_task_item.task_item_create, name='task_item_create'),
        # /task_item/edit
        url(r'task_item/edit', views_task_item.task_item_edit, name='task_item_edit'),

        ###########
        # COMMENT #
        ###########
        # /comment/create
        url(r'comment/create', views_comment.comment_create, name='comment_create'),
        # /comment/<pk_comment>
        url(r'comment/(?P<comment_pk>[0-9]+)', views_comment.comment_details, name='comment_details'),

        ##########
        # STATUS #
        ##########
        # /status/create
        url(r'status/create', views_status.status_create, name='status_create'),
        # /status/<pk_status>
        url(r'status/(?P<status_pk>[0-9]+)', views_status.status_details, name='status_details'),
]
