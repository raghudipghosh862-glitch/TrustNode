from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BountyViewSet, SubmissionViewSet

# The router automatically generates the URL patterns for our viewsets
router = DefaultRouter()
router.register(r'bounties', BountyViewSet)
router.register(r'submissions', SubmissionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]