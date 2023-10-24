# 24.10.2023
import numpy as np
import matplotlib.pyplot as plt


def create_matrix(dimension, num_diagonal, num_adjacent):
    # create a matrix of a given dimension with a given diagonal value and given adjacent value
    G = np.zeros((dimension, dimension))
    for i in range(dimension):
        if i == 0:
            G[0, 1] = num_adjacent
            G[0, 0] = num_diagonal
        elif i == dimension-1:
            G[i, -2] = num_adjacent
            G[i, -1] = num_diagonal
        else:
            G[i, i-1] = num_adjacent
            G[i, i+1] = num_adjacent
            G[i, i] = num_diagonal
    return G

def taking_diagonal(A):
    # taking the diagonal of a matrix, and checking that it is a diagonal matrix
    num_diag = A[0, 0]
    for i in range(1, len(A)):
        if A[i, i] != num_diag:
            raise ValueError("A must be a diagonal matrix")
    return num_diag

def invert_matrix(A):
    # invert a diagonal matrix
    num_diag = taking_diagonal(A)
    if num_diag == 0:
        raise ValueError("A must be invertible")
    else:
        return create_matrix(len(A), 1/num_diag, 0)

def taking_triangular_matrix(A):
    T_L, T_U = np.zeros((len(A), len(A))), np.zeros((len(A), len(A)))
    for i in range(len(A)):
        for j in range(len(A)):
            if i < j:
                T_U[i, j] = A[i, j]
            elif i > j:
                T_L[i, j] = A[i, j]
    return T_L, T_U
    
def find_residual(A, x, b):  
    r = np.dot(A, x) - b
    r_mag = 0
    for i in range(len(r)):
        r_mag += abs(r[i])
    return r_mag / len(r)

def jacobi_method(A, b):
    # applying jacobi iterative method to solve Ax = b
    B_inverse = invert_matrix(A)
    T_L, T_U = taking_triangular_matrix(A)
    x_0 = np.dot(B_inverse, b)
    x_previous = x_0
    flag = True
    iterations = 0
    while flag:
        # iterating
        G = np.dot(B_inverse, T_L + T_U)
        x_new = np.dot(B_inverse, b) - np.dot(G, x_previous)
        residual = find_residual(A, x_new, b)
        if residual < 1e-6:
            flag = False
        if iterations > 1000:
            raise ValueError("Method diverges")
            flag = False
        x_previous = x_new
        iterations += 1
    #print('###########################################')
    #print('x = ', x_new)
    #print('b = ', b)
    #print('A dot x = ', np.dot(A, x_new))
    print('used iterations = ', iterations, 'for', len(x_new), 'x', len(x_new), 'matrix')
    #print('###########################################')
    return x_new



A = create_matrix(5, 2, -1)
b = np.array([-1, 0, 0, 0, 5])
#jacobi_method(A, b)
# found to diverge if diagonal is < 1

# now trying 3 for diagonal values, which does converge much faster
A = create_matrix(5, 3, -1)
b = np.array([-1, 0, 0, 0, 5])
#jacobi_method(A, b)

# now trying for arbitrary large matrices
smallest_size = 3
largest_size = 100
print('initiating for arbitrary large matrices', 'from ', smallest_size, 'x', smallest_size, 'to', largest_size, 'x', largest_size)
for i in range(smallest_size, largest_size+1):
    A = create_matrix(i, 4, -1)
    b = np.zeros((i))
    b[0], b[-1] = -1, 5
    jacobi_method(A, b)
print('process run successful')
# iteration required for 3 on the diagonal is stable at around 20 iterations(even for up to 100x100 matrix)
# but for 2 on the diagonal, the number of iterations required grows past 1000 by 20x20 matrix

# eigenvalue of 2 matrix approaches 1 as matrix size increases
# eigenvalue of 3 matrix approaches 0.67 ish as matrix size increases
# eigenvalue decreases as number on the diagonal increases, 4 matrix takes even less iterations than 3 matrix
# the matrix technically have to be diagonally dominant, the more 'dominant' it is the faster it converges

# the iteration process is based on the same idea as binominal expansion which is only valid for |x| < 1, 
# and converges faster as |x| approaches 0. the same idea applies here