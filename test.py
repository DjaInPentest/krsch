import random
import tkinter as tk

def generate_sudoku():
    sudoku = [[0] * 9 for _ in range(9)]

    def is_valid(num, row, col):
        for i in range(9):
            if sudoku[row][i] == num or sudoku[i][col] == num:
                return False

        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if sudoku[i + start_row][j + start_col] == num:
                    return False

        return True

    def solve_sudoku():
        for row in range(9):
            for col in range(9):
                if sudoku[row][col] == 0:
                    nums = list(range(1, 10))
                    random.shuffle(nums)
                    for num in nums:
                        if is_valid(num, row, col):
                            sudoku[row][col] = num
                            if solve_sudoku():
                                return True
                            sudoku[row][col] = 0
                    return False
        return True

    solve_sudoku()
    return sudoku

class SudokuGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku")
        self.sudoku = None
        self.create_puzzle('easy')

    def create_puzzle(self, difficulty):
        if difficulty == 'easy':
            num_cells_to_remove = 30
        elif difficulty == 'medium':
            num_cells_to_remove = 40
        else:
            num_cells_to_remove = 50

        self.sudoku = generate_sudoku()

        # Remove cells to create the puzzle
        cells = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(cells)

        for _ in range(num_cells_to_remove):
            i, j = cells.pop()
            self.sudoku[i][j] = 0

        self.create_grid()

    def create_grid(self):
        self.entries = []
        for i in range(9):
            row = []
            for j in range(9):
                cell_value = self.sudoku[i][j]
                if cell_value == 0:
                    entry = tk.Entry(self.root, width=2, font=('Helvetica', 16))
                    entry.grid(row=i, column=j)
                    row.append(entry)
                else:
                    label = tk.Label(self.root, text=str(cell_value), font=('Helvetica', 16))
                    label.grid(row=i, column=j)
                    row.append(label)
            self.entries.append(row)

    def reset_puzzle(self):
        for row in self.entries:
            for cell in row:
                cell.grid_forget()
        self.create_puzzle('easy')


root = tk.Tk()
game = SudokuGame(root)
menu = tk.Menu(root)
root.config(menu=menu)
difficulty_menu = tk.Menu(menu)
menu.add_cascade(label="Difficulty", menu=difficulty_menu)
difficulty_menu.add_command(label="Easy", command=lambda: game.create_puzzle('easy'))
difficulty_menu.add_command(label="Medium", command=lambda: game.create_puzzle('medium'))
difficulty_menu.add_command(label="Hard", command=lambda: game.create_puzzle('hard'))
difficulty_menu.add_separator()
difficulty_menu.add_command(label="New Puzzle", command=game.reset_puzzle)

root.mainloop()
