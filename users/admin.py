from django.contrib import admin
from .models import *
from django_jalali.admin.filters import JDateFieldListFilter
import django_jalali.admin as jadmin

admin.site.register(UserLoginProfile)
admin.site.register(Student)
admin.site.register(College)
admin.site.register(Department)
admin.site.register(Field)
admin.site.register(FieldCourse)
admin.site.register(Subfield)
admin.site.register(FieldCourseSubfieldRelation)
admin.site.register(Carrier)
admin.site.register(Professor)

class JTerm(admin.ModelAdmin):
    list_filter = (
        ('start_date', JDateFieldListFilter),
        ('end_date', JDateFieldListFilter)
    )
admin.site.register(Term, JTerm)

class JCourse(admin.ModelAdmin):
    list_filter = (
        ('midterm_exam_date', JDateFieldListFilter),
        ('final_exam_date', JDateFieldListFilter)
    )
admin.site.register(Course, JCourse)

admin.site.register(Teach)
admin.site.register(PreliminaryRegistration)
admin.site.register(Attend)
admin.site.register(Credit)
admin.site.register(DayRange)
admin.site.register(DayTime)
admin.site.register(DayTimeCourseRelation)

class JGrade(admin.ModelAdmin):
    list_filter = (
        ('date_examined', JDateFieldListFilter),
    )
admin.site.register(Grade, JGrade)