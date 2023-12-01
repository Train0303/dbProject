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
            choice:str = input('1. 가입요청 관리\n2. 경매 관리\n3. 직원 권한 변경\n0. 나가기\nEnter: ')
            
            if choice == '1':
                self.process_signup_request()
            elif choice == '2':
                self.process_auction_manage()
            elif choice == '3':
                self.process_promote_employee_request()
            elif choice == '0':
                break
    
    def process_auction_manage(self) -> None:
        choice:str = input("""1. 경매 조회\n2. 경매 수정\nEnter: """)
        if choice == '1':
            result:List[dict] = self._find_all_auction_list()
            print(*result, sep = '\n')
        elif choice == '2':
            result:List[dict] = self._find_not_verified_auction_list()
            self._change_auction_status(result)
    
    def process_signup_request(self) -> None:
        choice:str = input("""1. 회원\n2. 직원\n0. 나가기\nEnter: """)
        if choice == '1':
            self._manage_member()
        elif choice == '2':
            self._manage_employee()
        elif choice == '0':
            return 
        else:
            print("잘못된 입력입니다.")

    def process_promote_employee_request(self) -> None:
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

    def _manage_member(self) -> None:
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
                    id, pw, name, role = result[int(choice)-1]
                    cur.execute("INSERT INTO member_tb(id, pw, name, role) VALUES(%s, %s, %s, %s);", (id, pw, name, role))
                    cur.execute("DELETE FROM member_request_tb WHERE id = %s;", (id, ))
                    cur.execute("CREATE USER %s PASSWORD %s;", (AsIs(id), pw, ))
                    cur.execute("GRANT %s TO %s", (AsIs(role), AsIs(id), ))
                    self.conn.commit()
                except Exception as e:
                    print(e)
                    self.conn.rollback()

    def _manage_employee(self) -> None:
        with self.conn.cursor() as cur:
            cur.execute("SELECT id, pw, name, role FROM employee_request_tb")
            result:List[Tuple[tuple]] = cur.fetchall()
            for i, request in enumerate(result):
                print(f"{i+1} - ID : {request[0]}, Name : {request[2]}, Role : {request[3]}")
                
            choice = input("\n회원 전환할 번호를 입력해주세요: ")
        
            if not choice.isdigit() or (int(choice) > len(result) or int(choice) <= 0):
                print("잘못된 입력입니다!!")  
            else: 
                try:
                    id, pw, name, role = result[int(choice)-1]
                    cur.execute("INSERT INTO employee_tb(id, pw, name, role) VALUES(%s, %s, %s, %s);", (id, pw, name, role))
                    cur.execute("DELETE FROM employee_request_tb WHERE id = %s;", (id, ))
                    cur.execute("CREATE USER %s PASSWORD %s;", (AsIs(id), pw, ))
                    cur.execute("GRANT %s TO %s", (AsIs(role), AsIs(id), ))
                    self.conn.commit()
                except Exception as e:
                    print(e)
                    self.conn.rollback()
                    
            print("회원 생성이 완료되었습니다!")
        
        
    def _find_all_auction_list(self) -> List[dict]:
        with self.conn.cursor() as cur:
            cur.execute("SELECT a.id, a.sel_id, a.product_id, p.name, a.price, a.verified, a.count, a.start_time, a.end_time\
                FROM auction_tb a\
                JOIN product_tb p on product_id = p.id\
                ORDER BY a.id desc")
            print('\n=======경매 목록=======')
            return [
                {
                    "auctionId": data[0],
                    'sellerId': data[1],
                    'productId': data[2],
                    'productName': data[3],
                    'auctionPrice': data[4],
                    'verified': data[5],
                    'count': data[6],
                    'start_time': data[7].strftime("%Y-%m-%d"),
                    'end_time': data[8].strftime("%Y-%m-%d")
                }
                for data in cur.fetchall()]
        
    
    def _find_not_verified_auction_list(self) -> List[dict]:
        with self.conn.cursor() as cur:
            cur.execute("SELECT a.id, a.sel_id, a.product_id, p.name, a.price, a.verified, a.count, a.start_time, a.end_time\
                FROM auction_tb a\
                JOIN product_tb p on product_id = p.id\
                WHERE a.verified = 'N'\
                ORDER BY a.id DESC")
            return[
                {
                    "auctionId": data[0],
                    'sellerId': data[1],
                    'productId': data[2],
                    'productName': data[3],
                    'auctionPrice': data[4],
                    'verified': data[5],
                    'count': data[6],
                    'start_time': data[7].strftime("%Y-%m-%d"),
                    'end_time': data[8].strftime("%Y-%m-%d")
                }
                for data in cur.fetchall()]
    
    def _change_auction_status(self, result:List[dict]) -> None:
        
        print('\n=======경매 목록=======')
        for i, data in enumerate(result):
            print(f'{i+1} - {data}')
        
        choice:str = input("\n등록할 경매의 번호를 입력해주세요: ")
        if not choice.isdigit() or (int(choice) > len(result) or int(choice) <= 0):
                print("잘못된 입력입니다!!") 
        else:
            with self.conn.cursor() as cur:
                cur.execute("UPDATE auction_tb SET verified = 'Y', emp_id = %s WHERE id = %s;", 
                            (self.id, result[int(choice)-1]['auctionId'], ))
            self.conn.commit()
        
        print("경매 수정이 완료되었습니다.")