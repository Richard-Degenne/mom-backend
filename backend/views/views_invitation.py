from datetime import datetime

from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.db.utils import IntegrityError
from django.core.urlresolvers import reverse

from backend.models import *
from backend.views.helpers import *

# Create your views here.

################
# STATUS VIEWS #
################

def invitation_details(request, invitation_pk):
    """
    Get a invitation detailed information.

    @param  invitation_pk     Primary key of the invitation to get

    @return     A JSON object containing the requested info
    or a 404 error if the invitation couldn't be found.

    @see Invitation.json_detail
    """
    get_session_user(request)
    invitation = get_object_or_404(Invitation, pk=invitation_pk)
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
        if rank.fk_event.pk != request.POST['pk_event']:
            raise IntegrityError
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
        return JsonResponse(json_error("Integrity error"), status=400)
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
        rank = get_object_or_404(Rank, pk=request.POST['pk_rank'])
        if rank.fk_event.pk != invitation.fk_event.pk:
            raise IntegrityError
    except KeyError:
        return JsonResponse(json_error("Missing parameters"), status=400)
    except IntergrityError:
        return JsonResponse(json_error("Integrity error"), status=400)
    else:
        try:
            if request.POST['content'] == '':
                request.POST['content'] = invitation.content
        except KeyError:
            request.POST['content'] = invitation.content

    invitation.content = request.POST['content']
    invitation.status = request.POST.get('status', invitation.status)
    invitation.fk_rank = get_object_or_404(Rank, pk=request.POST.get('pk_rank', invitation.fk_rank.pk))
    invitation.save()

    return HttpResponseRedirect(reverse('backend:invitation_details', args=(invitation.pk,)))
