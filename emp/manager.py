from employee import Employee
from typing import Optional, Tuple
from psycopg2.extensions import AsIs

## 매니저 비즈니스 로직

class Manager(Employee):
    role = 'role_manager'
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        with self.conn.cursor() as cur:
            # 트랜잭션에 영향을 주지않는 세션 레벨의 명령어 -> commit()을 해줄 필요 없다.
            cur.execute("SET ROLE role_manager") 

    def menu(self) -> None:
        while (True):
            print("=======업무 선택=======")
            choice:int = int(input("""1. 가입요청 관리\n2. 경매 관리\n3. 자료 관리\n0. 나가기\nEnter: """))
            
            if choice == 1:
                self.process_signup_request()
            elif choice == 2:
                self.process_auction_manage()
            elif choice == 0:
                break
    
    def process_auction_manage(self, username:str):
        print("""1. 경매 조회\n2. 경매 수정\n""")
        
    
    def process_signup_request(self):
        choice:str = input("""1. 회원\n2. 직원\n0. 나가기\nEnter: """)
        if choice == '1':
            self._manage_member()
        elif choice == '2':
            self._manage_employee()
        elif choice == '0':
            return 
        else:
            print("잘못된 입력입니다.")

    def _manage_member(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT id, pw, name, role FROM member_request_tb")
            result:Optional[Tuple[str]] = cur.fetchall()
            for i, request in enumerate(result):
                print(f"{i+1} - ID : {request[0]}, Name : {request[2]}")
            
            choice = input("\n회원 전환할 번호를 입력해주세요: ")
        
            if not choice.isdigit() or (int(choice) > len(result) or int(choice) < 0):
                print("잘못된 입력입니다!!")  
            else: 
                try:
                    id, pw, name, role = request
                    cur.execute("INSERT INTO member_tb(id, pw, name, role) VALUES(%s, %s, %s, %s);", (id, pw, name, role))
                    cur.execute("DELETE FROM member_request_tb WHERE id = %s;", (id, ))
                    cur.execute("CREATE USER %s PASSWORD %s;", (AsIs(id), pw, ))
                    cur.execute("GRANT %s TO %s", (AsIs(role), AsIs(id), ))
                    self.conn.commit()
                except Exception as e:
                    print(e)
                    self.conn.rollback()

    def _manage_employee(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT id, pw, name, role FROM employee_request_tb")
            result:Optional[Tuple[str]] = cur.fetchall()
            for i, request in enumerate(result):
                print(f"{i+1} - ID : {request[0]}, Name : {request[2]}")
                
            choice = input("\n회원 전환할 번호를 입력해주세요: ")
        
            if not choice.isdigit() or (int(choice) > len(result) or int(choice) < 0):
                print("잘못된 입력입니다!!")  
            else: 
                try:
                    id, pw, name, role = request
                    cur.execute("INSERT INTO employee_tb(id, pw, name, role) VALUES(%s, %s, %s, %s);", (id, pw, name, role))
                    cur.execute("DELETE FROM employee_request_tb WHERE id = %s;", (id, ))
                    cur.execute("CREATE USER %s PASSWORD %s;", (AsIs(id), pw, ))
                    cur.execute("GRANT %s TO %s", (AsIs(role), AsIs(id), ))
                    self.conn.commit()
                except Exception as e:
                    print(e)
                    self.conn.rollback()
                    
    def _find_all_auction_list(self):
        with self.conn.cursor() as cur:
            cur.execute