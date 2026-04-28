from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('courses/<int:course_pk>/enroll/', views.enrollment_create, name='enrollment_create'),
]