from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import models
from .models import Course, Student
import json


# COURSE VIEWS


@csrf_exempt
def create_course(request):
    if request.method == "POST":
        data = json.loads(request.body)
        course = Course.objects.create(
            name=data["name"],
            instructor=data["instructor"],
            category=data["category"],
        )
        return JsonResponse({"message": "Course created", "course_id": course.id})
    return JsonResponse({"error": "Invalid method"}, status=405)


@csrf_exempt
def update_course(request, course_id):
    if request.method == "PUT":
        data = json.loads(request.body)
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return JsonResponse({"error": "Course not found"}, status=404)
        course.name = data.get("name", course.name)
        course.instructor = data.get("instructor", course.instructor)
        course.category = data.get("category", course.category)
        course.save()
        return JsonResponse({"message": "Course updated"})
    return JsonResponse({"error": "Invalid method"}, status=405)


@csrf_exempt
def delete_course(request, course_id):
    if request.method == "DELETE":
        try:
            course = Course.objects.get(id=course_id)
            course.delete()
            return JsonResponse({"message": "Course deleted"})
        except Course.DoesNotExist:
            return JsonResponse({"error": "Course not found"}, status=404)
    return JsonResponse({"error": "Invalid method"}, status=405)


def list_courses(request):
    courses = Course.objects.order_by("id")
    data = [
        {
            "id": c.id,
            "name": c.name,
            "instructor": c.instructor,
            "category": c.category
        } for c in courses
    ]
    return JsonResponse(data, safe=False)


def search_courses(request):
    # Get query parameters individually
    name = request.GET.get("name", "")
    instructor = request.GET.get("instructor", "")
    category = request.GET.get("category", "")

    # Build a filter using models.Q
    filters = models.Q()
    if name:
        filters &= models.Q(name__icontains=name)
    if instructor:
        filters &= models.Q(instructor__icontains=instructor)
    if category:
        filters &= models.Q(category__icontains=category)

    courses = Course.objects.filter(filters)

    data = [
        {
            "id": c.id,
            "name": c.name,
            "instructor": c.instructor,
            "category": c.category
        } for c in courses
    ]
    return JsonResponse(data, safe=False)




# STUDENT VIEWS


@csrf_exempt
def associate_student(request):
    if request.method == "POST":
        data = json.loads(request.body)
        course_id = data.get("course_id")
        student_id = data.get("student_id")

        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return JsonResponse({"error": f"Course with id {course_id} not found"}, status=404)

        try:
            student_id = int(student_id)
        except (ValueError, TypeError):
            return JsonResponse({"error": "Invalid student_id"}, status=400)

        student_obj, created = Student.objects.get_or_create(course=course, student_id=student_id)

        if created:
            message = "Student added successfully to course"
        else:
            message = "Student is already associated with this course"

        return JsonResponse({
            "message": message,
            "course": course.name,
            "student_id": student_id
        })

    return JsonResponse({"error": "Invalid method"}, status=405)