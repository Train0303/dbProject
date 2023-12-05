from employee import Employee
from typing import List
from datetime import datetime
## Custom Service 비지니스 로직

class CustomService(Employee):
    role = 'role_cs'
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.conn.cursor() as cur:
            # 트랜잭션에 영향을 주지않는 세션 레벨의 명령어 -> commit()을 해줄 필요 없다.
            cur.execute("SET ROLE role_cs") 
            
    
    def menu(self) -> None:
        while True:
            print("\n=======업무 선택=======")
            
            choice:str = input('1. 경매 기록 조회\n2. 입출금 기록 조회\n0. 나가기\nEnter: ')
            if choice == '1':
                # 경매 기록 조회 로직
                self.process_auction_record()
            elif choice == '2':
                # 입출금 기록 조회 로직
                self.process_account_record()
            elif choice == '0':
                break
            

    def process_auction_record(self) -> None:
        print("\n=======경매 기록 조회 시스템=======")
        
        choice:str = input('1. 전체 기록 조회\n2. 회원 정보로 조회\n3. 경매 정보로 조회\n0. 나가기\nEnter: ')
        if choice == '1':
            print("\n=======전체 경매 기록 조회=======\n")
            result:List[dict] = self._find_all_auction_record()
            print(*result, sep='\n')
        elif choice == '2':
            print("\n=======회원 정보로 경매 기록 조회=======\n")
            member_id:str = input("회원정보 입력: ")
            result:List[dict] = self._find_auction_record_by_buy_id(member_id)
            print(*result, sep='\n')
        elif choice == '3':
            print("\n=======경매 정보로 경매 기록 조회=======\n")
            auc_id:int = int(input("경매id 입력: "))
            result:List[dict] = self._find_auction_record_by_auc_id(auc_id)
            print(*result, sep='\n')
        elif choice == '0':
            return

    def process_account_record(self) -> None:
        print("\n=======입출금 기록 조회 시스템=======")
        choice:str = input('1. 전체 기록 조회\n2. 날짜 정보로 조회\n0. 나가기\nEnter: ')
        
        if choice == '1':
            print('\n=======전체 입출금 기록 조회=======\n')
            result:List[dict] = self._find_all_account_record()
            print(*result, sep='\n')
        elif choice == '2':
            print('\n=======날짜로 입출금 기록 조회=======\n')
            date:str = input('날짜 입력(yyyy-mm-dd): ')
            try:
                datetime.strptime(date, '%Y-%m-%d')
            except Exception as e:
                print(e)
                print("올바른 입력이 아닙니다!")
                return
            
            result:List[dict] = self._find_account_record_by_date(date)
            print(*result, sep='\n')

    def _find_all_auction_record(self) -> List[dict]:
        with self.conn.cursor() as cur:
            cur.execute("SELECT m.id, m.name, a.id, p.name, p.kind, ar.price, ar.order_time \
                FROM auction_record_tb ar \
                JOIN auction_tb a ON ar.auc_id = a.id \
                JOIN member_tb m ON ar.buy_id = m.id \
                JOIN product_tb p ON a.product_id = p.id \
                ORDER BY order_time")
            return [
                {
                    "memberId" : data[0],
                    "memberName" : data[1],
                    'auctionId' : data[2],
                    "productName" : data[3],
                    "productKind" : data[4],
                    "requestPrice" : data[5],
                    "orderTime" : data[6].strftime('%Y/%m/%d')
                }
                for data in cur.fetchall()]
    
    def _find_auction_record_by_buy_id(self, member_id:str) -> List[dict]:
        with self.conn.cursor() as cur:
            cur.execute("SELECT m.id, m.name, a.id, p.name, p.kind, ar.price, ar.order_time \
                FROM auction_record_tb ar \
                JOIN auction_tb a ON ar.auc_id = a.id \
                JOIN member_tb m ON ar.buy_id = m.id \
                JOIN product_tb p ON a.product_id = p.id \
                WHERE m.id = %s \
                ORDER BY order_time", (member_id, ))
            
            return [
                {
                    "memberId" : data[0],
                    "memberName" : data[1],
                    'auctionId' : data[2],
                    "productName" : data[3],
                    "productKind" : data[4],
                    "requestPrice" : data[5],
                    "orderTime" : data[6].strftime('%Y/%m/%d')
                }
                for data in cur.fetchall()]
        
    def _find_auction_record_by_auc_id(self, auc_id:int) -> List[dict]:
        with self.conn.cursor() as cur:
            cur.execute("SELECT m.id, m.name, a.id, p.name, p.kind, ar.price, ar.order_time \
                FROM auction_record_tb ar \
                JOIN auction_tb a ON ar.auc_id = a.id \
                JOIN member_tb m ON ar.buy_id = m.id \
                JOIN product_tb p ON a.product_id = p.id \
                WHERE a.id = %s \
                ORDER BY order_time", (auc_id, ))
            return [
                {
                    "memberId" : data[0],
                    "memberName" : data[1],
                    'auctionId' : data[2],
                    "productName" : data[3],
                    "productKind" : data[4],
                    "requestPrice" : data[5],
                    "orderTime" : data[6].strftime('%Y-%m-%d')
                }
                for data in cur.fetchall()]
            
    
    def _find_all_account_record(self) -> List[dict]:
        with self.conn.cursor() as cur:
            cur.execute("SELECT receiver, r.name, sender, s.name, money, created_at FROM account_record_tb \
                LEFT JOIN member_tb r ON r.id = receiver \
                LEFT JOIN member_tb s ON s.id = sender")
            
            return [
                {
                    "receiver_id" : data[0],
                    "receiver_name" : data[1],
                    "sender_id" : data[2],
                    "sender_name" : data[3],
                    "money" : data[4],
                    "created_at" : data[5]
                } for data in cur.fetchall()]
            
    
    def _find_account_record_by_date(self, date:str) -> List[dict]:
        with self.conn.cursor() as cur:
            cur.execute("SELECT receiver, r.name, sender, s.name, money, created_at FROM account_record_tb \
                LEFT JOIN member_tb r ON r.id = receiver \
                LEFT JOIN member_tb s ON s.id = sender \
                WHERE DATE(created_at) = %s \
                ORDER BY created_at DESC;", (date, ))
            return [
                {
                    "receiver_id" : data[0],
                    "receiver_name" : data[1],
                    "sender_id" : data[2],
                    "sender_name" : data[3],
                    "money" : data[4],
                    "created_at" : data[5]
                } for data in cur.fetchall()]