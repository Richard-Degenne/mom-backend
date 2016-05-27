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

###############
# EVENT VIEWS #
###############

def event_statuses(request, event_pk):
    """
    Get all the statuses associated on a given event.

    @param  event_pk    Primary key of the event to get

    @return     A JSON array containing the statuses JSON objects.
    """
    get_session_user(request)
    event = get_object_or_404(Event, pk=event_pk)
    response=[]
    for s in Status.objects.filter(fk_event=event.pk):
        response.append({'pk': s.pk,
                'content': s.content,
                'date_created': s.date_created,
                'user_pk': s.fk_user_created_by.pk})
    return JsonResponse(response, safe=False)

def event_tasks(request, event_pk):
    """
    Get all the tasks associated on a given event.

    @param  event_pk    Primary key of the event to get

    @return     A JSON array containing the tasks JSON objects.
    """
    get_session_user(request)
    event = get_object_or_404(Event, pk=event_pk)
    response=[]
    for t in Task.objects.filter(fk_event=event.pk):
        response.append({'pk': t.pk,
                'name': t.name,
                'date_created': t.date_created,
                'user_pk': t.fk_user_created_by.pk})
    return JsonResponse(response, safe=False)

def event_details(request, event_pk):
    """
    Get an event detailed information.

    @param  event_pk     Primary key of the event to get

    @return     A JSON object containing the requested info
    or a 404 error if the event couldn't be found.

    @see Event.json_detail
    """
    get_session_user(request)
    event = get_object_or_404(Event, pk=event_pk)
    return JsonResponse(event.json_detail())

def event_create(request):
    """
    Register a new event in the database.

    @return     A JSON object according the @ref event_details function
    or a 400 error on a bad request.
    """
    user = get_session_user(request)
    try:
        if request.POST['name'] == '':
            raise ValueError
        event = Event.objects.create(name = request.POST['name'],
                description = request.POST.get('description', ''),
                date = request.POST.get('date', None),
                date_created = datetime.now(),
                place_event = request.POST.get('place', ''),
                fk_user_created_by = user
        )
    except ValueError as v:
        print(v)
        return JsonResponse(json_error("Name cannot be empty"), status=400)
    except KeyError:
        return JsonResponse(json_error("Missing parameters"), status=400)
    except IntegrityError:
        return JsonResponse(json_error("Integrity error"), status=400)
    else:
        return HttpResponseRedirect(reverse('backend:event_details', args=(event.pk,)))
