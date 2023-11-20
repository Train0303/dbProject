from typing import Tuple, Optional
from connection import Employee

def signin() -> Employee:
    account:Employee = Employee('gimtaeho', None)  # -> 실제로는 직원 조회 권한만 준 임시계정으로 만든다.
    
    id:str = input("ID를 입력해주세요: ")
    pw:str = input("비밀번호를 입력해주세요: ")
    
    with account.conn.cursor() as cur:
        cur = account.conn.cursor()
        cur.execute("SELECT id, name, role FROM employee_tb WHERE id = %s AND pw = %s;", (id, pw, ))
        result:Optional[Tuple[str, str, str]] = cur.fetchone()
        if result is None:
            print("아이디와 비밀번호를 다시 확인해주세요.")
            return None
        else:
            print("로그인 성공")
            account.conn.close()
            return Employee(result[2], "비번")
            
def signup() -> None:
    id:str = input("ID를 입력해주세요: ")
    pw:str = input("비밀번호를 입력해주세요: ")
    name:str = input("이름을 입력해주세요: ")
    account:Employee = Employee('gimtaeho', None)  # -> 실제로는 직원 생성 권한만 준 임시계정으로 만든다.
    
    with account.conn.cursor() as cur:
        cur = account.conn.cursor()
        cur.execute("SELECT id FROM employee_tb where id= %s;", (id, ))
        if(cur.fetchone() is not None) :
            print("해당 ID가 이미 디비에 존재합니다.")
        else:
            cur.execute("INSERT INTO employee_tb(id, pw, name, role) VALUES(%s, %s, %s, %s);", (id, pw, name, "role_cs", ))
            account.conn.commit()
            print("계정 생성 완료!")

def init() -> None:
    
    choose:int = int(input("""========농산물 경매 프로그램(직원용)========
1. 로그인
2. 회원가입
3. 나가기
Enter: """))
        
    if(choose == 1):
        signin()
    elif(choose == 2):
        signup()
    elif(choose == 3):
        return
    
if __name__ == "__main__":
    init()
    
    