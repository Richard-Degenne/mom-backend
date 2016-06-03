from datetime import datetime
import requests
from mom.secrets import google_api_key # This is an invisible file, for privacy purposes.

from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.db.utils import IntegrityError
from django.db.models import Q
from django.core.urlresolvers import reverse

from backend.models import *
from backend.views.helpers import *

# Create your views here.

##########
# HELPER #
##########

def get_google_user_id(token):
    response = requests.get("https://www.googleapis.com/oauth2/v2/tokeninfo?id_token="+token+"&key="+google_api_key)
    if response.status_code != 200:
        raise ValueError
    else:
        print(response.json())
        return response.json()['user_id']

def success(request, pk_user):
    request.session['pk_user'] = user.pk
    return {'status':'success', 'pk_user': user.pk}
#################
# NETWORK VIEWS #
#################
def network_sync(request):
    try:
        network = get_object_or_404(Network, name__iexact=request.POST['network'])
        if network == Network.objects.get(name="Google"):
            # OAuth v2 Google
            token_user_id = get_google_user_id(request.POST['token']) # throws ValueError on invalid token
            sync = IsSyncedWith.objects.get(user_id=token_user_id)
            response = success(request, sync.fk_user.pk)
        else:
            return JsonResponse(json_error("Unknown network"), status=400)
    except ValueError:
        return JsonResponse(json_error("Invalid token"), status=400)
    except KeyError:
        return JsonResponse(json_error("Missing parameters"), status=400)
    except Network.DoesNotExist:
        return JsonResponse(json_error("Network does not exist"), status=400)
    except IsSyncedWith.DoesNotExist:
        try:
            user = get_object_or_404(User, pk=request.POST['pk_user'])
            sync = IsSyncedWith.objects.create(user_id = token_user_id,
                    fk_user = user,
                    fk_network = network)
            response = success(request, sync.fk_user.pk)
        except KeyError:
            response = {'status': "failure"} # Need a user_pk to setup sync
    return JsonResponse(response)
