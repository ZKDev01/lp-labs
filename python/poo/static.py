class UniqueStruct:
  def __init__(self,value:int):
    self.value = value

class Utils:
  @staticmethod
  def to_sum(a:UniqueStruct,b:UniqueStruct) -> UniqueStruct:
    r = UniqueStruct(a.value + b.value)
    return r

a = UniqueStruct(10)
b = UniqueStruct(20)
c = Utils.to_sum(a,b)
print(c.value) # Output: 30


