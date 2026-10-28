from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # This routes all /api/... requests to api/urls.py file
    path('api/', include('api.urls')),
]

