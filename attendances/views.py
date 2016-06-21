from django.shortcuts import render
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterStudentListForm
from .models import Student, Course

SUCCESS_MESSAGE = "You saved succesfully the attendances"


@login_required
def register(request, course_id):
    student_list_form = RegisterStudentListForm(course_id=course_id, professor=get_user(request))
    if request.method == 'POST':
        student_list_form = RegisterStudentListForm(course_id=course_id, professor=get_user(request), data=request.POST)
        if student_list_form.is_valid():
            student_list_form.save()
            messages.info(request, SUCCESS_MESSAGE)
        return render(request, 'register.html', {'course_id': course_id, 'form': student_list_form})
    return render(request, 'register.html', {'course_id': course_id, 'form': student_list_form})


@login_required
def registered(request, course_id, date):
    students = Student.objects.filter(
        attendance__course__id=course_id,
        attendance__course__professors__in=[get_user(request)],
        attendance__date=date
    )
    return render(request, 'registered.html', {'students': students})


@login_required
def courses(request):
    courses = Course.objects.filter(professors__in=[get_user(request)])
    return render(request, 'courses.html', {'courses': courses})
