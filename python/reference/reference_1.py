
def square_number(n):
  n*=n

def square_list_first_element(l):
  l[0]*=l[0]

x = 5
print(x)          # 5
square_number(x)
print(x)          # 5

y = [5]
print(y)          # [5]
square_list_first_element(y)
print(y)          # [25]
