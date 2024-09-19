import time
from . import database as db
import hashlib

def Filter ( data ):
    new_data = {}
    for key in data.keys ( ):
        new_data[key] = data[key].replace ( "'", "&apos;" )
    
    return new_data

def PrepareQuery ( data, columns, type_ ):
    if type_ == 1:
        query = '(' + ','.join ( columns ) + ') VALUES ('

        for keys in data.keys ( ):
            query += f"'{data[keys]}',"
        
        query = query[0: len ( query ) - 1]
        query += ')'
    elif type_ == 2:
        query = ''
        for keys in data.keys ( ):
            if keys != 'id':
                query += f"{keys}='{data[keys]}',"
        
        query = query[0: len ( query ) - 1]
        
    return query

def GetRecord ( cursor, id, type_, cols, conn, url, request ):
    msg = {}

    if url.startswith ( '/books' ) or url.startswith ( '/authors' ) or url.startswith ( '/favourites' ):
        id = int ( id )
        if url.startswith ( '/books' ):
            table = 'books'
        elif url.startswith ( '/authors' ):
            table = 'authors'
        elif url.startswith ( '/favourites' ):
            table = 'favourites'
        
        # Add the recorded data to the message sent to the client
        if id == 0:
            query = request.GET.get ( 'search' )
            if query != None:
                query = Filter ( {'query': query} )
            
            if query != None:
                record = db.SelectFilter ( cursor, table, f"1", cols, query )
            else:
                record = db.Select ( cursor, table, f"1", cols )
        else:
            if table == 'favourites':
                record = db.Select ( cursor, table, f"user_id = {id}", cols )
            else:
                record = db.Select ( cursor, table, f"id = {id}", cols )

        if len ( record ):
            msg['status'] = 1
            msg['message'] = f"Found {len ( record )} record!"
            msg['data'] = str ( record )
        else:
            msg['status'] = 0
            msg['message'] = f"No record was found!"
    
    conn.commit ( )
    return msg

def Hash ( string ):
    hash_object = hashlib.sha256(string.encode('utf-8'))  
    hex_dig = hash_object.hexdigest()

    return hex_dig

def DeleteRecord ( cursor, id, type_, table, cols, conn, url ):
    msg = {}

    if url.startswith ( '/books' ) or url.startswith ( '/authors' ) or url.startswith ( '/favourites/remove' ):
        id = int ( id )

        # Delete the record data requested
        if id != 0:
            record = db.SelectRow ( cursor, table, f"id = {id}" )
            if record:
                record = db.Delete ( cursor, table, f"id = {id}" )

        if record:
            msg['status'] = 1
            msg['message'] = f"removed one record!"
            msg['data'] = str ( record )
        else:
            msg['status'] = 0
            msg['message'] = f"No record was found!"
    
    conn.commit ( )
    return msg

def Save ( cursor, data, type_, table, xcols, conn ):
    msg = {}
    cols = xcols.copy ( )
    
    if cols[0] == 'id':
        cols.pop ( 0 )
    
    if table == 'books':
        # Check books table for any book with the same name
        count = db.SelectRow ( cursor, table, f"name = '{data['name']}'" )
    elif table == 'authors':
        # Check books table if the author_book_id exist
        count = db.SelectRow ( cursor, 'books', f"id = '{data['author_book_id']}'" ) 
        if count == 0:
            count = -1
        elif type_ != 2:
            # count = db.SelectRow ( cursor, 'authors', f"author_book_id = '{data['author_book_id']}'" )
            # if count != 0:
            #     count = -2
            # else:
            #     count = 1
            count = 1

    elif table == 'favourites':
        # Check favourites table for any existing item
        count = db.SelectRow ( cursor, table, f"book_id = '{data['book_id']}' AND user_id = '{data['user_id']}'" )
        if count == 0:
            count = db.SelectRow ( cursor, table, f"user_id = '{data['user_id']}'" )
            if count == 20:
                count = -3
            else:
                count = 0
    elif table == 'users':
        count = 0
    
    # Save book in database if no existing name was found!
    if count == 0 and table == 'books' or count == 1 and table == 'authors' or count == 0 and table == 'favourites' or count == 0 and table == 'users':
        # Prepare the query
        query = PrepareQuery ( data, cols, type_ )
        
        if type_ == 1:
            # Insert a new record. Return 1 on success and 0 on failure
            count = db.Insert ( cursor, table, query )
        elif type_ == 2:
            # Update existing record
            count = db.Update ( cursor, table, query, data['id'] )

        if count:
            msg['status'] = 1
            if type_ == 1:
                cols.insert ( 0, 'id' )
                msg['message'] = f"New record added successfully!"
                
                if table == 'books':
                    # Add the recorded data to the message sent to the client
                    record = db.Select ( cursor, table, f"name = '{data['name']}'", cols )
                    msg['data'] = str ( record )
                elif table == 'users':
                    # Add the recorded data to the message sent to the client
                    record = db.Select ( cursor, table, f"email = '{data['email']}'", cols )
                    msg['data'] = str ( record )
                elif table == 'authors' or table == 'favourites':
                    # Add the recorded data to the message sent to the client
                    record = db.Select ( cursor, table, 0, cols )
                    msg['data'] = str ( record )
            else:
                msg['message'] = f"Record updated!"
                # Add the updated data to the message sent to the client
                record = db.Select ( cursor, table, f"id = '{data['id']}'", cols )
                msg['data'] = str ( record )
        
        # Run queries and free connection to database
        conn.commit ( )

    # Report a message if at least one matching record was found
    else:
        if table == 'books':
            msg['status'] = 0
            msg['message'] = f"Book name [{data['name']}] already exists!"
        
        elif table == 'authors':
            if count == -1:
                msg['status'] = 0
                msg['message'] = f"Book id does not exist. Have you uploaded this author's book before?"
            else:
                msg['status'] = 0
                msg['message'] = f"Author already exist for this book"
        
        elif table == 'favourites':
            if count == -3:
                msg['status'] = 0
                msg['message'] = f"You can only add a maximum of 20 books to your favourite list"
            else:
                msg['status'] = 0
                msg['message'] = f"This book is already in your favourite list or doesnt exist"
    
    return msg