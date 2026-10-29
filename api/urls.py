from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BountyViewSet, SubmissionViewSet, dashboard_view, submit_view
from django.views.generic import RedirectView # Import RedirectView

# The router automatically generates the URL patterns for our viewsets
router = DefaultRouter()
router.register(r'bounties', BountyViewSet)
router.register(r'submissions', SubmissionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('', RedirectView.as_view(url='/submit/', permanent=False)), 
    path('submit/', submit_view, name='submit'),
]