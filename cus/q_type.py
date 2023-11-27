import psycopg2

id = None
conn = psycopg2.connect(
    dbname = "dbproject",
    user = "db2023",
    password = "db2023",
    host = "::1",
    port = 5432
)
cursor = conn.cursor()

def close():
    global conn, cursor

    conn.close()
    conn = None
    cursor = None


class Login:
    def _print(self):
        global conn, cursor, id

        id = input("ID: ")
        pw = input("PW: ")

        if(conn != None):
            close()
        conn = psycopg2.connect(
            dbname = "dbproject",
            user = id,
            password = pw,
            host = "::1",
            port = 5432
        )
        cursor = conn.cursor()
        cursor.execute(f"select role from member_tb where id = '{id}'")
        r = cursor.fetchone()

        print("Login Success")
        return  -1 if (r[0] == 'role_buyer') else \
                -2 if (r[0] == 'role_seller') else \
                -3 if (r[0] == 'role_deliver') else 0


class Menu:
    def __init__(self, title, options):
        self.title = title
        self.options = options

    def _print(self):
        print(self.title)
        for i in range(len(self.options)):
            print(f"{i + 1}. {self.options[i]}")
        
        userInput = 0
        while(True):
            userInput = int(input("Enter : "))
            if(userInput > 0 and userInput <= len(self.options)):
                break

        return userInput

class QueryResult:
    def __init__(self, title, query):
        self.title = title
        self.query = query
    
    def _print(self):
        global cursor
        
        print(self.title)
        
        sql = self.query
        sql = eval(f"f'{sql}'").format(id) if "{id}" in sql else sql
        cursor.execute(sql)

        result = cursor.fetchall()
        for row in result:
            print(row)

class QueryInsert:
    def __init__(self, title, table, keys, values):
        self.title = title
        self.table = table
        self.keys = keys
        self.values = values
    
    def _print(self):
        global cursor, conn
        insertValues = []

        print(self.title)
        for i in range(len(self.values)):
            if(self.values[i] == '?'):
                insertValues.append(input("Enter " + self.keys[i] + ": "))

        sql = f"INSERT INTO {self.table} ({','.join(self.keys)}) VALUES ({str(insertValues)[1:-1]})"
        sql = eval(f"f'{sql}'").format(id) if "{id}" in sql else sql
        cursor.execute(sql)
        conn.commit()

        return 0

class Quit:
    def _print(self):
        close()
        print("Logout Success")
        return -5