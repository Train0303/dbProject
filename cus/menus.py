import q_type as qt

login_menu = [
    qt.Menu(
        "메뉴를 입력해 주세요", 
        ["로그인", "회원가입"]
    ),
    qt.Login(),
    qt.QueryInsert(
        "회원가입을 위해 필요한 정보를 입력해 주세요\n역할('role_buyer','role_seller','role_deliver')",
        "insert into member_request_tb (id, pw, name, role) values ('{0}', '{1}', '{2}', '{3}')",
        ["id", "pw", "name", "role"],
    ),
]

seller_menu = [
    qt.Menu(
        "메뉴를 입력해 주세요", 
        ["경매 품목 보기", "경매 등록" , "경매 내역 보기", "잔액 조회", "출금", "로그아웃",]
    ),
    qt.QueryResult(
        "품목 목록",
        "select * from product_tb"
    ),
    qt.QueryInsert(
        "경매 등록을 위해 필요한 정보를 입력해 주세요", 
        "insert into auction_tb (sel_id, product_id, price, count, adjust, start_time) values ('__id__', {0}, {1}, {2}, 'N', '{3}')", 
        ["product_id", "price", "count", "start_time"],
    ),
    qt.QueryResult(
        "경매 내역 보기",
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
        ["경매 목록", "경매 입찰", "배송 요청", "잔액 조회", "입금", "로그아웃",]
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
    qt.QueryInsert(
        "배송 요청을 위해 필요한 정보를 입력해 주세요",
        "insert into delivery_tb (auc_id, loc_id, address, status) values ({0}, {1}, '{2}', 'READY');",
        ['auc_id', 'loc_id', 'address'],
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
        ["배달 대기 목록", "배달 수락","배달 상태 변경", "배달 내역 보기", "지역 목록", "유통 지역 목록", "유통 지역 추가", "유통 지역 삭제", "로그아웃",]
    ),
    qt.QueryResult(
        "배달 요청이 들어온 목록입니다",
        "select * from delivery_tb d \
            join delivery_area_tb a on d.loc_id = a.loc_id \
            where d.deli_id is null"
    ),
    qt.QueryInsert(
        "배송 수락을 위해 필요한 정보를 입력해 주세요",
        "update delivery_tb set deli_id = '__id__', status = 'IN_PROGRESS' where id = {0}",
        ['delivery id'],
    ),
    qt.QueryInsert(
        "배달 상태 변경을 위해 필요한 정보를 입력해 주세요\nstatus : READY, IN_PROGRESS, DELIVERED",
        "update delivery_tb set status = '{1}' where id = {0}",
        ['delivery id', 'status'],
    ),
    qt.QueryResult(
        "배달 내역",
        "select * from delivery_tb where deli_id = '__id__'"
    ),
    qt.QueryResult(
        "현재 등록되어 있는 지역들의 목록입니다",
        "select * from location_tb"
    ),
    qt.QueryResult(
        "유통 지역 목록",
        "select name from location_tb join delivery_area_tb on loc_id = id where mem_id = '__id__'"
    ),
    qt.QueryInsert(
        "유통 지역 추가",
        "insert into delivery_area_tb (mem_id, loc_id) values ('__id__', {0})",
        ['location id'],
    ),
    qt.QueryInsert(
        "유통 지역 삭제",
        "delete from delivery_area_tb where mem_id = '__id__' and loc_id = {0}",
        ['location id'],
    ),
    qt.Quit(),
]