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


##############
# TASK VIEWS #
##############
def task_items(request, task_pk):
    """
    Get all the items associated to a given task.

    @param  task_pk     Primary key of the task to get

    @return     A JSON array containing all the items JSON objects.
    """
    get_session_user(request)
    task = get_object_or_404(Task, pk=task_pk)
    response=[]
    for i in TaskItem.objects.filter(fk_task=task):
        response.append({'pk': i.pk,
                'name': i.name,
                'completed': i.completed,
                'date_created': i.date_created})
    return JsonResponse(response, safe=False)

def task_details(request, task_pk):
    """
    Get a task detailed information.

    @param  task_pk     Primary key of the task to get

    @return     A JSON object containing the requested info
    or a 404 error if the task couldn't be found.

    @see Task.json_detail
    """
    get_session_user(request)
    task = get_object_or_404(Task, pk=task_pk)
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
                fk_event=get_object_or_404(Event, pk=request.POST['event_pk']),
                fk_user_created_by = user
        )
    except ValueError as v:
        return JsonResponse(json_error("Name cannot be empty"), status=400)
    except KeyError:
        return JsonResponse(json_error("Missing parameters"), status=400)
    else:
        return HttpResponseRedirect(reverse('backend:task_details', args=(task.pk,)))
