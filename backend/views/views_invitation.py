from datetime import datetime

from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied

from backend.models import *
from backend.views.helpers import *

# Create your views here.

####################
# INVITATION VIEWS #
####################

def invitation_details(request, invitation_pk):
    """
    Get a invitation detailed information.

    @param  invitation_pk     Primary key of the invitation to get

    @return     A JSON object containing the requested info
    or a 404 error if the invitation couldn't be found.

    @see Invitation.json_detail
    """
    user = get_session_user(request)
    invitation = get_object_or_404(Invitation, pk=invitation_pk)
    if(not user.has_attendee_access(invitation.fk_event)):
        raise PermissionDenied
    return JsonResponse(invitation.json_detail())

def invitation_create(request):
    """
    Register a new invitation in the database.

    @return     A JSON object according the @ref invitation_details function
    or a 400 error on a bad request.
    """
    user = get_session_user(request)
    try:
        rank = get_object_or_404(Rank, pk=request.POST['pk_rank'])
        event = get_object_or_404(Event, pk=request.POST['pk_event'])
        if rank.fk_event != event:
            raise IntegrityError
        if not user.has_organiser_access(event):
            raise PermissionDenied
        invitation = Invitation.objects.create(content = request.POST.get('content', ''),
                status = 'P', #Pending
                date_created = datetime.now(),
                fk_event = get_object_or_404(Event, pk=request.POST['pk_event']),
                fk_user_created_by = user,
                fk_user_invited = get_object_or_404(User, pk=request.POST['pk_user']),
                fk_rank = get_object_or_404(Rank, pk=request.POST['pk_rank'])
        )
    except KeyError:
        return JsonResponse(json_error("Missing parameters"), status=400)
    except IntegrityError:
        return JsonResponse(json_error("Integrity error: Wrong event/rank combination"), status=400)
    else:
        return HttpResponseRedirect(reverse('backend:invitation_details', args=(invitation.pk,)))

def invitation_edit(request):
    """
    Edit an existing invitation in the database.

    @return     A JSON object according the @ref user_detail function
    or a 400 error on a bad request.
    """
    user = get_session_user(request)
    try:
        invitation = get_object_or_404(Invitation, pk=request.POST['pk_invitation'])
        if not user.has_organiser_access(invitation.fk_event):
            raise PermissionDenied
        rank = get_object_or_404(Rank, pk=invitation.fk_rank.pk)
        if rank.fk_event.pk != invitation.fk_event.pk:
            raise IntegrityError
    except KeyError as v:
        print(v)
        return JsonResponse(json_error("Missing parameters"), status=400)
    except IntegrityError as v:
        print(v)
        return JsonResponse(json_error("Integrity error"), status=400)
    else:
        try:
            if request.POST['content'] == '':
                request.POST['content'] = invitation.content
        except KeyError:
            pass

    invitation.content = request.POST.get('content', invitation.content)
    invitation.status = request.POST.get('status', invitation.status)
    invitation.save()

    return HttpResponseRedirect(reverse('backend:invitation_details', args=(invitation.pk,)))
