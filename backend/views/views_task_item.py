from datetime import datetime

from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.db.utils import IntegrityError
from django.core.urlresolvers import reverse

from backend.models import *

# Create your views here.

####################
# HELPER FUNCTIONS #
####################

def json_error(message):
    """
    Generates a JSON object to indicate an error.

    @param  message     The message to associate to the error.

    @return A JSON object with the following structure:
    {'status': "failure", 'message': <message>}
    """
    return {'status': "failure",
            'message': message
    }

def get_session_user(request):
    """
    Checks in the session variable wether the client making the request
    is logged in.

    @return     On success, the User object associated with the session.
    On failure, return a 401 error.
    """
    try:
        action_user = User.objects.get(pk=request.session['user_pk'])
    except (KeyError, User.DoesNotExist):
        return JsonResponse(json_error("Unauthorized"), status=401)
    else:
        return action_user

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
                fk_task = get_object_or_404(Task, pk=request.POST['task_pk']),
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
        task_item = get_object_or_404(TaskItem, pk=request.POST['task_item_pk'])
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
