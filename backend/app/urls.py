from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/courses/<str:course_id>/', include('metrics.api.endpoints')),
]
