from django.shortcuts import render, get_object_or_404
from .models import Department, Course
from django.contrib.auth.decorators import login_required
from users.decorators import role_required
from students.models import Student

def department_list(request):
    departments = Department.objects.select_related('chairperson')
    return render(request, 'academics/department_list.html', {
        'departments': departments,
    })

@login_required
def department_detail(request, pk):
    department = get_object_or_404(Department, pk=pk)
    staff = department.staff.all()       
    courses = department.courses.all()
    return render(request, 'academics/department_detail.html', {
        'department': department,
        'staff': staff,
        'courses': courses,
    })

def course_list(request):
    courses = Course.objects.select_related('department')
    department = request.GET.get('department')
    if department:
        courses = courses.filter(
            department__name=department
        )
    
    return render(request, 'academics/course_list.html', {
        'courses': courses,
    })

@login_required
def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    enrollments = course.enrollments.select_related('student')
    return render(request, 'academics/course_detail.html', {
        'course': course,
        'enrollments': enrollments,
    })

@login_required
def dashboard(request):
    user = request.user

    if user.role == 'admin':
        context = {
            'departments': Department.objects.all(),
            'total_students': Student.objects.count(),
            'total_courses': Course.objects.count(),
        }
        return render(request, 'academics/admin_dashboard.html', context)

    context = {
        'department': user.department,
        'courses': Course.objects.filter(
            department=user.department
        ) if user.department else Course.objects.none(),
    }
    return render(request, 'academics/instructor_dashboard.html', context)

from rest_framework import filters, viewsets
from .serializers import DepartmentSerializer, CourseSerializer
from .models import Department, Course
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view, extend_schema
from .filters import CourseFilter
from .permissions import IsAdminOrReadOnly

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.select_related('chairperson')
    serializer_class = DepartmentSerializer

@extend_schema_view(
    list=extend_schema(tags=['courses'],
    summary='List courses (filter / search / order)'),
    retrieve=extend_schema(tags=['courses']),
)
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.select_related('department')
    serializer_class = CourseSerializer
    permission_classes = [IsAdminOrReadOnly]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_class = CourseFilter
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'credits']
    ordering = ['name']


