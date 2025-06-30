from matrix import Matrix

if __name__ == "__main__":
  matrix1 = Matrix([[1, 2], [3, 4]])
  matrix2 = Matrix(rows=2, cols=2, default=1.1) 

  print("Matrix 1")
  print(matrix1)
  
  print("Matrix 2")
  print(matrix2)
  
  print("Addition of Matrix 1 and Matrix 2:")
  print(matrix1 + matrix2)
  
  for item in matrix1:
    print (item)
  
  n_matrix1 = matrix1.as_type(float)
  print(n_matrix1)
  
  n_matrix1[0,0] = 9999999999
  print(matrix1)
  print(n_matrix1)
  
  n_matrix1._1_1 = 1234.4321
  print(n_matrix1)
