from backend.models import User

from django.core.exceptions import PermissionDenied

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
        action_user = User.objects.get(pk=request.session['pk_user'])
    except (KeyError, User.DoesNotExist):
        raise PermissionDenied
    else:
        return action_user
