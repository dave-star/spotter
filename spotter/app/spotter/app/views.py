from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from .engine import database as db
from .engine import utility as ut

class Home ( APIView ):
    authentication_classes = [JWTAuthentication]
    permision_classes = [IsAuthenticated]
    cols = [
        ['id', 'name', 'price', 'published_date', 'category', 'date_uploaded'],
        ['id', 'author_title', 'author_name', 'author_gender', 'author_book_id', 'date_uploaded'],
        ['id', 'user_id', 'book_id', 'date_uploaded'],
        ['id', 'full_name', 'email', 'password', 'date_uploaded']
    ]
    
    def get ( self, request, id = '0' ):
        msg = {}
        
        # connect to the database
        conn    = db.Connect ( )
        
        # prepare database for execution
        cursor  = conn.cursor ( )

        if id.isdigit ( ):
            
            # Get the path the client followed
            url = request.path
            if url.startswith ( '/books' ):
                msg = ut.GetRecord ( cursor, id, 1, self.cols[0], conn, url, request )
            elif url.startswith ( '/authors' ):
                msg = ut.GetRecord ( cursor, id, 1, self.cols[1], conn, url, request )
            elif url.startswith ( '/favourites' ):
                msg = ut.GetRecord ( cursor, id, 1, self.cols[2], conn, url, request )
            else:
                msg['status'] = 403
                msg['message'] = f"Your request was rejected by the server!"
        else:
            msg['status'] = 0
            msg['message'] = f"Your request was rejected by the server!"

        # Run queries and free connection to database
        conn.commit ( )
        conn.close ( )

        # Return response to the client
        return Response ( msg )
    
    def put ( self, request, id = '0' ):
        msg = {}
        
        # connect to the database
        conn    = db.Connect ( )
        
        # prepare database for execution
        cursor  = conn.cursor ( )

        # Filter user input for any malicious input
        data = ut.Filter ( request.data )
        
        # Get the path the client followed
        url = request.path
        if url.startswith ( '/books' ):
            data['id'] = id
            msg = ut.Save ( cursor, data, 2, 'books', self.cols[0], conn )
        elif url.startswith ( '/authors' ):
            data['id'] = id
            msg = ut.Save ( cursor, data, 2, 'authors', self.cols[1], conn )
        
        conn.close ( )
        return Response ( msg )
    
    def delete ( self, request, id = '0' ):
        msg = {}
        
        # connect to the database
        conn    = db.Connect ( )
        
        # prepare database for execution
        cursor  = conn.cursor ( )

        if id.isdigit ( ):
            
            # Get the path the client followed
            url = request.path
            if url.startswith ( '/books' ):
                msg = ut.DeleteRecord ( cursor, id, 1, 'books', self.cols[0], conn, url )
            elif url.startswith ( '/authors' ):
                msg = ut.DeleteRecord ( cursor, id, 1, 'authors', self.cols[1], conn, url )
            elif url.startswith ( '/favourites/remove' ):
                msg = ut.DeleteRecord ( cursor, id, 1, 'favourites', self.cols[2], conn, url )

        else:
            msg['status'] = 0
            msg['message'] = f"Your request was rejected by the server!"

        # Run queries and free connection to database
        conn.commit ( )
        conn.close ( )

        # Return response to the client
        return Response ( msg )
                 
    def post ( self, request, id = '0' ):
        # connect to the database
        conn    = db.Connect ( )
        
        # prepare database for execution
        cursor  = conn.cursor ( )
        
        # Filter user input for any malicious input
        data = ut.Filter ( request.data )
        
        # Get the path the client followed
        url = request.path
        
        if url == '/books':
            msg = ut.Save ( cursor, data, 1, 'books', self.cols[0], conn )
        
        elif url == '/authors':
            msg = ut.Save ( cursor, data, 1, 'authors', self.cols[1], conn )
        
        elif url == '/favourites/add':
            msg = ut.Save ( cursor, data, 1, 'favourites', self.cols[2], conn )
        
        elif url == '/recommend':
            msg = {}
            msg['status'] = 1
            record = db.Select ( cursor, "books", f"category = '{data['category']}' ORDER BY RANDOM() LIMIT 5", self.cols[0] )
            msg['message'] = f"Found {len ( record )} record(s)!"
            msg['data'] = str ( record )
        
        elif url == '/register':
            msg = {}
            record = db.SelectRow ( cursor, 'users', f"email = '{data['email']}'" )
            if record == 0:
                msg = ut.Save ( cursor, data, 1, 'users', self.cols[3], conn )
            else:
                msg['status'] = 0
                msg['message'] = f"Email address already exist!"
        
        elif url == '/login':
            msg = {}
            password = ut.Hash ( data['password'] )
            msg['status'] = 1
            record = db.Select ( cursor, 'users', f"email = '{data['email']}' and password='{password}'", self.cols[3] )
            if len ( record ):
                msg['message'] = f"Found {len ( record )} record(s)!"
                msg['data'] = str ( record )
            else:
                msg['status'] = 0
                msg['message'] = f"Invalid email address or password!"

        conn.close ( )

        # Return response to the client
        return Response ( msg )