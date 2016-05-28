from datetime import datetime

from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.db.utils import IntegrityError
from django.core.urlresolvers import reverse

from backend.models import *
from backend.views.helpers import *

# Create your views here.

###################
# TASK ITEM VIEWS #
###################
def task_item_details(request, task_item_pk):
    """
    Get a task item detailed information.

    @param  task_item_pk     Primary key of the task item to get

    @return     A JSON object containing the requested info
    or a 404 error if the task item couldn't be found.

    @see TaskItem.json_detail
    """
    get_session_user(request)
    task_item = get_object_or_404(TaskItem, pk=task_item_pk)
    return JsonResponse(task_item.json_detail())

def task_item_create(request):
    """
    Register a new task item in the database.

    @return     A JSON object according the @ref user_detail function
    or a 400 error on a bad request.
    """
    user = get_session_user(request)
    try:
        if request.POST['name'] == '':
            raise ValueError
        task_item = TaskItem.objects.create(name = request.POST['name'],
                completed = False,
                fk_task = get_object_or_404(Task, pk=request.POST['pk_task']),
                date_created = datetime.now()
        )
    except ValueError:
        return JsonResponse(json_error("Name cannot be empty"), status=400)
    except KeyError:
        return JsonResponse(json_error("Missing parameters"), status=400)
    else:
        return HttpResponseRedirect(reverse('backend:task_item_details', args=(task_item.pk,)))

def task_item_edit(request):
    """
    Edit an existing task item in the database.

    @return     A JSON object according the @ref user_detail function
    or a 400 error on a bad request.
    """
    user = get_session_user(request)
    try:
        task_item = get_object_or_404(TaskItem, pk=request.POST['pk_task_item'])
    except KeyError:
        return JsonResponse(json_error("Missing parameters"), status=400)
    else:
        try:
            if request.POST['name'] == '':
                request.POST['name'] = task_item.name
        except KeyError:
            request.POST['name'] = task_item.name

    task_item.name = request.POST['name']
    task_item.completed = request.POST.get('completed', task_item.completed)
    task_item.save()

    return HttpResponseRedirect(reverse('backend:task_item_details', args=(task_item.pk,)))
