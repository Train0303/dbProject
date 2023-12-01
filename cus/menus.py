import q_type as qt

login_menu = [
    qt.Menu(
        "메뉴를 입력해 주세요", 
        ["로그인", "회원가입"]
    ),
    qt.Login(),
    qt.QueryInsert(
        "회원가입을 위해 필요한 정보를 입력해 주세요\n역할('role_buyer','role_seller','role_deliver')",
        "member_request_tb",
        ["id",  "pw",   "name", "role", 'address',  'location_name'],
        [ '?',   '?',      '?',    '?',       '?',              '?']
    ),
]

seller_menu = [
    qt.Menu(
        "메뉴를 입력해 주세요", 
        ["경매 품목 보기", "경매 등록" , "거래 내역 보기", "잔액 조회", "출금", "로그아웃",]
    ),
    qt.QueryResult(
        "품목 목록",
        "select * from product_tb"
    ),
    qt.QueryInsert(
        "경매 등록을 위해 필요한 정보를 입력해 주세요", 
        "auction_tb", 
        ["sel_id", "product_id", "price", "count", "adjust","start_time"],
        ["__id__",          '?',     '?',     '?',      "N",        '?',]
    ),
    qt.QueryResult(
        "최근 거래 내역",
        "select * from auction_tb where sel_id = '__id__' order by end_time desc"
    ),
    qt.QueryResult(
        "잔액 조회",
        "select balance from member_tb where id = '__id__'"
    ),
    qt.QueryTransaction(
        "출금을 위해 필요한 정보를 입력해 주세요\n",
        [
            "insert into account_record_tb (receiver, money) values ('__id__', {0});",
            "update member_tb set balance = balance - {0} where id = '__id__';"
        ],
        ['money'],
    ),
    qt.Quit(),
]

buyer_menu = [
    qt.Menu(
        "메뉴를 입력해 주세요", 
        ["경매 목록", "경매 입찰", "잔액 조회", "입금", "로그아웃",]
    ),
    qt.QueryResult(
        "진행중인 경매 목록입니다",
        "select * from auction_tb where start_time <= now() and end_time > now()"
    ),
    qt.QueryTransaction(
        "경매 입찰을 위해 필요한 정보를 입력해 주세요",
        [
            "insert into auction_record_tb (auc_id, buy_id, price) values ({0}, '__id__', {1});",
            "update auction_tb set price = {1}, buy_id = '__id__' where id = {0};"
        ],
        ['auc_id', 'price'],
    ),
    qt.QueryResult(
        "잔액 조회",
        "select balance from member_tb where id = '__id__'"
    ),
    qt.QueryTransaction(
        "입금을 위해 필요한 정보를 입력해 주세요",
        [
            "insert into account_record_tb (receiver, money) values ('__id__', {0});",
            "update member_tb set balance = balance + {0} where id = '__id__';"
        ],
        ['money'],
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
    qt.Quit(),
    qt.Quit(),
    qt.Quit(),
    qt.Quit(),
]