from rest_framework.generics import ListAPIView
from .serializers import *
from users.models import *
from rest_framework.permissions import IsAuthenticated


class CarrierMiniProfileListView(ListAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = CarrierDetailSerializer
    
    def get_queryset(self):
        return Carrier.objects.filter(pk=self.request.user.user_login_profile.carrier.pk)
    