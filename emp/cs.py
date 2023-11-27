from employee import Employee
## Custom Service 비지니스 로직

class CustomService(Employee):
    role = 'role_cs'
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.conn.cursor() as cur:
            # 트랜잭션에 영향을 주지않는 세션 레벨의 명령어 -> commit()을 해줄 필요 없다.
            cur.execute("SET ROLE role_cs") 