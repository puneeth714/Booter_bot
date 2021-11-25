import cx_Oracle
def connect_to_Oracle(user, password,address):
    con = cx_Oracle.connect(
    user=user,
    password=password,
    dsn=address)

    cursor=con.cursor()
    print("Database version:", con.version)

    # cursor.execute("create table  employee(empid integer primary key, name varchar2(30), salary number(10, 2))")
    return cursor
    # cursor.execute("""describe  employee""")
    cursor.close()
    con.close()
cursor_is=connect_to_Oracle("system","oracle","localhost:49161")

cursor_is.execute("""
    create table todoitem (
        id number generated always as identity,
        description varchar2(4000),
        creation_ts timestamp with time zone default current_timestamp,
        done number(1,0),
        primary key (id));""")


cursor_is.close()