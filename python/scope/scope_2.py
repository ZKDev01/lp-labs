

x = 10

def test1():
  def show_locals():
    x = True
    print(locals())
  
  show_locals()  



def test2():
      
  def create_local_var(y):
    global x 
    y = 5
    print(x)
    print(locals())
    print(globals())
    
  create_local_var(10)
  
  """ 
  output:
    10
    {'y': 5}
    [...] 'x': 10 [...]
  """
  
def test3():
  def example():
    hello = "hi!"
    print(hello)
  example()
  #print(hello)
  
  """ 
  output:
    hi!
    Traceback (most recent call last):
      File "python/scope_2.py", line 31, in <module>
        test3()
      File "python/scope_2.py", line 29, in test3
        print(hello)
    NameError: name 'hello' is not defined
  """
  
  

def test4():
  """ 
  UnboundLocalError: cannot access local variable 'a' where it is not associated with a value
  when condition = False
  """
  condition = True
  
  if condition:
    a = 5
  
  print (a)
  

if __name__ == '__main__':
  #test1()
  #test2()
  #test3()
  test4()