# 12.10.2023
import numpy as np
import matplotlib.pyplot as plt

# LU decompusition, choosing deolittle's method

A = np.array([[5, 4, 3, 2, 1], [4, 8, 6, 4, 2], [
             3, 6, 9, 6, 3], [2, 4, 6, 8, 4], [1, 2, 3, 4, 5]])
A = A/6
b = np.array([0, 1, 2, 3, 4])


class LU():
    def decomposation(self, A):

        # checking if A is square
        shape = np.shape(A)
        if len(shape) != 2:
            raise ValueError("A must be 2-dimensional")
        if shape[0] != shape[1]:
            raise ValueError("A must be square")

        # initializing L and U
        dimension = shape[0]
        L = np.zeros(shape)
        U = np.zeros(shape)

        # calculating first rows as they are obvious and allows calculation of the rest
        L_0 = np.zeros(dimension)
        L_0[0] = 1
        L[0] = L_0
        U[0] = A[0]

        # decomposing A into L and U
        for i in range(1, dimension):
            for j in range(dimension):
                A_ij = A[i, j]
                U_sum = 0
                for k in range(i+1):
                    U_sum += L[i, k] * U[k, j]

                if i <= j:
                    U[i, j] = A_ij - U_sum
                else:
                    U[i, j] = 0

                L_sum = 0
                if i < j:
                    L[i, j] = 0
                elif i == j:
                    L[i, j] = 1
                else:
                    for k in range(j+1):
                        L_sum += L[i, k] * U[k, j]
                    L[i, j] = (A_ij - L_sum) / U[j, j]

        # printing L and U
        print("L = \n", L)
        print("\nU = \n", U)

        # checking by taking inner product
        decomposed_A = np.matmul(L, U)
        print('\nexpected \n', A, '\n\n got \n', decomposed_A)

        # storing the values
        self.U = U
        self.L = L

    def solve(self, b):

        # solving for y, only solving for L
        dimension = len(b)
        self.dimension = dimension
        self.b = b
        y = np.zeros((dimension))
        y[0] = b[0]/self.L[0, 0]
        for i in range(1, dimension):
            y_sum = 0
            for j in range(i):
                y_sum += self.L[i, j] * y[j]
            y[i] = (b[i] - y_sum) / self.L[i, i]
        self.y = y
        print('\ny = ', y)

        # solving for x, solving U on y
        x = np.zeros((dimension))
        x[-1] = y[-1] / self.U[-1, -1]
        for i in range(dimension-2, -1, -1):
            x_sum = 0
            for j in range(i+1, dimension):
                x_sum += self.U[i, j] * x[j]
            x[i] = (y[i] - x_sum) / self.U[i, i]
        self.x = x
        print('\nx = ', x)

    def residual(self):
        # calculating the residual, matrix and magnitude
        r = np.matmul(A, self.x) - self.b
        print('\nr = ', r)
        r_mag = 0
        for i in range(self.dimension):
            r_mag += abs(r[i]) / self.dimension
        print('\nr_mag = ', r_mag)


# running the decomposation
M = LU()
M.decomposation(A)
M.solve(b)
M.residual()
