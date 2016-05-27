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
    {'comment': "failure", 'message': <message>}
    """
    return {'comment': "failure",
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
        return JsonResponse(json_error("Unauthorized"), comment=401)
    else:
        return action_user

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
    get_session_user(request)
    comment = get_object_or_404(Comment, pk=comment_pk)
    return JsonResponse(comment.json_detail())

def comment_create(request):
    """
    Register a new comment in the database.

    @return     A JSON object according the @ref comment_details function
    or a 400 error on a bad request.
    """
    user = get_session_user(request)
    try:
        comment = Comment.objects.create(content = request.POST['content'],
                date_created = datetime.now(),
                fk_task = get_object_or_404(Task, pk=request.POST['task_pk']),
                fk_user_created_by = user
        )
    except KeyError:
        return JsonResponse(json_error("Missing parameters"), comment=400)
    except IntegrityError:
        return JsonResponse(json_error("Integrity error"), comment=400)
    else:
        return HttpResponseRedirect(reverse('backend:comment_details', args=(comment.pk,)))
