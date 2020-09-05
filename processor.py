MENU = """
1. Add matrices
2. Multiply matrix by a constant
3. Multiply matrices
4. Transpose matrix
5. Calculate a determinant
6. Inverse matrix
0. Exit
Your choice: > """

TRANSPONSE = """
1. Main diagonal
2. Side diagonal
3. Vertical line
4. Horizontal line
Your choice: > """


class Matrix:

    def __init__(self, rows=None, columns=None, number=""):
        try:
            self.matrix = False
            if rows and columns:
                self.row, self.column = rows, columns
                self.matrix = [[0] * columns for _ in range(rows)]
            else:
                row, column = input(f"Enter size of {number}matrix: > ").split()
                self.row = int(row)
                self.column = int(column)
        except (ValueError, TypeError):
            print("expected 2 numbers")
        else:
            if not rows and not columns:
                self.matrix = self.init_matrix(number)

    def init_matrix(self, number):
        new_matrix = list()
        print(f"Enter {number}matrix:")
        for _n in range(self.row):
            row = [float(num) if "." in num else int(num) for num in input("> ").split()]
            if len(row) != self.column:
                return False
            new_matrix.append(row)
        return new_matrix

    def multiply_const_matrix(self):
        const = input("Enter constant: > ")
        const = float(const) if "." in const else int(const)
        matrix = [[const * column for column in row] for row in self.matrix]
        return matrix

    def transposition_main_diagonal(self):
        matrix = list()
        for column in range(self.column):
            matrix.append([])
            for row in range(self.row):
                matrix[column].append(self.matrix[row][column])
        # matrix = [[self.matrix[m][n] for m in range(self.row)] for n in range(self.column)]
        return matrix

    def transposition_side_diagonal(self):
        row = self.row - 1
        column = self.column - 1
        matrix = [[self.matrix[row - m][column - n] for m in range(self.row)] for n in range(self.column)]
        return matrix

    def transposition_vertical_line(self):
        column = self.column - 1
        matrix = [[self.matrix[n][column - m] for m in range(self.column)] for n in range(self.row)]
        return matrix

    def transposition_horizontal_line(self):
        row = self.row - 1
        matrix = [[self.matrix[row - n][m] for m in range(self.column)] for n in range(self.row)]
        return matrix

    @staticmethod
    def get_minor_matrix(matrix, size, row, column):
        # new_matrix = [[0] * size for _ in range(size)]
        minor = Matrix(rows=size, columns=size)
        shift_row = 0
        for n in range(size):
            if n == row:
                shift_row = 1
            shift_column = 0
            for m in range(size):
                if m == column:
                    shift_column = 1
                minor.matrix[n][m] = matrix[n + shift_row][m + shift_column]
        return minor.matrix

    def calculate_determinant(self, matrix, size):
        det = 0
        sign = 1
        if size == 1:
            return matrix[0][0]
        elif size == 2:
            det = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
            return det
        else:
            for column in range(size):
                minor = self.get_minor_matrix(matrix, size - 1, 0, column)
                det += (sign * matrix[0][column] * self.calculate_determinant(minor, size - 1))
                sign = -sign
            return det

    def cofactor_matrix(self):
        cofactor = Matrix(rows=self.row, columns=self.row)
        for row in range(self.row):
            sign = 1 if (row % 2) == 0 else -1
            for column in range(self.column):
                minor = self.get_minor_matrix(self.matrix, self.row - 1, row, column)
                cofactor.matrix[row][column] = sign * self.calculate_determinant(minor, self.row - 1)
                sign *= -1
        return cofactor.matrix

    # def inverse_matrix(self, det):
    #     det = 1 / det
    #     self.matrix = self.cofactor_matrix()
    #     self.matrix = self.transposition_main_diagonal()
    #     self.matrix = [[int(det * column * 100) / 100 for column in row] for row in self.matrix]
    #     return self.matrix

    def inverse_matrix(self, det):
        det = 1 / det
        inverse = Matrix(rows=self.row, columns=self.row)
        inverse.matrix = self.cofactor_matrix()
        inverse.matrix = inverse.transposition_main_diagonal()
        inverse.matrix = [[int(det * column * 100) / 100 for column in row] for row in inverse.matrix]
        return inverse.matrix


def add_matrices(A, B):
    matrix = list()
    for row in range(A.row):
        matrix.append([])
        for column in range(A.column):
            matrix[row].append(A.matrix[row][column] + B.matrix[row][column])
    # matrix = [[(A.matrix[n][m] + B.matrix[n][m]) for m in range(A.column)] for n in range(A.row)]
    return matrix


def multiply_matrices(A, B):
    matrix = list()
    for k in range(A.row):
        matrix.append([])
        for m in range(B.column):
            c = 0
            for n in range(B.row):
                c += A.matrix[k][n] * B.matrix[n][m]
            matrix[k].append(c)
    return matrix


def print_matrix(matrix):
    print("The result is:")
    for row in matrix:
        print(' '.join([str(elem) for elem in row]))


def transpose_matrix():
    new_choice = input(TRANSPONSE)
    A = Matrix()
    if A.matrix:
        if new_choice == "1":
            print_matrix(A.transposition_main_diagonal())
        if new_choice == "2":
            print_matrix(A.transposition_side_diagonal())
        if new_choice == "3":
            print_matrix(A.transposition_vertical_line())
        if new_choice == "4":
            print_matrix(A.transposition_horizontal_line())
    else:
        print("The operation cannot be performed.")


def main():
    while True:
        choice = input(MENU)
        if choice == "0":
            break
        elif choice == "1" or choice == "3":
            A = Matrix(number="first ")
            B = Matrix(number="second ")
            if A.matrix and B.matrix:
                if choice == "1" and A.row == B.row and A.column == B.column:
                    print_matrix(add_matrices(A, B))
                elif choice == "3" and A.column == B.row:
                    print_matrix(multiply_matrices(A, B))
                else:
                    print("The operation cannot be performed.")
            else:
                print("These matrices not initialized.")
        elif choice == "2" or choice == "5" or choice == "6":
            A = Matrix()
            if A.matrix:
                if choice == "2":
                    print_matrix(A.multiply_const_matrix())
                elif choice == "5" and A.row == A.column:
                    det = A.calculate_determinant(A.matrix, A.row)
                    print(f"The result is:\n{det}")
                elif choice == "6" and A.row == A.column:
                    det = A.calculate_determinant(A.matrix, A.row)
                    if det != 0:
                        print_matrix(A.inverse_matrix(det))
                    else:
                        print("This matrix doesn't have an inverse.")
                else:
                    print("The operation cannot be performed.")
            else:
                print("This matrix is not initialized.")
        elif choice == "4":
            transpose_matrix()
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
