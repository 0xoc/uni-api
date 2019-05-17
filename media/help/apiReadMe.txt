APIs:
-------------------------------------------------------------------------------------------------------------------------------------------------
1 - API for recieving Token:
    
    EXP: 
    curl -X POST -d "username=zahrabgh&password=12345zahra" http://127.0.0.1:8000/api-token-auth/
    
    RESULT: {"token":"df089f8170c434f0e002fd92ff965083c3432b2e"}
-------------------------------------------------------------------------------------------------------------------------------------------------
2 - API for recieving carrier basic information:
    
    EXP: 
    curl -X GET http://127.0.0.1:8000/api/v1/carrier/mini_profile/ -H 'Authorization: Token df089f8170c434f0e002fd92ff965083c3432b2e'
    
    RESULT: 

    [
        {
            "student": {
            "first_name": "سپیده",
            "last_name": "جلالی",
            "pic": "pic_folder/no-img.jpg"
            },
            "subfield": { "title": "نرم افزار", "field": "مهندسی کامپیوتر" },
            "entry_year": 1397,
            "admission_type": "روزانه",
            "total_credits_taken": 6,
            "total_credits_passed": 6,
            "average": 18
        }
    ]
-------------------------------------------------------------------------------------------------------------------------------------------------
3 - API for recieving the terms of a student:
    
    EXP:
    curl -X GET http://127.0.0.1:8000/api/v1/carrier/terms/ -H 'Authorization: Token df089f8170c434f0e002fd92ff965083c3432b2e'
    
    RESULT:

    [
        {
            "pk": 2,
            "title": "1397 نیمسال اول",
            "start_date": "1397-07-01",
            "end_date": "1397-10-30"
        },
        {
            "pk": 4,
            "title": "1398 نیمسال اول",
            "start_date": "1398-07-01",
            "end_date": "1398-10-30"
        }
    ]
-------------------------------------------------------------------------------------------------------------------------------------------------
4 - API for recieving the courses summary for a specific term and carrier:

    EXP:
    curl -X GET http://127.0.0.1:8000/api/v1/carrier/terms/1/ -H 'Authorization: Token f67877b6de83395d34bb02e5b8747501ebc71029'

    RESULT:

    [
        {
            "course_type_for_carrier": "تخصصی اجباری",
            "grade": null,
            "grade_status": null,
            "carrier_course_status": "تایید نشده",
            "course": {
            "section_number": 1,
            "grades_status": "ارسال نشده",
            "grades_average": null,
            "min_grade": null,
            "max_grade": null,
            "field_course": { "serial_number": 1, "title": "مدار الکتریکی", "credit": 3 }
            }
        },
        {
            "course_type_for_carrier": null,
            "grade": null,
            "grade_status": null,
            "carrier_course_status": "تایید نشده",
            "course": {
            "section_number": 3,
            "grades_status": "ارسال نشده",
            "grades_average": null,
            "min_grade": null,
            "max_grade": null,
            "field_course": { "serial_number": 4, "title": "مدار منطقی", "credit": 3 }
            }
        }
    ]
-------------------------------------------------------------------------------------------------------------------------------------------------
5 - API for recieving term averages:

    EXP:

    curl -X GET http://127.0.0.1:8000/api/v1/carrier/terms/gradessummary/2/ -H 'Authorization: Token b993cee51045108d01ba529a2c25e01f2e5fac97'

    RESULT:

    {
        "total_credits_taken": 6,
        "total_credits_passed": 6,
        "carrier_average": 18,
        "field_average": 17,
        "department_average": 17,
        "college_average": 18
    }
-------------------------------------------------------------------------------------------------------------------------------------------------