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
        ["id", "pw", "name", "role"],
        ['?', '?', '?', '?']
    ),
]

seller_menu = [
    qt.Menu(
        "메뉴를 입력해 주세요", 
        ["경매 등록", "경매 품목 보기", "경매 취소 요청", "거래 내역 보기", "출금", "로그아웃",]
    ),
    qt.QueryResult(
        "품목 목록",
        "select * from product_tb"
    ),
    qt.QueryInsert(
        "경매 등록을 위해 필요한 정보를 입력해 주세요\n품목 id 가격 수량\n", 
        "auction_tb", 
        ["{id}", "buy_id", "emp_id", "product_id", "price", "status", "count", "start_time", "end_time"],
        [0, 0, 0, '?', '?', 'NOT_READY', '?', 0, 0]
    ),
    qt.QueryResult(
        "최근 거래 내역 10개",
        "select * from auction_tb where seller_id = {id} order by end_time desc limit 10"
    ),
    qt.QueryResult(
        "취소할 경매를 선택해 주세요", 
        "select * from auction_tb where seller_id = {id} and status = 'NOT_READY'"
    ),
    qt.Quit(),
]

buyer_menu = [
    qt.Menu(
        "메뉴를 입력해 주세요", 
        ["경매 목록 보기", "경매 입장", "계좌 보기", "입금", "로그아웃",]
    ),
    qt.QueryResult(
        "경매 목록",
        "select * from auction_tb where status = 'READY'"
    ),
    # qt.QueryResult(
    #     "입장할 경매를 선택해 주세요", 
    #     "select * from auction_tb where status = 'READY'"
    # ),
    qt.QueryResult(
        "계좌 정보",
        "select * from account_tb where id = {id}"
    ),
    qt.QueryInsert(
        "입금을 위해 필요한 정보를 입력해 주세요\n계좌 id 입금액",
        "account_record_tb",
        ["account_num", "money"],
        ['?', '?']
    ),
    qt.Quit(),
]

deliver_menu = [
    qt.Menu(
        "메뉴를 입력해 주세요", 
        ["배달 요청 보기", "배달 내역 보기", "유통 지역 수정", "로그아웃",]
    ),
    qt.Quit(),
]