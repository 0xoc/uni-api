from django.db import models
from django.contrib.auth.models import User
from django_enumfield import enum
from django_jalali.db import models as jmodels
from .utils import *

class UserLoginProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_login_profile')

    # todo: other login info

    def __str__(self):
        return str(self.user)

class Student(models.Model):
    first_name = models.CharField(max_length=255, blank=False)
    last_name = models.CharField(max_length=255, blank=False)
    pic = models.ImageField(upload_to = 'pic_folder/', default = 'pic_folder/no-img.jpg', validators=[validate_image_size])

    def __str__(self):
        return str(self.first_name) + " " + str(self.last_name)

class College(models.Model):
    title = models.CharField(max_length=255, blank=False, unique=True)

    def __str__(self):
        return str(self.title)

class Department(models.Model):
    title = models.CharField(max_length=255, blank=False)
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name='departments')

    class Meta:
        unique_together = (("title", "college"))

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

    class Meta:
        unique_together = (("head_department", "title", "degree"))

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
    field_courses = models.ManyToManyField(FieldCourse, blank=False, through='FieldCourseSubfieldRelation', related_name='subfields')

    title = models.CharField(max_length=255, blank=False)

    class Meta:
        unique_together = (("field", "title"))

    def __str__(self):
        return str(self.title)

class FieldCourseType(enum.Enum):
    NOT_DEFINED = 0
    OMUMI = 1
    PAYE = 2
    ASLI = 3
    TAKHASOSI_EJBARI = 4
    EKHTIARI = 5

class FieldCourseSubfieldRelation(models.Model):
    field_course = models.ForeignKey(FieldCourse, on_delete=models.CASCADE)
    subfield = models.ForeignKey(Subfield, on_delete=models.CASCADE)
    suggested_term = models.PositiveSmallIntegerField(blank=True, null=True)
    course_type = enum.EnumField(FieldCourseType, null=False, blank=False)

    class Meta:
        unique_together = (("field_course", "subfield"))

    def __str__(self):
        return ("[ "+str(self.field_course) + " ] for [ " + str(self.subfield) + " ] is [ " 
            + get_key(FieldCourseType, self.course_type) + " ]")

class CarrierStatusType(enum.Enum):
    STUDYING = 0
    GRADUATED = 1
    NOT_FINISHED = 2

class Term(models.Model):
    objects = jmodels.jManager()
    start_date = jmodels.jDateField(null=False, blank=False)
    end_date = jmodels.jDateField(null=False, blank=False)

    @property
    def title(self):
        if self.start_date.month > self.end_date.month:
            return str(self.start_date.year) + "-SemesterB"
        else:
            return str(self.start_date.year) + "-SemesterA"

    class Meta:
        unique_together = (("start_date", "end_date"))
    
    def __str__(self):
        return "Term: "+str(self.start_date)+" to "+str(self.end_date) + " | " + self.title

    def __init__(self, *args, **kwargs):
        super(Term, self).__init__(* args, **kwargs)
        if self.start_date is not None:
            self.old_title = self.title
        else:
            self.old_title = " "

    def clean(self):
        if (self.end_date < self.start_date) or (self.end_date.year - self.start_date.year > 1):
            raise ValidationError("Invalid Term interval!")
        elif self.title != self.old_title and self.title in list(map(lambda x: x.title, Term.objects.all())):
            raise ValidationError("a term with the title <%s> is already defined! Detail: <%s>" % (self.title, str(self)))
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super(Term, self).save(*args, **kwargs)

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

    @property
    def terms(self):
        carrier_terms = list(map(lambda x: x.term, self.registered_courses.all()))
        carrier_terms = list(set(carrier_terms))
        carrier_terms.sort(key = lambda x: x.title)
        return carrier_terms

    @property
    def entry_year(self):
        return self.terms[0].start_date.year

    id = models.IntegerField(primary_key=True)
    status = enum.EnumField(CarrierStatusType, blank=False)
    admission_type_num = enum.EnumField(AdmissionType, blank=False)

    @property
    def admission_type(self):
        return get_key(AdmissionType, self.admission_type_num)

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

