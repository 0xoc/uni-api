from django.urls import include, path
from .views import *

urlpatterns = [
    path("carrier/mini_profile/", CarrierMiniProfileListView.as_view())
]