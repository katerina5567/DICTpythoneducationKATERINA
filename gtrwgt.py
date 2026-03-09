import sys

# ======= FUNCTIONS =======

def read_matrix_with_size():
    n, m = map(int, input().split())
    matrix = [list(map(float, input().split())) for _ in range(n)]
    return matrix, n, m

def print_matrix(matrix):
    for row in matrix:
        print(*[format(x, ".2f").rstrip('0').rstrip('.') for x in row])

# ----- MATRIX OPERATIONS -----

def add_matrices(a, b):
    if len(a) != len(b) or len(a[0]) != len(b[0]):
        return None
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]

def multiply_by_constant(a, c):
    return [[a[i][j] * c for j in range(len(a[0]))] for i in range(len(a))]

def multiply_matrices(a, b):
    if len(a[0]) != len(b):
        return None
    rows_a = len(a)
    cols_a = len(a[0])
    cols_b = len(b[0])
    result = [[0]*cols_b for _ in range(rows_a)]
    for i in range(rows_a):
        for j in range(cols_b):
            for k in range(cols_a):
                result[i][j] += a[i][k] * b[k][j]
    return result

# ----- TRANSPOSE -----

def transpose_main_diag(a):
    return list(map(list, zip(*a)))

def transpose_side_diag(a):
    n = len(a)
    m = len(a[0])
    return [[a[n-1-j][m-1-i] for j in range(n)] for i in range(m)]

def transpose_vertical(a):
    return [row[::-1] for row in a]

def transpose_horizontal(a):
    return a[::-1]

# ----- DETERMINANT -----

def determinant(a):
    n = len(a)
    if n == 1:
        return a[0][0]
    if n == 2:
        return a[0][0]*a[1][1] - a[0][1]*a[1][0]
    det = 0
    for col in range(n):
        minor = [[a[i][j] for j in range(n) if j != col] for i in range(1, n)]
        det += ((-1)**col) * a[0][col] * determinant(minor)
    return det

# ----- INVERSE -----

def inverse_matrix(a):
    det = determinant(a)
    if det == 0:
        return None
    n = len(a)
    cofactors = []
    for i in range(n):
        row_cof = []
        for j in range(n):
            minor = [[a[r][c] for c in range(n) if c != j] for r in range(n) if r != i]
            row_cof.append(((-1)**(i+j)) * determinant(minor))
        cofactors.append(row_cof)
    adj = transpose_main_diag(cofactors)
    return [[adj[i][j]/det for j in range(n)] for i in range(n)]

# ======= MENU =======

def main():
    while True:
        print("\n1. Add matrices")
        print("2. Multiply matrix by a constant")
        print("3. Multiply matrices")
        print("4. Transpose matrix")
        print("5. Calculate a determinant")
        print("6. Inverse matrix")
        print("0. Exit")
        choice = input("Your choice: > ")

        # ADD MATRICES
        if choice == "1":
            print("Enter size of first matrix: >", end=" ")
            a, _, _ = read_matrix_with_size()
            print("Enter size of second matrix: >", end=" ")
            b, _, _ = read_matrix_with_size()
            res = add_matrices(a, b)
            if res is None:
                print("The operation cannot be performed.")
            else:
                print("The result is:")
                print_matrix(res)

        # MULTIPLY BY CONSTANT
        elif choice == "2":
            print("Enter size of matrix: >", end=" ")
            a, _, _ = read_matrix_with_size()
            c = float(input("Enter constant: > "))
            print("The result is:")
            print_matrix(multiply_by_constant(a, c))

        # MULTIPLY MATRICES
        elif choice == "3":
            print("Enter size of first matrix: >", end=" ")
            a, _, _ = read_matrix_with_size()
            print("Enter size of second matrix: >", end=" ")
            b, _, _ = read_matrix_with_size()
            res = multiply_matrices(a, b)
            if res is None:
                print("The operation cannot be performed.")
            else:
                print("The result is:")
                print_matrix(res)

        # TRANSPOSE
        elif choice == "4":
            print("1. Main diagonal")
            print("2. Side diagonal")
            print("3. Vertical line")
            print("4. Horizontal line")
            t = input("Your choice: > ")
            print("Enter matrix size: >", end=" ")
            a, _, _ = read_matrix_with_size()
            if t == "1":
                res = transpose_main_diag(a)
            elif t == "2":
                res = transpose_side_diag(a)
            elif t == "3":
                res = transpose_vertical(a)
            elif t == "4":
                res = transpose_horizontal(a)
            else:
                print("Invalid option.")
                continue
            print("The result is:")
            print_matrix(res)

        # DETERMINANT
        elif choice == "5":
            print("Enter matrix size: >", end=" ")
            a, _, _ = read_matrix_with_size()
            print("The result is:")
            print(int(determinant(a)))

        # INVERSE MATRIX
        elif choice == "6":
            print("Enter matrix size: >", end=" ")
            a, _, _ = read_matrix_with_size()
            inv = inverse_matrix(a)
            if inv is None:
                print("This matrix doesn't have an inverse.")
            else:
                print("The result is:")
                print_matrix(inv)

        # EXIT
        elif choice == "0":
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()
