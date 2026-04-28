from django.shortcuts import render, redirect, get_object_or_404
from academics.models import Course
from .forms import EnrollmentForm
from django.contrib.auth.decorators import login_required
from users.decorators import role_required

@login_required
@role_required(['admin'])
def enrollment_create(request, course_pk):
    course = get_object_or_404(Course, pk=course_pk)
    
    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            enrollment = form.save(commit=False)
            enrollment.course = course
            enrollment.save()
            return redirect('academics:course_detail', pk=course.pk)
    else:
        form = EnrollmentForm()
    
    return render(request, 'students/enrollment_form.html', {
        'form': form,
        'course': course,
    })

from rest_framework import viewsets
from .serializers import StudentSerializer, EnrollmentSerializer
from .models import Student, Enrollment

class StudentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Student.objects.select_related('major')
    serializer_class = StudentSerializer

class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.select_related('student', 'course')
    serializer_class = EnrollmentSerializer