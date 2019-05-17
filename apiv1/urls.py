from django.urls import include, path
from .views import *

urlpatterns = [
    path("carrier/mini_profile/", CarrierMiniProfileListView.as_view()),
    path("carrier/terms/", CarrierTermsListView.as_view()),
    path("carrier/terms/<term_id>/", CarrierTermDetailsListView.as_view()),
    path("carrier/terms/gradessummary/<term_id>/", TermSummaryView.as_view())
]