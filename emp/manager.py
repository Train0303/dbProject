from employee import Employee
## 매니저 비즈니스 로직

class Manager(Employee):
    role = 'role_manager'
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # @classmethod
    # def from_employee(cls, employee:Employee):
    #     return cls(employee.conn)
    
    def menu(self):
        print("=======업무 선택=======")
        choice:int = input("""1. 회원 관리
2. 경매 관리
3. 자료 관리
"""
        )