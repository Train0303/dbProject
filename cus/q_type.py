import psycopg2

id = 'db2023' # todo: change to default id
conn = psycopg2.connect(
    dbname = "dbproject",
    user = id,
    password = "",
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

        print("=====================================")
        print("로그인을 위해 아이디와 비밀번호를 입력해 주세요\n")
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
        cursor.execute("SET ROLE %s", (r[0], ))
        # r = ['role_deliver']
        print("Login Success")
        print("=====================================")
        return  -1 if (r[0] == 'role_seller') else \
                -2 if (r[0] == 'role_buyer')  else \
                -3 if (r[0] == 'role_deliver') else 0


class Menu:
    def __init__(self, title, options):
        self.title = title
        self.options = options

    def _print(self):
        print("=====================================")
        print(self.title + '\n')
        for i in range(len(self.options)):
            print(f"{i + 1}. {self.options[i]}")
        
        userInput = 0
        while(True):
            userInput = int(input("Enter : "))
            if(userInput > 0 and userInput <= len(self.options)):
                break
        print("=====================================")

        return userInput

class QueryResult:
    def __init__(self, title, query):
        self.title = title
        self.query = query
    
    def _print(self):
        global cursor
        
        print("=====================================")
        print(self.title + '\n')
        
        sql = self.query.replace("__id__", id)
        cursor.execute(sql)

        result = cursor.fetchall()
        for row in result:
            print(row)
        print("=====================================")

        return 0

class QueryInsert:
    def __init__(self, title, sql, keys):
        self.title = title
        self.sql = sql
        self.keys = keys
    
    def _print(self):
        global cursor, conn, id
        userInput = []

        print("=====================================")
        print(self.title + '\n')

        for i in range(len(self.keys)):
            userInput.append(input("Enter " + self.keys[i] + ": "))

        sql = self.sql.replace("__id__", id)
        sql = sql.format(*userInput)
        cursor.execute(sql)

        conn.commit()
        print("=====================================")

        return 0

class QueryTransaction:
    def __init__(self, title, sqls, keys):
        self.title = title
        self.sqls = sqls
        self.keys = keys
    
    def _print(self):
        global cursor, conn, id
        userInput = []

        print("=====================================")
        print(self.title + '\n')

        for i in range(len(self.keys)):
            userInput.append(input("Enter " + self.keys[i] + ": "))

        for sql in self.sqls:
            sql = sql.replace("__id__", id)
            sql = sql.format(*userInput)
            cursor.execute(sql)
        
        conn.commit()
        print("=====================================")

        return 0

class Quit:
    def _print(self):
        close()
        print("Logout Success")
        return -5