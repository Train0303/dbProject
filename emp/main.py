from typing import Tuple, Optional
from employee import Employee
from manager import Manager
from cs import CustomService

role_dict = {
    '1' : 'role_manager',
    '2' : 'role_cs'
}

def signin() -> Tuple[str, object]:
    id:str = input("\nID를 입력해주세요: ")
    pw:str = input("비밀번호를 입력해주세요: ")
    account:Employee = Employee(id = id, pw = pw)
    with account.conn.cursor() as cur:
        cur.execute("SELECT id, role FROM employee_tb WHERE id = %s", (id, ))
        result:Optional[Tuple[str]] = cur.fetchone()
        if result is None:
            raise Exception("데이터베이스에 이상이 있습니다 서버 관리자에게 문의 부탁드립니다.")
        print("로그인 성공")
        return (result, account.conn)
            
def signup() -> None:
    id:str = input("\nID를 입력해주세요: ")
    pw:str = input("비밀번호를 입력해주세요: ")
    name:str = input("이름을 입력해주세요: ")
    role:str = role_dict.get(input("역할을 입력해주세요\n(1. 매니저)\n(2. CS팀)\nEnter:"))
    
    if role is None:
        print("잘못된 입력입니다. 다시 시도해주세요.")
        return 

    account:Employee = Employee(id = 'temp_account', pw = '')  # 실제로는 회원가입 요청 Insert 권한만 준 임시계정으로 만든다.
    
    with account.conn.cursor() as cur:
        cur.execute("INSERT INTO employee_request_tb(id, pw, name, role) VALUES(%s, %s, %s, %s);", (id, pw, name, role, ))
        account.conn.commit()
        print("계정 생성 요청 완료!")


def start(login_info:Tuple[str, object]):
    account = None
    if login_info[0][1] == 'role_manager':
        print('매니저로 시작하셨습니다.')
        account = Manager(id=login_info[0][0], conn=login_info[1])
        account.menu()
        # 로직
    elif login_info[0][1] == 'role_cs':
        print('cs팀으로 시작하셨습니다.')
        account = CustomService(id=login_info[0][0], conn=login_info[1])
        # account.menu()
        # 로직
    
def init() -> None:
    
    choose:int = int(input("""========농산물 경매 프로그램(직원용)========
1. 로그인
2. 회원가입
3. 나가기
Enter: """))
        
    if(choose == 1):
        login_info:Tuple[list, object] = signin()
        start(login_info)
    elif(choose == 2):
        signup()
    elif(choose == 3):
        return
    
if __name__ == "__main__":
    init()

    