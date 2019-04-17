from django.db import models
from django.contrib.auth.models import User
from django_enumfield import enum
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
    title = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return str(self.title)

class Department(models.Model):
    title = models.CharField(max_length=255, blank=False)
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name='departments')

    def __str__(self):
        return str(self.title)

class DegreeType(enum.Enum):
    KAARDANI = 0
    KARSHENASI = 1
    ARSHAD = 2
    DOCTORI = 3

class Field(models.Model):
    head_department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='main_fields')
    departments = models.ManyToManyField(Department, blank=False, related_name='fields')

    title = models.CharField(max_length=255, blank=False)
    degree = enum.EnumField(DegreeType, blank=False, null=False)

    def __str__(self):
        return str(self.title)

class Credit(models.Model):
    practical_units = models.PositiveSmallIntegerField(null=False, blank=False)
    theoritical_units = models.PositiveSmallIntegerField(null=False, blank=False)

    class Meta:
        unique_together = (("practical_units", "theoritical_units"))
    
    def __str__(self):
        return str(self.practical_units)+" Practical Units and "+str(self.theoritical_units)+" Theoritical Units"

class FieldCourse(models.Model):
    corequisites = models.ManyToManyField('FieldCourse', blank=True, related_name='corequisite_for')
    prerequisites = models.ManyToManyField('FieldCourse', blank=True, related_name='prerequisite_for')

    serial_number = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255, blank=False)
    credit = models.ForeignKey(Credit, on_delete=models.CASCADE, related_name='field_courses')

    def __str__(self):
        return str(self.title) + " | " + str(self.serial_number)

class Subfield(models.Model):
    field = models.ForeignKey(Field, on_delete=models.CASCADE, related_name='subfields')
    field_courses = models.ManyToManyField(FieldCourse, blank=False, through='FieldCourseSubfield', related_name='subfields')

    title = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return str(self.title)

class FieldCourseType(enum.Enum):
    NOT_DEFINED = 0
    OMUMI = 1
    PAYE = 2
    ASLI = 3
    TAKHASOSI_EJBARI = 4
    EKHTIARI = 5

class FieldCourseSubfield(models.Model):
    field_course = models.ForeignKey(FieldCourse, on_delete=models.CASCADE)
    subfield = models.ForeignKey(Subfield, on_delete=models.CASCADE)
    suggested_term = models.PositiveSmallIntegerField(blank=True, null=True)
    type = enum.EnumField(FieldCourseType, null=False, blank=False)

    class Meta:
        unique_together = (("field_course", "subfield"))

class CarrierStatusType(enum.Enum):
    STUDYING = 0
    GRADUATED = 1
    NOT_FINISHED = 2

# class SemesterType(enum.Enum):
#     NIMSAL_AVVAL = 0
#     NIMSAL_DOVVOM = 1

class Term(models.Model):
    start_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null=False, blank=False)
    #semester = enum.EnumField(SemesterType, null=False, blank=False)

    class Meta:
        unique_together = (("start_date", "end_date"))
    
    def __str__(self):
        return "Term: "+str(self.start_date)+" to "+str(self.end_date)

class AdmissionType(enum.Enum):
    ROOZANEH = 0
    SHABANEH = 1
    MEHMAN = 2
    ENTEGHALI = 3

class Carrier(models.Model):
    login_profile = models.OneToOneField(UserLoginProfile, on_delete=models.CASCADE, related_name='carrier')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='carriers')
    subfield = models.ForeignKey(Subfield, on_delete=models.CASCADE, related_name='carriers')
    pre_reg_field_courses = models.ManyToManyField(FieldCourse, blank=True, through = 'PreliminaryRegistration', related_name='carriers')
    entry_term = models.ForeignKey(Term, on_delete=models.CASCADE, related_name='entered_carriers')
    
    id = models.IntegerField(primary_key=True)
    status = enum.EnumField(CarrierStatusType, blank=False)
    admission_type = enum.EnumField(AdmissionType, blank=False)

    def __str__(self):
        return str(self.student)+" | "+str(self.subfield)

