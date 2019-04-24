APIs:

- API for recieving Token:
    EXP: 
    curl -X POST -d "username=zahrabgh&password=12345zahra" http://127.0.0.1:8000/api-token-auth/
    RESULT: {"token":"df089f8170c434f0e002fd92ff965083c3432b2e"}

- API for recieving carrier basic information:
    EXP: 
    curl -X GET http://127.0.0.1:8000/api/v1/carrier/mini_profile/ -H 'Authorization: Token df089f8170c434f0e002fd92ff965083c3432b2e'
    RESULT: 

    [{  "student":
            {"first_name":"Zahra","last_name":"Bagheri","pic":"pic_folder/caf1c5b054c0423f3b8c38b4af3c96cf.jpg"},
        "subfield":
            {"title":"IT Engineering","field":"IT Engineering"},
        "entry_year":1389,
        "admission_type":"SHABANEH"
    }]
