from employee import Employee
from typing import List
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
                self.process_auction_record()
            elif choice == '2':
                # 입출금 기록 조회 로직
                pass
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
            result:List[dict] = self._find_by_buy_id(member_id)
            print(*result, sep='\n')
        elif choice == '3':
            print("\n=======경매 정보로 경매 기록 조회=======\n")
            auc_id:int = int(input("경매id 입력: "))
            result:List[dict] = self._find_by_auc_id(auc_id)
            print(*result, sep='\n')
        elif choice == '0':
            return

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
    
    def _find_by_buy_id(self, member_id:str) -> List[dict]:
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
        
    def _find_by_auc_id(self, auc_id:int) -> List[dict]:
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