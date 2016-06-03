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

#################
# COMMENT VIEWS #
#################

def comment_details(request, comment_pk):
    """
    Get a comment detailed information.

    @param  comment_pk     Primary key of the comment to get

    @return     A JSON object containing the requested info
    or a 404 error if the comment couldn't be found.

    @see Comment.json_detail
    """
    user = get_session_user(request)
    comment = get_object_or_404(Comment, pk=comment_pk)
    if(not user.has_organiser_access(comment.fk_task.fk_event)):
        raise PermissionDenied
    return JsonResponse(comment.json_detail())

def comment_create(request):
    """
    Register a new comment in the database.

    @return     A JSON object according the @ref comment_details function, 400 error on a bad request or a 403 error on a forbidden access.
    """
    user = get_session_user(request)
    try:
        task = get_object_or_404(Task, pk=request.POST['pk_task'])
        if(not user.has_organiser_access(task.fk_event)):
            raise PermissionDenied
        comment = Comment.objects.create(content = request.POST['content'],
                date_created = datetime.now(),
                fk_task = get_object_or_404(Task, pk=request.POST['pk_task']),
                fk_user_created_by = user
        )
    except KeyError:
        return JsonResponse(json_error("Missing parameters"), comment=400)
    except IntegrityError:
        return JsonResponse(json_error("Integrity error"), comment=400)
    else:
        return HttpResponseRedirect(reverse('backend:comment_details', args=(comment.pk,)))
