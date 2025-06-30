from copy import deepcopy
from typing import List,Any,Tuple

class Matrix:
  
  def __init__(self, *args:tuple[Any], **kwargs:dict[str,int]) -> None:
    if len(args) == 1 and isinstance(args[0], list):
      self.data:List[List[Any]] = args[0]
      return 
    
    if 'rows' in kwargs and 'cols' in kwargs:
      if 'default' in kwargs:
        default_value = kwargs['default']
      rows:int = kwargs.get('rows', -1)
      cols:int = kwargs.get('cols', -1) 
      self.data = [[default_value for _ in range(cols)] for _ in range(rows)]
      return
    
  def __str__(self):
    if not self.data:
      return "[]"
    max_len = max(len(str(item)) for row in self.data for item in row)
    rows_str = []
    for row in self.data:
      row_str = " ".join(f"{str(item):>{max_len}}" for item in row)
      rows_str.append(f"[ {row_str} ]")
    return "\n".join(rows_str)
  
  def __add__(self, other:"Matrix") -> "Matrix":
    if not isinstance(other, Matrix):
      raise ValueError("Can only add another Matrix.")
    
    if len(self.data) != len(other.data) or len(self.data[0]) != len(other.data[0]):
      raise ValueError("Matrices must have the same dimensions for addition.")
    
    result = []
    for i in range(len(self.data)):
      row = [self.data[i][j] + other.data[i][j] for j in range(len(self.data[0]))]
      result.append(row)
    
    return Matrix(result)

  def __mul__(self, other:"Matrix") -> "Matrix":
    if not isinstance(other, Matrix):
      raise ValueError("Can only multiply by another Matrix.")
    
    if len(self.data[0]) != len(other.data):
      raise ValueError("Number of columns in the first matrix must equal number of rows in the second matrix.")
    
    result = []
    for i in range(len(self.data)):
      row = []
      for j in range(len(other.data[0])):
        value = sum(self.data[i][k] * other.data[k][j] for k in range(len(other.data)))
        row.append(value)
      result.append(row)
    
    return Matrix(result)
  
  def __getitem__(self, idx):
    i,j = idx
    return self.data[i][j]

  def __setitem__(self, idx:Tuple, value:int) -> None:
    i,j = idx
    self.data[i][j] = value
  
  def __iter__(self):
    self._iter_row = 0
    self._iter_col = 0
    return self

  def __next__(self):
    if self._iter_row >= len(self.data):
      raise StopIteration
    value = self.data[self._iter_row][self._iter_col]
    self._iter_col += 1
    if self._iter_col >= len(self.data[0]):
      self._iter_col = 0
      self._iter_row += 1
    return value
  
  def __getattr__(self, name):
    if name.startswith('_'):
      try:
        parts = name[1:].split('_')
        if len(parts) == 2:
          i, j = map(int, parts)
          return self.data[i][j]
      except Exception:
        pass
    raise AttributeError(f"'Matrix' object has no attribute '{name}'")

  def __setattr__(self, name, value):
    if name.startswith('_') and name[1:].replace('_', '').isdigit():
      try:
        parts = name[1:].split('_')
        if len(parts) == 2:
          i, j = map(int, parts)
          self.data[i][j] = value
          return
      except Exception:
        pass
    super().__setattr__(name, value)
  
  def as_type(self,_type):
    _copy = deepcopy(self.data)
    new_matrix = Matrix(_copy)
    for i in range(len(self.data)):
      for j in range(len(self.data[0])):
        new_matrix.data[i][j] = _type(self.data[i][j])
    return new_matrix