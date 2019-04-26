from rest_framework.generics import ListAPIView
from .serializers import *
from users.models import *
from rest_framework.permissions import IsAuthenticated


class CarrierMiniProfileListView(ListAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = CarrierDetailSerializer
    
    def get_queryset(self):
        return Carrier.objects.filter(pk=self.request.user.user_login_profile.carrier.pk)

class CarrierTermsListView(ListAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = TermDetailSerializer

    def get_queryset(self):
        return self.request.user.user_login_profile.carrier.terms

class CarrierTermDetailsListView(ListAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = AttendSerializer

    def get_queryset(self):
        term_id = self.kwargs['term_id']
        return Attend.objects.filter(course__term__pk=term_id, carrier=self.request.user.user_login_profile.carrier)