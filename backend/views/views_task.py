from datetime import datetime

from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.db.utils import IntegrityError
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied

from backend.models import *
from backend.views.helpers import *

# Create your views here.

##############
# TASK VIEWS #
##############
def task_items(request, task_pk):
    """
    Get all the items associated to a given task.

    @param  task_pk     Primary key of the task to get

    @return     A JSON array containing all the items JSON objects.
    """
    user = get_session_user(request)
    task = get_object_or_404(Task, pk=task_pk)
    if not user.has_organiser_access(task.fk_event):
        raise PermissionDenied
    response={}
    response['items'] = []
    for i in TaskItem.objects.filter(fk_task=task):
        response['items'].append({'pk': i.pk,
                'name': i.name,
                'completed': i.completed,
                'date_created': i.date_created})
    return JsonResponse(response, safe=False)

def task_comments(request, task_pk):
    """
    Get all the comments associated to a given task.

    @param  task_pk     Primary key of the task to get

    @return     A JSON array containing all the comments JSON objects.
    """
    user = get_session_user(request)
    task = get_object_or_404(Task, pk=task_pk)
    if not user.has_organiser_access(task.fk_event):
        raise PermissionDenied
    response={}
    response['comments'] = []
    for c in Comment.objects.filter(fk_task=task):
        response['comments'].append({'pk': c.pk,
                'content': c.content,
                'date_created': c.date_created,
                'pk_user_created_by': c.fk_user_created_by.pk})
    return JsonResponse(response, safe=False)

def task_add_user(request, task_pk):
    """
    Affects a new user to a given task.

    @param  task_pk     Primary key of the task to get
    """
    user_request = get_session_user(request)
    task = get_object_or_404(Task, pk=task_pk)
    if not user_request.has_organiser_access(task.fk_event):
        raise PermissionDenied
    try:
        user = get_object_or_404(User, pk=request.POST['pk_user'])
    except KeyError:
        return JsonResponse(json_error("Missing parameters"), status=400)
    else:
        IsAffectedTo.objects.create(fk_task=task, fk_user=user)
        return HttpResponseRedirect(reverse('backend:task_details', args=(task.pk,)))

def task_users(request, task_pk):
    """
    Get all the users affected to a given task.

    @param  task_pk     Primary key of the task to get

    @return     A JSON array containing all the users JSON objects.
    """
    user = get_session_user(request)
    task = get_object_or_404(Task, pk=task_pk)
    if not user.has_organiser_access(task.fk_event):
        raise PermissionDenied
    response={}
    response['users'] = []
    for u in User.objects.filter(pk__in = IsAffectedTo.objects.filter(fk_task = task)
            .values_list('fk_user__pk', flat=True)):
        response['users'].append(u.json_detail_public())
    return JsonResponse(response, safe=False)

def task_details(request, task_pk):
    """
    Get a task detailed information.

    @param  task_pk     Primary key of the task to get

    @return     A JSON object containing the requested info
    or a 404 error if the task couldn't be found.

    @see Task.json_detail
    """
    user = get_session_user(request)
    task = get_object_or_404(Task, pk=task_pk)
    if not user.has_organiser_access(task.fk_event):
        raise PermissionDenied
    return JsonResponse(task.json_detail())

def task_create(request):
    """
    Register a new task in the database.

    @return     A JSON object according the @ref task_details function
    or a 400 error on a bad request.
    """
    user = get_session_user(request)
    # Set description to null if it is not given in the request or blank
    try:
        if not user.has_organiser_access(get_object_or_404(request.POST['pk_event'])):
            raise PermissionDenied
        if request.POST['description'] == '':
            request.POST['description'] = None
    except KeyError:
        request.POST['description'] = None

    try:
        if request.POST['name']=='':
            raise ValueError
        task = Task.objects.create(name = request.POST['name'],
                description = request.POST['description'],
                date_created =datetime.now(),
                fk_event=get_object_or_404(Event, pk=request.POST['pk_event']),
                fk_user_created_by = user
        )
    except ValueError as v:
        return JsonResponse(json_error("Name cannot be empty"), status=400)
    except KeyError:
        return JsonResponse(json_error("Missing parameters"), status=400)
    else:
        return HttpResponseRedirect(reverse('backend:task_details', args=(task.pk,)))
