from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AccountViewSet, DestinationViewSet, get_destinations, incoming_data

router = DefaultRouter()
router.register(r'accounts', AccountViewSet)
router.register(r'destinations', DestinationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('destinations/<uuid:account_id>/', get_destinations, name='get_destinations'),
    path('server/incoming_data/', incoming_data, name='incoming_data'),
]
