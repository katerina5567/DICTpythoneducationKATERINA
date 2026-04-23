def read_matrix():
    n, m = map(float, input().split())
    n, m = int(n), int(m)
    matrix = [list(map(float, input().split())) for _ in range(n)]
    return matrix


def read_matrix_with_size():
    n, m = map(int, input().split())
    matrix = [list(map(float, input().split())) for _ in range(n)]
    return matrix, n, m


def print_matrix(matrix):
    for row in matrix:
        print(*[format(x, ".2f").rstrip('0').rstrip('.') if '.' in format(x, ".2f") else int(x) for x in row])


# ---------- MATRIX OPERATIONS ----------

def add_matrices(a, b):
    if len(a) != len(b) or len(a[0]) != len(b[0]):
        return None

    result = []
    for i in range(len(a)):
        row = []
        for j in range(len(a[0])):
            row.append(a[i][j] + b[i][j])
        result.append(row)

    return result


def multiply_by_constant(a, c):
    return [[a[i][j] * c for j in range(len(a[0]))] for i in range(len(a))]


def multiply_matrices(a, b):
    if len(a[0]) != len(b):
        return None

    rows_a = len(a)
    cols_a = len(a[0])
    cols_b = len(b[0])

    result = [[0] * cols_b for _ in range(rows_a)]

    for i in range(rows_a):
        for j in range(cols_b):
            for k in range(cols_a):
                result[i][j] += a[i][k] * b[k][j]

    return result


# ---------- TRANSPOSITIONS ----------

def transpose_main_diag(a):
    return list(map(list, zip(*a)))


def transpose_side_diag(a):
    n = len(a)
    m = len(a[0])
    return [[a[n - 1 - j][m - 1 - i] for j in range(n)] for i in range(m)]


def transpose_vertical(a):
    return [row[::-1] for row in a]


def transpose_horizontal(a):
    return a[::-1]


# ---------- DETERMINANT ----------

def determinant(a):
    n = len(a)

    if n == 1:
        return a[0][0]

    if n == 2:
        return a[0][0] * a[1][1] - a[0][1] * a[1][0]

    det = 0
    for col in range(n):
        minor = []
        for i in range(1, n):
            row = []
            for j in range(n):
                if j != col:
                    row.append(a[i][j])
            minor.append(row)
        det += ((-1) ** col) * a[0][col] * determinant(minor)

    return det


# ---------- INVERSE MATRIX ----------

def inverse_matrix(a):
    det = determinant(a)
    if det == 0:
        return None

    n = len(a)

    cofactors = []
    for i in range(n):
        row_cof = []
        for j in range(n):
            minor = []
            for r in range(n):
                if r != i:
                    row = []
                    for c in range(n):
                        if c != j:
                            row.append(a[r][c])
                    minor.append(row)
            row_cof.append(((-1) ** (i + j)) * determinant(minor))
        cofactors.append(row_cof)

    adj = transpose_main_diag(cofactors)
    inv = [[adj[i][j] / det for j in range(n)] for i in range(n)]

    return inv


# ---------- MENU ----------

def main():
    while True:
        print("1. Add matrices")
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
            a, n1, m1 = read_matrix_with_size()
            print("Enter first matrix:")
            # a already read

            print("Enter size of second matrix: >", end=" ")
            b, n2, m2 = read_matrix_with_size()
            print("Enter second matrix:")

            res = add_matrices(a, b)

            if res is None:
                print("The operation cannot be performed.")
            else:
                print("The result is:")
                print_matrix(res)

        # MULTIPLY BY CONSTANT
        elif choice == "2":
            print("Enter size of matrix: >", end=" ")
            a, n, m = read_matrix_with_size()

            print("Enter matrix:")
            # matrix already read

            c = float(input("Enter constant: > "))

            print("The result is:")
            print_matrix(multiply_by_constant(a, c))

        # MULTIPLY MATRICES
        elif choice == "3":
            print("Enter size of first matrix: >", end=" ")
            a, n1, m1 = read_matrix_with_size()
            print("Enter first matrix:")

            print("Enter size of second matrix: >", end=" ")
            b, n2, m2 = read_matrix_with_size()
            print("Enter second matrix:")

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
            a, n, m = read_matrix_with_size()
            print("Enter matrix:")

            if t == "1":
                res = transpose_main_diag(a)
            elif t == "2":
                res = transpose_side_diag(a)
            elif t == "3":
                res = transpose_vertical(a)
            elif t == "4":
                res = transpose_horizontal(a)
            else:
                res = None

            print("The result is:")
            print_matrix(res)

        # DET
        elif choice == "5":
            print("Enter matrix size: >", end=" ")
            a, n, m = read_matrix_with_size()
            print("Enter matrix:")

            print("The result is:")
            print(int(determinant(a)))

        # INVERSE MATRIX
        elif choice == "6":
            print("Enter matrix size: >", end=" ")
            a, n, m = read_matrix_with_size()
            print("Enter matrix:")

            inv = inverse_matrix(a)

            if inv is None:
                print("This matrix doesn't have an inverse.")
            else:
                print("The result is:")
                print_matrix(inv)

        # EXIT
        elif choice == "0":
            break


if __name__ == "__main__":
    main()
