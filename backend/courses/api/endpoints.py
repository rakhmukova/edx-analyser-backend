from django.urls import path

from courses.api import views

urlpatterns = [
    path('', views.CourseView.as_view({'get': 'get_available_courses'}))
]
