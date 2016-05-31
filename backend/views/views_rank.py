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
# RANK VIEWS #
##############

def rank_details(request, rank_pk):
    """
    Get a rank detailed information.

    @param  rank_pk     Primary key of the rank to get

    @return     A JSON object containing the requested info
    or a 404 error if the rank couldn't be found.

    @see Rank.json_detail
    """
    user = get_session_user(request)
    rank = get_object_or_404(Rank, pk=rank_pk)
    if not user.has_organiser_access(rank.fk_event):
        raise PermissionDenied
    return JsonResponse(rank.json_detail())

def rank_create(request):
    """
    Register a new rank in the database.

    @return     A JSON object according the @ref rank_details function
    or a 400 error on a bad request.
    """
    user = get_session_user(request)
    try:
        if not user.has_organiser_access(get_object_or_404(Event, pk=request.POST['pk_event'])):
            raise PermissionDenied
        rank = Rank.objects.create(name = request.POST['name'],
                description = request.POST.get('descripion', ''),
                date_created = datetime.now(),
                is_attendee = request.POST.get('is_attendee', None),
                is_organiser = request.POST.get('is_organiser', None),
                is_admin = request.POST.get('is_admin', None),
                fk_event = get_object_or_404(Event, pk=request.POST['pk_event'])
        )
    except KeyError:
        return JsonResponse(json_error("Missing parameters"), status=400)
    except IntegrityError:
        return JsonResponse(json_error("Integrity error"), status=400)
    else:
        return HttpResponseRedirect(reverse('backend:rank_details', args=(rank.pk,)))
