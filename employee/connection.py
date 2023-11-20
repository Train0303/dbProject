import psycopg2
from exception import LoginException

role_account = {
    "gimtaeho" : None,
    "role_manager" : "manager12!",
    "role_cs" : "cs12!"
}

class Employee:
    """
    직원 클래스, 실질적으로 디비와 연결함으로써 비즈니스 로직과 분리  
    """
    host:str='localhost'
    dbname:str='dbproject'
    port:int=5432
    
    def __init__(self, id, pw):
        try:
            self.conn = psycopg2.connect(host=self.host, 
                                        user=id, 
                                        password=role_account[id],
                                        dbname=self.dbname, 
                                        port=self.port)
            
        except BaseException:
            raise LoginException('로그인에 실패했습니다.')
        