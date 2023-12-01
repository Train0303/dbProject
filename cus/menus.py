import q_type as qt

login_menu = [
    qt.Menu(
        "메뉴를 입력해 주세요", 
        ["로그인", "회원가입"]
    ),
    qt.Login(),
    qt.QueryInsert(
        "회원가입을 위해 필요한 정보를 입력해 주세요\n아이디 비밀번호 이름 역할('role_buyer','role_seller','role_deliver')",
        "member_request_tb",
        ["id",  "pw",   "name", "role"],
        [ '?',   '?',       '?',    '?']
    ),
]

seller_menu = [
    qt.Menu(
        "메뉴를 입력해 주세요", 
        ["경매 품목 보기", "경매 등록" , "거래 내역 보기", "잔액 조회", "출금", "로그아웃",]
        # ["경매 품목 보기", "경매 등록" , "경매 취소 요청", "거래 내역 보기", "잔액 조회", "출금", "로그아웃",]
    ),
    qt.QueryResult(
        "품목 목록",
        "select * from product_tb"
    ),
    qt.QueryInsert(
        "경매 등록을 위해 필요한 정보를 입력해 주세요\n", 
        "auction_tb", 
        ["sel_id",  "buy_id",   "emp_id",   "product_id",   "price", "verified",   "count", "start_time"],
        ["__id__",          0,          0,          '?',        '?',        'N',       '?',         '?',]
    ),
    # qt.QueryInsert(
    #     "취소 요청을 할 경매를 선택해 주세요",
    #     "auction_tb",
    #     [],
    #     []
    # ),
    qt.QueryResult(
        "최근 거래 내역",
        "select * from auction_tb where sel_id = __id__ order by end_time desc"
    ),
    qt.QueryResult(
        "계좌 잔액",
        "select * from account_tb where mem_id = __id__"
    ),
    qt.QueryInsert(
        "출금액을 입력해 주세요", 
        "account_record_tb",
        ["account_num", "money"],
        [           '?',    '?']
    ),
    qt.Quit(),
]

buyer_menu = [
    qt.Menu(
        "메뉴를 입력해 주세요", 
        ["경매 목록 보기", "경매 입장", "잔액 조회", "입금", "로그아웃",]
    ),
    qt.QueryResult(
        "경매 목록",
        "select * from auction_tb where status = 'READY'"
    ),
    qt.QueryResult(
        # todo
        "입장할 경매를 선택해 주세요\n", 
        "select * from auction_tb where status = 'READY'"
    ),
    qt.QueryResult(
        "잔액 조회\n",
        "select * from account_tb where id = __id__"
    ),
    qt.QueryInsert(
        "입금을 위해 필요한 정보를 입력해 주세요\n",
        "account_record_tb",
        ["account_num", "money"],
        [          '?',     '?']
    ),
    qt.Quit(),
]

deliver_menu = [
    qt.Menu(
        "메뉴를 입력해 주세요", 
        ["배달 요청 보기", "배달 상태 변경", "배달 내역 보기", "유통 지역 수정", "로그아웃",]
        # select * from auction_tb join member_tb ~~~ where loc_id in (~~~~) and end_time < now();
    ),
    qt.Quit(),
]