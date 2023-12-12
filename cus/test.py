sql = "select * from table where id = {0} and a = {1}"
# eval(f"f'{sql}'").format(id, a)

keys = ['id', 'a']
userInput = []
for i in range(len(keys)):
    userInput.append(input("Enter " + keys[i] + ": "))

print(sql.format(*userInput))
# id = "123"
# a = "abc"
# print(sql.format(id, a))