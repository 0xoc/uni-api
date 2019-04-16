from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserLoginProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_login_profile')

    # todo: other login info

    def __str__(self):
        return str(self.user)

class Student(models.Model):
    first_name = models.CharField(max_length=255, blank=False)
    last_name = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return str(self.first_name) + " " + str(self.last_name)

class College(models.Model):
    pass

class Department(models.Model):
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name='departments')

class Field(models.Model):
    head_department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='main_fields')
    departments = models.ManyToManyField(Department, blank=False, related_name='fields')

class FieldCourse(models.Model):
    corequisites = models.ManyToManyField('FieldCourse', blank=True, related_name='corequisite_for')
    prerequisites = models.ManyToManyField('FieldCourse', blank=True, related_name='prerequisite_for')

class SubField(models.Model):
    field = models.ForeignKey(Field, on_delete=models.CASCADE, related_name='subfields')
    field_courses = models.ManyToManyField(FieldCourse, blank=False, related_name='subfields')

class Carrier(models.Model):
    login_profile = models.OneToOneField(UserLoginProfile, on_delete=models.CASCADE, related_name='carrier')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='carriers')
    subfield = models.ForeignKey(SubField, on_delete=models.CASCADE, related_name='carriers')
    pre_reg_field_courses = models.ManyToManyField(FieldCourse, blank=True, through = 'PreliminaryRegistration', related_name='carriers')

class Professor(models.Model):
    first_name = models.CharField(max_length=255, blank=False)
    last_name = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return str(self.first_name) + " " + str(self.last_name)

class Term(models.Model):
    pass

class Course(models.Model):
    field_course = models.ForeignKey(FieldCourse, on_delete=models.CASCADE, related_name = 'courses')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name = 'courses')
    subfields = models.ManyToManyField(SubField, blank=False, related_name='allowed_courses')
    departments = models.ManyToManyField(Department, blank=False, related_name='allowed_courses')
    professors = models.ManyToManyField(Professor, through = 'Teaches', related_name='courses')
    carriers = models.ManyToManyField(Carrier, through = 'Attends', related_name='registered_courses')
    term = models.ForeignKey(Term, on_delete=models.CASCADE)

class Teaches(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    percentage = models.PositiveSmallIntegerField(null=False, blank=False)

class PreliminaryRegistration(models.Model):
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    field_course = models.ForeignKey(FieldCourse, on_delete=models.CASCADE)
    carrier = models.ForeignKey(Carrier, on_delete=models.CASCADE)

class Grade(models.Model):
    pass

class Attends(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    carrier = models.ForeignKey(Carrier, on_delete=models.CASCADE)
    percentage = models.PositiveSmallIntegerField(null=False, blank=False)
    grades = models.ManyToManyField(Grade, blank=True)