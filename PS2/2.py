# 14.10.2023
import numpy as np
import matplotlib.pyplot as plt


class M():
    def __init__(self, dimension, num):
        self.G = np.zeros((dimension, dimension))
        self.v = np.linspace(0, dimension-1, dimension)
        for i in range(dimension):
            if i == 0:
                self.G[0, 1] = num
            elif i == dimension-1:
                self.G[i, -2] = num
            else:
                self.G[i, i-1], self.G[i, i+1] = num, num

    def find_largest_eigenvalue(self):
        n = 1
        old_eigenvalue = 0
        old_difference = np.inf
        while True:
            product = self.G@self.v
            w_j = product / np.linalg.norm(product)
            new_eigenvalue = w_j.T@self.G@w_j
            new_difference = abs(new_eigenvalue - old_eigenvalue)
            if new_difference < 1e-4:
                self.eigenvalue = new_eigenvalue
                print('The largest eigenvalue is', new_eigenvalue)
                break
            if old_difference < new_difference:
                print('Method of powers to find the largest eigenvalue diverges')
                break
            old_eigenvalue = new_eigenvalue
            old_difference = new_difference
            n += 1


# for a 5x5 matrix
G = M(5, -1/2)
G.find_largest_eigenvalue()

# now trying for arbitrary large matrices
x = list(range(3, 60))
y = []
for i in x:
    G = M(i, -1/2)
    print('for ', i, 'x', i, 'matrix, ')
    G.find_largest_eigenvalue()
    y.append(G.eigenvalue)
plt.xlabel('size of the 2D matrix')
plt.ylabel('largest eigenvalue')
plt.plot(x, y, label='for -1/2')

# if doing the same but for -1/3 instead of -1/2
x = list(range(3, 60))
y = []
for i in x:
    G = M(i, -1/3)
    print('for ', i, 'x', i, 'matrix, ')
    G.find_largest_eigenvalue()
    y.append(G.eigenvalue)
plt.xlabel('size of the 2D matrix')
plt.ylabel('largest eigenvalue')
plt.plot(x, y, label='for -1/3')
plt.legend()
plt.grid()
plt.show()
