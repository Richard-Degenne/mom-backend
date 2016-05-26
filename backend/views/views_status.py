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

################
# STATUS VIEWS #
################

def status_details(request, status_pk):
    """
    Get a status detailed information.

    @param  status_pk     Primary key of the status to get

    @return     A JSON object containing the requested info
    or a 404 error if the status couldn't be found.

    @see Status.json_detail
    """
    get_session_user(request)
    status = get_object_or_404(Status, pk=status_pk)
    return JsonResponse(status.json_detail())

def status_create(request):
    """
    Register a new status in the database.

    @return     A JSON object according the @ref status_details function
    or a 400 error on a bad request.
    """
    user = get_session_user(request)
    try:
        status = Status.objects.create(content = request.POST['content'],
                date_created = datetime.now(),
                fk_event = get_object_or_404(Event, pk=request.POST['pk_event']),
                fk_user_created_by = user
        )
    except KeyError:
        return JsonResponse(json_error("Missing parameters"), status=400)
    except IntegrityError:
        return JsonResponse(json_error("Integrity error"), status=400)
    else:
        return HttpResponseRedirect(reverse('backend:status_details', args=(status.pk,)))
