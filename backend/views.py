from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.db.utils import IntegrityError
from django.core.urlresolvers import reverse

from .models import *

# Create your views here.

def json_error(message):
    return {'message': message}

def user_details(request, user_pk):
    """
    Get a user detailed information.

    @param  user_pk     Primary key of the user to get

    @return     A JSON object containing the requested info
    or a 404 error if the user couldn't be found.

    @see User.json_detail
    """
    user = get_object_or_404(User, pk=user_pk)
    return JsonResponse(user.json_detail())

def user_register(request):
    """
    Register a new user in the database.

    @return     A JSON object according the @ref user_details function
    or a 400 error on a bad request.
    """
    # Set phone_number to null if it is not given in the request or blank
    try:
        if request.POST['phone_number'] == '':
            request.POST['phone_number'] = None
    except KeyError:
        request.POST['phone_number'] = None

    try:
        if request.POST['password'] == '' or request.POST['email'] == '':
            raise ValueError
        user = User.objects.create(first_name = request.POST.get('first_name', ''),
                last_name = request.POST.get('last_name', ''),
                email = request.POST['email'],
                password = request.POST['password'],
                phone_number = request.POST['phone_number']
        )
    except ValueError:
        return JsonResponse(json_error("Password/Email cannot be empty"), status=400)
    except KeyError:
        return JsonResponse(json_error("Missing parameters"), status=400)
    except IntegrityError:
        return JsonResponse(json_error("Phone number/email already exists"), status=400)
    else:
        return HttpResponseRedirect(reverse('backend:user_details', args=(user.pk,)))
        
