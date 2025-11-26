from django.urls import path
from . import views

urlpatterns = [
    # Course endpoints
    path('courses/create/', views.create_course, name='create_course'),
    path('courses/<int:course_id>/update/', views.update_course, name='update_course'),
    path('courses/<int:course_id>/delete/', views.delete_course, name='delete_course'),
    path('courses/', views.list_courses, name='list_courses'),
    path('courses/search/', views.search_courses, name='search_courses'),

    # Student endpoints
    path('students/associate/', views.associate_student, name='associate_student'),
]
