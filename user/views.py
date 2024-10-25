from django.shortcuts import render
from .models import User
from .serializers import UserSerializer
from django.http import JsonResponse
from rest_framework.decorators import api_view

#juste pour test
@api_view(['GET'])
def list_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return JsonResponse(serializer.data, safe=False)
