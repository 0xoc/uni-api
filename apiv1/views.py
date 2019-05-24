from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from users.models import *
from users.utils import *
from rest_framework.permissions import IsAuthenticated


class CarrierMiniProfileListView(ListAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = CarrierDetailSerializer

    def get_queryset(self):
        return Carrier.objects.filter(pk=self.request.user.user_login_profile.carrier.pk)


class CarrierTermsListView(ListAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = TermDetailSerializer

    def get_queryset(self):
        return self.request.user.user_login_profile.carrier.terms


class CarrierTermDetailsListView(ListAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = AttendSerializer

    def get_queryset(self):
        term_id = self.kwargs['term_id']
        return Attend.objects.filter(course__term__pk=term_id, carrier=self.request.user.user_login_profile.carrier)


class TermSummaryView(APIView):

    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):

        car = self.request.user.user_login_profile.carrier
        term_id = int(self.kwargs['term_id'])

        carrier_attends = list(filter(lambda attend: attend.course.term.pk == term_id
                                      and attend.carrier == car and not attend.deleted_by_carrier, Attend.objects.all()))

        field_attends = list(filter(lambda attend: attend.course.term.pk == term_id
                                    and attend.carrier.subfield.field == car.subfield.field
                                    and not attend.grade == None, Attend.objects.all()))
        department_attends = list(filter(lambda attend: attend.course.term.pk == term_id
                                         and attend.carrier.subfield.field.head_department == car.subfield.field.head_department
                                         and not attend.grade == None, Attend.objects.all()))
        college_attends = list(filter(lambda attend: attend.course.term.pk == term_id
                                      and attend.carrier.subfield.field.head_department.college == car.subfield.field.head_department.college
                                      and not attend.grade == None, Attend.objects.all()))

        mydata = {
            'total_credits_taken': 0,
            'total_credits_passed': 0,
            'carrier_average': 0.0,
            'field_average': 0.0,
            'department_average': 0.0,
            'college_average': 0.0
        }

        mydata["total_credits_taken"] = sum(
            list(map(lambda x: x.course.field_course.credit, carrier_attends)))

        carrier_attends = list(
            filter(lambda attend: attend.course.are_grades_approved, carrier_attends))
        temp = list(map(lambda x: (x.course.field_course.credit,
                                   x.course.field_course.credit * x.grade), carrier_attends))

        total_credits = sum(list(map(lambda x: x[0], temp)))
        if total_credits == 0:
            mydata["carrier_average"] = None
        else:
            mydata["carrier_average"] = sum(
                list(map(lambda x: x[1], temp))) / total_credits

        carrier_attends = list(filter(lambda attend: attend.grade_status == get_key(
            GradeState, GradeState.PASSED), carrier_attends))
        mydata["total_credits_passed"] = sum(
            list(map(lambda x: x.course.field_course.credit, carrier_attends)))

        temp = list(map(lambda x: (x.course.field_course.credit,
                                   x.course.field_course.credit * x.grade), field_attends))
        total_credits = sum(list(map(lambda x: x[0], temp)))
        if total_credits == 0:
            mydata["field_average"] = None
        else:
            mydata["field_average"] = sum(
                list(map(lambda x: x[1], temp))) / total_credits

        temp = list(map(lambda x: (x.course.field_course.credit,
                                   x.course.field_course.credit * x.grade), department_attends))
        total_credits = sum(list(map(lambda x: x[0], temp)))
        if total_credits == 0:
            mydata["department_average"] = None
        else:
            mydata["department_average"] = sum(
                list(map(lambda x: x[1], temp))) / total_credits

        temp = list(map(lambda x: (x.course.field_course.credit,
                                   x.course.field_course.credit * x.grade), college_attends))
        total_credits = sum(list(map(lambda x: x[0], temp)))
        if total_credits == 0:
            mydata["college_average"] = None
        else:
            mydata["college_average"] = sum(
                list(map(lambda x: x[1], temp))) / total_credits

        results = TermSummarySerializer(mydata, many=False).data
        return Response(results)


class CarrierPreRegistrationView(ListAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = PreRegistrationSerializer

    def get_queryset(self):
        term_id = self.kwargs['term_id']
        return PreliminaryRegistration.objects.filter(term__pk=term_id, carrier=self.request.user.user_login_profile.carrier)