class Professor(models.Model):
    first_name = models.CharField(max_length=255, blank=False)
    last_name = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return str(self.first_name) + " " + str(self.last_name)
    
class GenderTypeAllowed(enum.Enum):
    NOT_DEFINED = 0
    MALE = 1
    FEMALE = 2
    BOTH = 3

class DayRange(models.Model):
    start = models.TimeField(blank=False, null=False)
    end = models.TimeField(blank=False, null=False)

    class Meta:
        unique_together = (("start","end"))

    def __str__(self):
        return "Start: "+str(self.start)+" | End: "+str(self.end)    

class Day(enum.Enum):
    SATURDAY = 0
    SUNDAY = 1
    MONDAY = 2
    TUESDAY = 3
    WEDNESDAY = 4
    THURSDAY = 5
    FRIDAY = 6

class DayTime(models.Model):
    day_range = models.ForeignKey(DayRange, on_delete=models.CASCADE)
    day = enum.EnumField(Day, blank=False, null=False)

    class Meta:
        unique_together = (("day_range","day"))

    def __str__(self):
        return str(self.day_range)+" | Day: "+str(Day.get(self.day))

class WeeklySchedule(models.Model):
    day_times = models.ManyToManyField(DayTime, blank=False, related_name='weekly_schedules')

    def __str__(self):
        st = ""
        for item in self.day_times.all():
            st += str(item) + " ~ "
        return st



class Course(models.Model):
    field_course = models.ForeignKey(FieldCourse, on_delete=models.CASCADE, related_name = 'courses')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name = 'courses')
    subfields = models.ManyToManyField(Subfield, blank=False, related_name='allowed_courses')
    departments = models.ManyToManyField(Department, blank=False, related_name='allowed_courses')
    professors = models.ManyToManyField(Professor, blank=False, through = 'Teaches', related_name='courses')
    carriers = models.ManyToManyField(Carrier, blank=True, through = 'Attends', related_name='registered_courses')
    term = models.ForeignKey(Term, on_delete=models.CASCADE, related_name = 'courses')

    midterm_exam_date = models.DateTimeField(null=True, blank=True)
    final_exam_date = models.DateTimeField(null=True, blank=True)
    section_number = models.PositiveSmallIntegerField(blank=False, null=False)
    capacity = models.PositiveSmallIntegerField(blank=False, null=False)
    room_number = models.PositiveSmallIntegerField(blank=True, null=True)
    students_gender = enum.EnumField(GenderTypeAllowed, blank=False, null=False)
    weekly_schedule = models.ForeignKey(WeeklySchedule, on_delete=models.CASCADE, related_name='courses')

    class Meta:
        unique_together = (("field_course", "term", "section_number", "room_number"))

    def __str__(self):
        return str(self.field_course)+" | Section "+str(self.section_number)


class Teaches(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    percentage = models.PositiveSmallIntegerField(null=False, blank=False)

class PreliminaryRegistration(models.Model):
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    field_course = models.ForeignKey(FieldCourse, on_delete=models.CASCADE)
    carrier = models.ForeignKey(Carrier, on_delete=models.CASCADE)

class Grade(models.Model):
    out_of_twenty = models.FloatField(null=False, blank=False, default=20.0) # az 20 nomre
    value = models.FloatField(null=False, blank=False, default=0.0)
    base_value = models.FloatField(null=False, blank=False, default=20.0)
    date_examined = models.DateField(null=True, blank=True)
    title = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.title

class CourseStatusType(enum.Enum):
    NOT_DEFINED = 0
    FAILED = 1
    PASSED = 2

class CourseApprovalState(enum.Enum):
    NOT_DEFINED = 0
    APPROVED = 1
    NOT_APPROVED = 2

class Attends(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    carrier = models.ForeignKey(Carrier, on_delete=models.CASCADE)
    grades = models.ManyToManyField(Grade, blank=True)

    status = enum.EnumField(CourseStatusType, null=False, blank=False)
    approved = enum.EnumField(CourseApprovalState, null=False, blank=False)

