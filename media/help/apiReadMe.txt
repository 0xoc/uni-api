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
            "first_name": "Zahra",
            "last_name": "Bagheri",
            "pic": "pic_folder/caf1c5b054c0423f3b8c38b4af3c96cf.jpg"
        },
            "subfield": { "title": "IT Engineering", "field": "IT Engineering" },
            "entry_year": 1389,
            "admission_type": "SHABANEH"
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
            "title": "1396-SemesterA",
            "start_date": "1396-07-01",
            "end_date": "1396-11-01"
        },
        {
            "pk": 1,
            "title": "1397-SemesterB",
            "start_date": "1397-12-01",
            "end_date": "1398-04-31"
        }
    ]

-------------------------------------------------------------------------------------------------------------------------------------------------
4 - API for recieving the courses summary for a specific term and carrier:

    EXP:
    curl -X GET http://127.0.0.1:8000/api/v1/carrier/terms/1/ -H 'Authorization: Token f67877b6de83395d34bb02e5b8747501ebc71029'

    RESULT:

    [
        {
            "course_type_for_carrier": "TAKHASOSI_EJBARI",
            "grade": 11.0,
            "grade_status": "PASSED",
            "carrier_course_status": "NOT_DEFINED",
            "course": {
            "section_number": 1,
            "grades_status": "NOT_SENT",
            "grades_average": null,
            "min_grade": null,
            "max_grade": null,
            "field_course": { "serial_number": 1, "title": "OS LAB", "credit": 1 }
            }
        },
        {
            "course_type_for_carrier": null,
            "grade": 0.0,
            "grade_status": "FAILED",
            "carrier_course_status": "NOT_DEFINED",
            "course": {
            "section_number": 1,
            "grades_status": "NOT_SENT",
            "grades_average": null,
            "min_grade": null,
            "max_grade": null,
            "field_course": { "serial_number": 2, "title": "DB LAB", "credit": 1 }
            }
        }
    ]
-------------------------------------------------------------------------------------------------------------------------------------------------