from employee import Employee
from typing import Optional, Tuple, List
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
            print("\n=======업무 선택=======")
            choice:int = int(input("""1. 가입요청 관리\n2. 경매 관리\n3. 자료 관리\n4. 직원 권한 변경\n0. 나가기\nEnter: """))
            
            if choice == 1:
                self.process_signup_request()
            elif choice == 2:
                self.process_auction_manage()
            elif choice == 3:
                pass
            elif choice == 4:
                self._promote_employee()
            elif choice == 0:
                break
    
    def process_auction_manage(self):
        choice:str = input("""1. 경매 조회\n2. 경매 수정\nEnter: """)
        if choice == '1':
            self._find_all_auction_list()
        elif choice == '2':
            print(2)
    
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
            result:List[Tuple[str]] = cur.fetchall()
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
            result:List[Tuple[tuple]] = cur.fetchall()
            for i, request in enumerate(result):
                print(f"{i+1} - ID : {request[0]}, Name : {request[2]}")
                
            choice = input("\n회원 전환할 번호를 입력해주세요: ")
        
            if not choice.isdigit() or (int(choice) > len(result) or int(choice) <= 0):
                print("잘못된 입력입니다!!")  
            else: 
                try:
                    id, pw, name, role = result[choice-1]
                    cur.execute("INSERT INTO employee_tb(id, pw, name, role) VALUES(%s, %s, %s, %s);", (id, pw, name, role))
                    cur.execute("DELETE FROM employee_request_tb WHERE id = %s;", (id, ))
                    cur.execute("CREATE USER %s PASSWORD %s;", (AsIs(id), pw, ))
                    cur.execute("GRANT %s TO %s", (AsIs(role), AsIs(id), ))
                    self.conn.commit()
                except Exception as e:
                    print(e)
                    self.conn.rollback()
    
    def _promote_employee(self):
        print("\n=======승진 가능 대상자 목록=======")
        with self.conn.cursor() as cur:
            cur.execute("SELECT id, name FROM employee_tb WHERE role='role_cs';")
            result:List[tuple] = cur.fetchall()
            
            if not result:
                print("승진 가능한 직원이 존재하지 않습니다.")
                return
            
            for i, data in enumerate(result):
                print(f"{i+1} - ID : {data[0]}, Name : {data[1]}")

            emp_id:str = input("\n승진시킬 직원의 아이디를 입력해주세요: ")
            try:
                cur.execute("UPDATE employee_tb SET role = 'role_manager' WHERE id = %s;", (emp_id, ))
                cur.execute("GRANT %s TO %s;", (AsIs('role_manager'), AsIs(emp_id)))
                cur.execute("REVOKE %s FROM %s;", (AsIs('role_cs'), AsIs(emp_id)))
                self.conn.commit()
                print("승진이 완료되었습니다!")
            except Exception as e:
                print(e)
                self.conn.rollback()
        
        
    def _find_all_auction_list(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT a.id, a.sel_id, a.product_id, p.name, a.price, a.status, a.count, a.start_time, a.end_time\
                FROM auction_tb a\
                JOIN product_tb p on product_id = p.id")
            print('\n=======경매 목록=======')
            result:Optional[tuple] = cur.fetchall()
            print(*result, sep='\n')