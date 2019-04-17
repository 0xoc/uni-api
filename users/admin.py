from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(UserLoginProfile)
admin.site.register(Student)
admin.site.register(College)
admin.site.register(Department)
admin.site.register(Field)
admin.site.register(FieldCourse)
admin.site.register(Subfield)
admin.site.register(FieldCourseSubfield)
admin.site.register(Carrier)
admin.site.register(Professor)
admin.site.register(Term)
admin.site.register(Course)
admin.site.register(Teaches)
admin.site.register(PreliminaryRegistration)
admin.site.register(Grade)
admin.site.register(Attends)
admin.site.register(Credit)
admin.site.register(DayRange)
admin.site.register(DayTime)
admin.site.register(WeeklySchedule)
