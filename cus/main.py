import q_type as qt
import menus

cur_menu = menus.login_menu
cur_indx = 0

while(True):
    cur_indx = cur_menu[cur_indx]._print()
    if(cur_indx < 0):
        cur_menu =  menus.seller_menu if cur_indx == -1 else\
                    menus.buyer_menu if cur_indx == -2 else\
                    menus.login_menu if cur_indx == -3 else\
                    menus.login_menu
        cur_indx = 0