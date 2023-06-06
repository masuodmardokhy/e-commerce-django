from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from home.models import *
from .models import *

from rest_framework import viewsets




@api_view(['GET', 'POST', 'DELETE'])
class Home(viewsets.ModelViewSet):            # for Manage the user's shopping cart information
    pass