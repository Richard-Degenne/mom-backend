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
    user = get_session_user(request)
    status = get_object_or_404(Status, pk=status_pk)
    if not user.has_attendee_access(status.fk_event):
        raise PermissionDenied
    return JsonResponse(status.json_detail())

def status_create(request):
    """
    Register a new status in the database.

    @return     A JSON object according the @ref status_details function
    or a 400 error on a bad request.
    """
    user = get_session_user(request)
    try:
        if not user.has_organiser_access(get_object_or_404(Event, pk=request.POST['pk_event'])):
            raise PermissionDenied
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
