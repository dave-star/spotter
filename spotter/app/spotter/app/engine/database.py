import sqlite3

def Connect ( ):
    conn = sqlite3.connect ( 'db.sqlite3' )
    return conn

def SelectRow ( cursor, table, condition ):
    count = 0
    cursor.execute (
        f"SELECT * FROM {table} WHERE {condition}"
    )

    row = cursor.fetchall ( )
    
    return len ( row )

def SelectFilter ( cursor, table, condition, columns, query ):
    
    query = query['query']
    cursor.execute (
        f"SELECT * FROM {table} WHERE name LIKE '%{query}%'"
    )

    row = cursor.fetchall ( )
    data = []

    if len ( row ) == 0:
        cursor.execute (
            f"SELECT * FROM 'authors' WHERE author_name LIKE '%{query}%'"
        )
        row = cursor.fetchall ( )
        if len ( row ):
            for i in row:
                i = list ( i )
                cursor.execute (
                    f"SELECT * FROM {table} WHERE id = {i[4]}"
                )
                
                xrow = cursor.fetchall ( )
                for x in xrow:
                    x = list ( x )
                    xdata = {}
                    for i in range ( len ( columns ) ):
                        xdata[columns[i]] = x[i]
                    data.append ( xdata )

    else:
        for x in row:
            x = list ( x )
            xdata = {}
            for i in range ( len ( columns ) ):
                xdata[columns[i]] = x[i]
            data.append ( xdata )

    return data

def Select ( cursor, table, condition, columns ):
    if condition != 0:
        col = ','.join ( columns )
        cursor.execute (
            f"SELECT {col} FROM {table} WHERE {condition}"
        )

    else:
        cursor.execute (
            f"SELECT * FROM {table} WHERE 1 ORDER BY id DESC LIMIT 1"
        )

    row = cursor.fetchall ( )
    data = []
    for x in row:
        x = list ( x )
        xdata = {}
        for i in range ( len ( columns ) ):
            xdata[columns[i]] = x[i]
        data.append ( xdata )
    
    return data

def Update ( cursor, table, query, condition ):
    
    if cursor.execute ( f"UPDATE {table} SET {query} WHERE id = {condition}" ):
        return 1
    else:
        return 0

def Delete ( cursor, table, condition ):
    if cursor.execute ( f"DELETE FROM {table} WHERE {condition}" ):
        return 1
    else:
        return 0
    
def Insert ( cursor, table, query ):
    if cursor.execute ( f"INSERT INTO {table} {query}" ):
        return 1
    else:
        return 0
