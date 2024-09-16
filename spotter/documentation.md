INTRODUCTION:
    This folder contains all needed files for this program to run successfully.
    Make sure you are in the same directory with the manage.py file.
    Run: python manage.py runserver ( Python version must be 3.10 or above )
    Server will be accessible on port 8000. Please ensure the port is not busy

END POINTS:
    *** Please take note of the request type***
    *** All date_uploaded are in timestamp***

    FIRST THING TO DO IS GENERATE THE JWT TOKEN:
        *** Use the credentials below to generate tokens that works for this REST API***
        REQUEST: curl -X POST -d "username=spotter&password=spotter" http://127.0.0.1:8000/api/token/
        
        Response:
            {
                "refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcyNjU2Njk5NCwiaWF0IjoxNzI2NDgwNTk0LCJqdGkiOiJkNjAzOTljNjhmYTA0YmQzYjE3NzE3MGQxMWIzZTZiNiIsInVzZXJfaWQiOjF9.x4XPRZ2NRW68kWhIqEa9BRuamC7Cg9OPil5xvqR36u4",
                
                "access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI2NDg0MTk0LCJpYXQiOjE3MjY0ODA1OTQsImp0aSI6Ijk0NDBmMmIzOTYwNDQyNzFiMDgzMDhhYWRjZDA3MGNmIiwidXNlcl9pZCI6MX0.Dkeol4UxupxxFbrqBqiC8rjieYM0i0OS-Wtz_Abrhuo"
            }
        
        The "refresh" field will be used by the client to generate a new "access" token after it expires.
            
            REQUEST: curl -X POST -d "username=spotter&password=spotter" http://127.0.0.1:8000/api/token/

            Response Example: 
            {
                "refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcyNjU2Njk5NCwiaWF0IjoxNzI2NDgwNTk0LCJqdGkiOiJkNjAzOTljNjhmYTA0YmQzYjE3NzE3MGQxMWIzZTZiNiIsInVzZXJfaWQiOjF9.x4XPRZ2NRW68kWhIqEa9BRuamC7Cg9OPil5xvqR36u4"
            }

        For this system, the access token expires after 60 minutes. This can be tuned in the settings.py file to a shorter time. Every request made afterwards must have the "access" token included in the request's header "Authorization" field to be precise.
    
    GET ALL BOOKS:
        Request:
            curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI2NDg0MTk0LCJpYXQiOjE3MjY0ODA1OTQsImp0aSI6Ijk0NDBmMmIzOTYwNDQyNzFiMDgzMDhhYWRjZDA3MGNmIiwidXNlcl9pZCI6MX0.Dkeol4UxupxxFbrqBqiC8rjieYM0i0OS-Wtz_Abrhuo" http://127.0.0.1:8000/books

        Response:
            {
                "status":1,"message":"Found 8 record!","data":"[{'id': 1, 'name': 'Test Book 6', 'price': 100, 'published_date': 'July 12, 2020', 'category': 'Music', 'date_uploaded': 1719442305}, {'id': 2, 'name': 'Test Book 1', 'price': 100, 'published_date': 'July 12, 2020', 'category': 'Music', 'date_uploaded': 1719442305}, {'id': 3, 'name': 'Test Book 2', 'price': 100, 'published_date': 'July 12, 2020', 'category': 'Music', 'date_uploaded': 1719442305}, {'id': 4, 'name': 'Test Book 3', 'price': 100, 'published_date': 'July 12, 2020', 'category': 'Music', 'date_uploaded': 1719442305}, {'id': 5, 'name': 'Sci. Book 1', 'price': 100, 'published_date': 'July 12, 2020', 'category': 'Science', 'date_uploaded': 1719442305}, {'id': 6, 'name': 'Sci. Book 2', 'price': 100, 'published_date': 'July 12, 2020', 'category': 'Science', 'date_uploaded': 1719442305}, {'id': 7, 'name': 'Sci. Book 3', 'price': 100, 'published_date': 'July 12, 2020', 'category': 'Science', 'date_uploaded': 1719442305}, {'id': 8, 'name': 'Sci. Book 4', 'price': 100, 'published_date': 'July 12, 2020', 'category': 'Science', 'date_uploaded': 1719442305}]"
            }

    GET A SPECIFIC BOOKS ( id:3 for example):
        Request:
            curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI2NDg0MTk0LCJpYXQiOjE3MjY0ODA1OTQsImp0aSI6Ijk0NDBmMmIzOTYwNDQyNzFiMDgzMDhhYWRjZDA3MGNmIiwidXNlcl9pZCI6MX0.Dkeol4UxupxxFbrqBqiC8rjieYM0i0OS-Wtz_Abrhuo" http://127.0.0.1:8000/books/3

        Response:
            {
                "status":1,"message":"Found 1 record!","data":"[{'id': 3, 'name': 'Test Book 2', 'price': 100, 'published_date': 'July 12, 2020', 'category': 'Music', 'date_uploaded': 1719442305}]"
            }
    
    ADD A NEW BOOK:
        Request:
            curl -X POST -d "name=Test Book 9&price=100&published_date=July 12, 2020&category=Music&date_uploaded=1719442305" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI2NDg0MTk0LCJpYXQiOjE3MjY0ODA1OTQsImp0aSI6Ijk0NDBmMmIzOTYwNDQyNzFiMDgzMDhhYWRjZDA3MGNmIiwidXNlcl9pZCI6MX0.Dkeol4UxupxxFbrqBqiC8rjieYM0i0OS-Wtz_Abrhuo" http://127.0.0.1:8000/books
        
        Response:
            {
                "status":1,"message":"New record added successfully!","data":"[{'name': 'Test Book 9', 'price': 100, 'published_date': 'July 12, 2020', 'category': 'Music', 'date_uploaded': 1719442305}]"
            }
    
    DELETE BOOK:
        Request:
            curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI2NDg0MTk0LCJpYXQiOjE3MjY0ODA1OTQsImp0aSI6Ijk0NDBmMmIzOTYwNDQyNzFiMDgzMDhhYWRjZDA3MGNmIiwidXNlcl9pZCI6MX0.Dkeol4UxupxxFbrqBqiC8rjieYM0i0OS-Wtz_Abrhuo" -X DELETE http://127.0.0.1:8000/books/1
        
        Response:
            {
                "status":1,"message":"removed one record!","data":"1"
            } 
    
    ADD A NEW AUTHOR:
        Request:
            curl -d "author_title=Dr.&author_name=Akin Thompson&author_gender=Male&author_book_id=5&date_uploaded=1716642305" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI2NDg0MTk0LCJpYXQiOjE3MjY0ODA1OTQsImp0aSI6Ijk0NDBmMmIzOTYwNDQyNzFiMDgzMDhhYWRjZDA3MGNmIiwidXNlcl9pZCI6MX0.Dkeol4UxupxxFbrqBqiC8rjieYM0i0OS-Wtz_Abrhuo" http://127.0.0.1:8000/authors
        
        Response:
            {
                "status":1,"message":"New record added successfully!","data":"[{'id': 8, 'author_title': 'Dr.', 'author_name': 'Akin Thompson', 'author_gender': 'Female', 'author_book_id': 3, 'date_uploaded': 1716642305}]"
            }

    GET ALL AUTHORS:
        Request:
            curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI2NDg0MTk0LCJpYXQiOjE3MjY0ODA1OTQsImp0aSI6Ijk0NDBmMmIzOTYwNDQyNzFiMDgzMDhhYWRjZDA3MGNmIiwidXNlcl9pZCI6MX0.Dkeol4UxupxxFbrqBqiC8rjieYM0i0OS-Wtz_Abrhuo" http://127.0.0.1:8000/authors
        
        Response:
            {
                "status":1,"message":"Found 8 record!","data":"[{'id': 1, 'author_title': 'Dr.', 'author_name': 'Emmanuella Thompson', 'author_gender': 'Female', 'author_book_id': 3, 'date_uploaded': 1716642305}, {'id': 2, 'author_title': 'Dr.', 'author_name': 'Daniel J. Jones', 'author_gender': 'Male', 'author_book_id': 3, 'date_uploaded': 1716642305}, {'id': 3, 'author_title': 'Dr.', 'author_name': 'James Kirk', 'author_gender': 'Male', 'author_book_id': 5, 'date_uploaded': 1716642305}, {'id': 4, 'author_title': 'Dr.', 'author_name': 'Akin Thompson', 'author_gender': 'Female', 'author_book_id': 3, 'date_uploaded': 1716642305}, {'id': 5, 'author_title': 'Dr.', 'author_name': 'Akin Thompson', 'author_gender': 'Female', 'author_book_id': 3, 'date_uploaded': 1716642305}, {'id': 6, 'author_title': 'Dr.', 'author_name': 'Akin Thompson', 'author_gender': 'Female', 'author_book_id': 3, 'date_uploaded': 1716642305}, {'id': 7, 'author_title': 'Dr.', 'author_name': 'Akin Thompson', 'author_gender': 'Female', 'author_book_id': 3, 'date_uploaded': 1716642305}, {'id': 8, 'author_title': 'Dr.', 'author_name': 'Akin Thompson', 'author_gender': 'Female', 'author_book_id': 3, 'date_uploaded': 1716642305}]"
            } 

    GET A SPECIFIC AUTHOR:
        Request:
            curl -d "author_title=Dr.&author_name=Emmanuela Thompson&author_gender=Female&author_book_id=3&date_uploaded=1716642305" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI2NDg1OTY1LCJpYXQiOjE3MjY0ODIzNjUsImp0aSI6ImUwNWQ5MzE5MWMzZTQ4MTQ5MWFiZTJlYjQ4NzZmNWY4IiwidXNlcl9pZCI6MX0.xqMFhe_1bG8r4QuSgh4Xl1zsoXm5XHYuGMRl_LlhDzs" http://127.0.0.1:8000/authors/3
        
        Response:
            {
                "status":1,"message":"Found 1 record!","data":"[{'id': 1, 'author_title': 'Dr.', 'author_name': 'Emmanuella Thompson', 'author_gender': 'Female', 'author_book_id': 3, 'date_uploaded': 1716642305}]"
            }
    
    DELETE AUTHOR:
        Request:
            curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI2NDg0MTk0LCJpYXQiOjE3MjY0ODA1OTQsImp0aSI6Ijk0NDBmMmIzOTYwNDQyNzFiMDgzMDhhYWRjZDA3MGNmIiwidXNlcl9pZCI6MX0.Dkeol4UxupxxFbrqBqiC8rjieYM0i0OS-Wtz_Abrhuo" -X DELETE http://127.0.0.1:8000/authors/1
        
        Response:
            {
                "status":1,"message":"removed one record!","data":"1"
            } 
    
    GET FAVOURITES:
        Request:
            curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI2NDg1OTY1LCJpYXQiOjE3MjY0ODIzNjUsImp0aSI6ImUwNWQ5MzE5MWMzZTQ4MTQ5MWFiZTJlYjQ4NzZmNWY4IiwidXNlcl9pZCI6MX0.xqMFhe_1bG8r4QuSgh4Xl1zsoXm5XHYuGMRl_LlhDzs" http://127.0.0.1:8000/favourites/1
        
        Response:
            {
                "status":1,"message":"Found 2 record!","data":"[{'id': 1, 'user_id': 1, 'book_id': 3, 'date_uploaded': 1719442305}, {'id': 2, 'user_id': 1, 'book_id': 1, 'date_uploaded': 1719442305}]"
            }
    
    ADD FAVOURITES:
        Request:
            curl -X POST -d "user_id=1&book_id=3&date_updated=1719442305" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI2NDg1OTY1LCJpYXQiOjE3MjY0ODIzNjUsImp0aSI6ImUwNWQ5MzE5MWMzZTQ4MTQ5MWFiZTJlYjQ4NzZmNWY4IiwidXNlcl9pZCI6MX0.xqMFhe_1bG8r4QuSgh4Xl1zsoXm5XHYuGMRl_LlhDzs" http://127.0.0.1:8000/favourites/add
        
        Response:
            {
                "status":1,"message":"Found 2 record!","data":"[{'id': 1, 'user_id': 1, 'book_id': 3, 'date_uploaded': 1719442305}, {'id': 2, 'user_id': 1, 'book_id': 1, 'date_uploaded': 1719442305}]"
            }
    
    REMOVE FAVOURITES ( id:2 for example):
        Request:
            curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.    eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI2NDkzODY1LCJpYXQiOjE3MjY0OTAyNjUsImp0aSI6ImEwMzhlNWI3M2IwOTQ3N2M5ZmMzMDMyZWI1MWJiYTNmIiwidXNlcl9pZCI6MX0.URg-iW09JfHFcUJ18mscqZCshhtis56OB_4gJK0wziE" -X DELETE http://127.0.0.1:8000/favourites/remove/2
    
        Response:
            {
                "status":1,"message":"removed one record!","data":"1"
            }
    
    RECOMMEND:
        Request:
            curl -X POST -d "category=Music" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI2NDkzODY1LCJpYXQiOjE3MjY0OTAyNjUsImp0aSI6ImEwMzhlNWI3M2IwOTQ3N2M5ZmMzMDMyZWI1MWJiYTNmIiwidXNlcl9pZCI6MX0.URg-iW09JfHFcUJ18mscqZCshhtis56OB_4gJK0wziE" http://127.0.0.1:8000/recommend
        
        Response:
            {
                "status":1,"message":"Found 5 record(s)!","data":"[{'id': 1, 'name': 'Test Book 6', 'price': 100, 'published_date': 'July 12, 2020', 'category': 'Music', 'date_uploaded': 1719442305}, {'id': 3, 'name': 'Test Book 2', 'price': 100, 'published_date': 'July 12, 2020', 'category': 'Music', 'date_uploaded': 1719442305}, {'id': 2, 'name': 'Test Book 1', 'price': 100, 'published_date': 'July 12, 2020', 'category': 'Music', 'date_uploaded': 1719442305}, {'id': 4, 'name': 'Test Book 3', 'price': 100, 'published_date': 'July 12, 2020', 'category': 'Music', 'date_uploaded': 1719442305}, {'id': 9, 'name': 'Test Book 9', 'price': 100, 'published_date': 'July 12, 2020', 'category': 'Music', 'date_uploaded': 1719442305}]"
            }