class Course(models.Model):
    field_course = models.ForeignKey(FieldCourse, on_delete=models.CASCADE, related_name = 'courses')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name = 'courses')
    subfields = models.ManyToManyField(Subfield, blank=True, related_name='allowed_courses', verbose_name='Subfields allowed to register the course')
    departments = models.ManyToManyField(Department, blank=True, related_name='allowed_courses', verbose_name='Departments allowed to register the course')
    professors = models.ManyToManyField(Professor, blank=False, through = 'Teach', related_name='courses')
    carriers = models.ManyToManyField(Carrier, blank=True, through = 'Attend', related_name='registered_courses')
    term = models.ForeignKey(Term, on_delete=models.CASCADE, related_name = 'courses')

    objects = jmodels.jManager()
    midterm_exam_date = jmodels.jDateTimeField(null=True, blank=True)
    final_exam_date = jmodels.jDateTimeField(null=True, blank=True)
    section_number = models.PositiveSmallIntegerField(blank=False, null=False)
    capacity = models.PositiveSmallIntegerField(blank=False, null=False)
    room_number = models.PositiveSmallIntegerField(blank=True, null=True)
    students_gender = enum.EnumField(GenderTypeAllowed, blank=False, null=False, verbose_name='Genders allowed to register the course')
    weekly_schedule = models.ManyToManyField(DayTime, blank=False,  through = 'DayTimeCourseRelation', related_name='courses')

    class Meta:
        unique_together = (("field_course", "term", "section_number", "room_number"))

    def __str__(self):
        return "ID: "+str(self.field_course)+" | Section: "+str(self.section_number)

class DayTimeCourseRelation(models.Model):
    day_time = models.ForeignKey(DayTime, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("day_time","course"))
    
    def __str__(self):
        return "Course: [ "+str(self.course)+" ]  Time: [ "+str(self.day_time)+" ]"

class Teach(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    percentage = models.PositiveSmallIntegerField(null=False, blank=False)

    def __str__(self):
        return "[ "+str(self.professor) + " ] teaches [ " + str(self.course) +" ]"

class PreliminaryRegistration(models.Model):
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    field_course = models.ForeignKey(FieldCourse, on_delete=models.CASCADE)
    carrier = models.ForeignKey(Carrier, on_delete=models.CASCADE)

    def __str__(self):
        return "Preregistration of [ "+str(self.carrier)+" ] in [ "+str(self.field_course)+" ]"

class CourseStatusType(enum.Enum):
    NOT_DEFINED = 0
    FAILED = 1
    PASSED = 2
    DELETED = 3

class CourseApprovalState(enum.Enum):
    NOT_DEFINED = 0
    APPROVED = 1
    NOT_APPROVED = 2

class Attend(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    carrier = models.ForeignKey(Carrier, on_delete=models.CASCADE)
    status = enum.EnumField(CourseStatusType, null=False, blank=False)
    approved = enum.EnumField(CourseApprovalState, null=False, blank=False)

    class Meta:
        unique_together = (("course","carrier"))

    def __str__(self):
        return "[ "+str(self.carrier) + " ] attends [ " + str(self.course) +" ]"
    

class Grade(models.Model):
    objects = jmodels.jManager()
    out_of_twenty = models.FloatField(null=False, blank=False, default=20.0) # az 20 nomre
    value = models.FloatField(null=False, blank=False, default=0.0)
    base_value = models.FloatField(null=False, blank=False, default=20.0)
    date_examined = jmodels.jDateField(null=True, blank=True)
    title = models.CharField(max_length=255, blank=True)
    attend = models.ForeignKey(Attend, on_delete=models.CASCADE, related_name="grades")

    def __str__(self):
        return self.title