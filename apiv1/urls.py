from django.urls import include, path
from .views import *

urlpatterns = [
    path("carrier/mini_profile/", CarrierMiniProfileListView.as_view()),
    path("carrier/terms/", CarrierTermsListView.as_view())
]