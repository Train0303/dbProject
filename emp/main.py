from typing import Tuple, Optional
from employee import Employee
from manager import Manager

def signin() -> Tuple[str, object]:
    id:str = input("ID를 입력해주세요: ")
    pw:str = input("비밀번호를 입력해주세요: ")
    account:Employee = Employee(id = id, pw = pw)
    with account.conn.cursor() as cur:
        cur.execute("SELECT role FROM employee_tb WHERE id = %s", (id, ))
        result:Optional[Tuple[str]] = cur.fetchone()
        if result is None:
            raise Exception("데이터베이스에 이상이 있습니다 서버 관리자에게 문의 부탁드립니다.")
        print("로그인 성공")
        return (result[0], account.conn)
            
def signup() -> None:
    id:str = input("ID를 입력해주세요: ")
    pw:str = input("비밀번호를 입력해주세요: ")
    name:str = input("이름을 입력해주세요: ")
    account:Employee = Employee(id = 'temp_account', pw = '')  # 실제로는 회원가입 요청 Insert 권한만 준 임시계정으로 만든다.
    
    with account.conn.cursor() as cur:
        cur.execute("INSERT INTO employee_request_tb(id, pw, name) VALUES(%s, %s, %s);", (id, pw, name, ))
        account.conn.commit()
        print("계정 생성 요청 완료!")

def test_insert() -> None:
    account:Employee = Employee('gimtaeho', None) # 관리자로 접근
    with account.conn.cursor() as cur:
        while (True):
            cur.execute("SELECT * FROM employee_request_tb")
            result:Optional[Tuple[str]] = cur.fetchall()
            for i, request in enumerate(result):
                print(f"{i+1} - ID : {request[0]}, Name : {request[2]}")
                
            choice = input("회원 전환할 번호를 입력해주세요(종료는 0): ")
            if choice == 0:
                break
            elif choice > len(result) or choice < 0:
                print("잘못된 입력입니다!!")
                break
            else: 
                id, pw, name, role = request
                cur.execute("INSERT INTO employee_tb(id, pw, name, role) VALUES(%s, %s, %s, %s);", (id, pw, name, role))
                cur.execute("DELETE FROM employee_request_tb WHERE id = %s;", (id, ))
                cur.execute("CREATE USER %s PASSWORD %s;", (id, pw, ))
                cur.execute("GRANT role_cs TO %s", (id, ))
            
            account.conn.commit()

def start(login_info:Tuple[str, object]):
    account = None
    if login_info[0] == 'role_manager':
        print('매니저로 시작하셨습니다.')
        account = Manager(conn=login_info[1])
        account.menu()
        # 로직
    elif login_info[1] == 'role_cs':
        print('cs팀으로 시작하셨습니다.')
        # 로직
    
def init() -> None:
    
    choose:int = int(input("""========농산물 경매 프로그램(직원용)========
1. 로그인
2. 회원가입
3. 나가기
Enter: """))
        
    if(choose == 1):
        login_info:Tuple[str, object] = signin()
        start(login_info)
    elif(choose == 2):
        signup()
    elif(choose == 3):
        return
    
if __name__ == "__main__":
    init()
    
    