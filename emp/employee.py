import psycopg2
from exception import LoginException

# role_account = {
#     "temp_account" : '',
#     "role_manager" : "manager12!",
#     "role_cs" : "cs12!"
# }

class Employee:
    """
    직원 클래스, 실질적으로 디비와 연결함으로써 비즈니스 로직과 분리  
    """
    host:str='localhost'
    dbname:str='dbproject'
    port:int=5432
    conn = None
    
    def __init__(self, **kwargs):
        if kwargs.get('conn'):
            self.conn = kwargs['conn']
        elif kwargs.get('id'):
            try:
                self.conn = psycopg2.connect(host=self.host, 
                                            user=kwargs['id'], 
                                            password=kwargs.get('pw'),
                                            dbname=self.dbname, 
                                            port=self.port)
                
                self.conn.autocommit = False
                
            except BaseException:
                raise LoginException('로그인에 실패했습니다.')
        else:
            raise BaseException("잘못된 입력입니다.")
    