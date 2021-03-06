from django import forms
from django.utils import timezone

from .models import Attendance, Student


class RegisterStudentListForm(forms.Form):
    students = forms.ModelMultipleChoiceField(queryset=None, widget=forms.CheckboxSelectMultiple(), required=False)

    def __init__(self, course_id, professor, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.course_id = course_id
        self.fields['students'].queryset = Student.objects.filter(
            course__id=course_id,
            course__professors__in=[professor]
        )
        students_already_registered = Student.objects.filter(
            attendance__course_id=course_id,
            attendance__course__professors__in=[professor],
            attendance__date=timezone.now()
        )
        self.fields['students'].initial = [student.pk for student in students_already_registered]

    def save(self):
        students = self.cleaned_data['students']
        for student in students:
            if not Attendance.objects.filter(course_id=self.course_id, student=student, date=timezone.now()).exists():
                Attendance.objects.create(course_id=self.course_id, student=student)
        for pk in self.fields['students'].initial:
            attendance = Attendance.objects.filter(course_id=self.course_id, student_id=pk, date=timezone.now())
            if attendance.exists():
                attendance.delete()
