import q_type as qt
import menus

cur_menu = menus.login_menu
cur_indx = 0

# code checking
all_menus = [menus.login_menu, menus.buyer_menu, menus.seller_menu, menus.deliver_menu]
for i in range(len(all_menus)):
    if len(all_menus[i]) != (len(all_menus[i][0].options) + 1):
        print(f"menu {i} length error")
        exit()

while(True):
    cur_indx = cur_menu[cur_indx]._print()
    if(cur_indx < 0):
        cur_menu =  menus.seller_menu  if cur_indx == -1 else\
                    menus.buyer_menu   if cur_indx == -2 else\
                    menus.deliver_menu if cur_indx == -3 else\
                    menus.login_menu
        cur_indx = 0