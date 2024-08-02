from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Account, Destination
from .serializers import AccountSerializer, DestinationSerializer
from django.http import JsonResponse
import requests

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class DestinationViewSet(viewsets.ModelViewSet):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer

@api_view(['GET'])
def get_destinations(request, account_id):
    try:
        account = Account.objects.get(account_id=account_id)
        destinations = Destination.objects.filter(account=account)
        serializer = DestinationSerializer(destinations, many=True)
        return Response(serializer.data)
    except Account.DoesNotExist:
        return Response({"error": "Account not found"}, status=404)

@api_view(['POST'])
def incoming_data(request):
    token = request.headers.get('CL-X-TOKEN')
    if not token:
        return JsonResponse({"error": "Unauthenticated"}, status=401)

    try:
        account = Account.objects.get(app_secret_token=token)
    except Account.DoesNotExist:
        return JsonResponse({"error": "Unauthenticated"}, status=401)

    data = request.data
    for destination in account.destinations.all():
        headers = destination.headers
        url = destination.url
        method = destination.http_method

        if method == 'GET':
            response = requests.get(url, params=data, headers=headers)
        else:
            response = requests.request(method, url, json=data, headers=headers)

    return JsonResponse({"status": "success"})
