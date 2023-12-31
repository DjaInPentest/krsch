import random
import tkinter as tk
import pickle
import time
from tkinter import messagebox

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
        self.root.title("Судоку")
        self.sudoku = None
        self.solution = None
        self.root.resizable(False, False)  # Блокируем изменение размеров по обеим осям.
        self.errors_count = 0  # Добавляем счетчик ошибок.
        self.create_puzzle('easy')
        self.create_buttons()
        self.root.configure(bg='black')  # Set a dark background
    def create_puzzle(self, difficulty):
        if difficulty == 'easy':
            num_cells_to_remove = 30
        elif difficulty == 'medium':
            num_cells_to_remove = 40
        else:
            num_cells_to_remove = 50
        self.sudoku = generate_sudoku()
        self.solution = [row[:] for row in self.sudoku]

        cells = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(cells)

        for _ in range(num_cells_to_remove):
            i, j = cells.pop()
            self.sudoku[i][j] = 0

        self.create_grid()
    def create_grid(self):
        for widget in self.root.winfo_children():
            widget.grid_remove()
        self.entries = []
        for i in range(9):
            row = []
            for j in range(9):
                cell_value = self.sudoku[i][j]
                if cell_value == 0:
                    entry = tk.Entry(self.root, width=2, font=('Helvetica', 16), bg='black', fg='white')
                    entry.grid(row=i, column=j)
                    entry.bind('<KeyRelease>', lambda event, row=i, col=j: self.validate_entry(event, row, col))
                    row.append(entry)
                else:
                    label = tk.Label(self.root, text=str(cell_value), font=('Helvetica', 16), bg='black', fg='white')
                    label.grid(row=i, column=j)
                    row.append(label)
            self.entries.append(row)

        validate_button = tk.Button(self.root, text="Проверить", command=self.check_solution, bg="violet", fg="white")
        validate_button.grid(row=9, column=0, columnspan=3)
        new_game_button = tk.Button(self.root, text="Новая игра", command=self.reset_puzzle, bg="violet", fg="white")
        new_game_button.grid(row=9, column=3, columnspan=3)
        save_button = tk.Button(self.root, text="Сохранить", command=self.save_game, bg="violet", fg="white")
        save_button.grid(row=9, column=6, columnspan=3)

    def create_buttons(self):
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)
        difficulty_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Сложность", menu=difficulty_menu)
        difficulty_menu.add_command(label="Легко", command=lambda: self.create_puzzle('easy'))
        difficulty_menu.add_command(label="Средне", command=lambda: self.create_puzzle('medium'))
        difficulty_menu.add_command(label="Сложно", command=lambda: self.create_puzzle('hard'))
        difficulty_menu.add_separator()
        load_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Загрузить", menu=load_menu)
        load_menu.add_command(label="Загрузить игру", command=self.load_game)
        
    def validate_entry(self, event, row, col):
        entry_value = self.entries[row][col].get()
        if entry_value.isdigit() and 1 <= int(entry_value) <= 9:
            self.sudoku[row][col] = int(entry_value)
            self.entries[row][col].configure(bg='red', fg='white')
        if self.sudoku[row][col] == self.solution[row][col]:
            self.entries[row][col].configure(bg='green', fg='white')

        else:
            if event.keysym in ('1', '2', '3', '4', '5', '6', '7', '8', '9'):
            	self.sudoku[row][col] = 0
            	self.entries[row][col].configure(bg='red', fg='white')
            	self.errors_count += 1  # Увеличиваем счетчик ошибок
            	messagebox.showinfo("Вы совершили ошибку!", f"Ошибок: {self.errors_count}")
            	if self.errors_count >= 3:
            		messagebox.showinfo("Поражение", "Вы проиграли! Попробуйте начать новую игру!")

    def validate_solution(self):
        for i in range(9):
            for j in range(9):
                if self.sudoku[i][j] != self.solution[i][j]:
                    return False
        return True

    def check_solution(self):
        for i in range(9):
            for j in range(9):
                entry = self.entries[i][j]
                if self.sudoku[i][j] == 0:
                    if entry.get().isdigit() and int(entry.get()) == self.solution[i][j]:
                        entry.configure(bg='green', fg='white')
                    else:
                        entry.configure(bg='red', fg='white')
        if self.validate_solution():
            for i in range(9):
                for j in range(9):
                    entry = self.entries[i][j]
                    entry.configure(bg='green', fg='white')
            messagebox.showinfo("Поздравляем", "Вы решили головоломку!")
        else:
            pass

    def reset_puzzle(self):
        for row in self.entries:
            for cell in row:
                cell.grid_forget()
        self.errors_count = 0
        self.create_puzzle('easy')

    def save_game(self):
    # Создаем копию текущего состояния sudoku для проверки значений
        current_state = [row[:] for row in self.sudoku]

        for i in range(9):
            for j in range(9):
            # Если значение в клетке не соответствует решению, устанавливаем его как 0
                if self.sudoku[i][j] != self.solution[i][j]:
                    self.sudoku[i][j] = 0

        game_state = {
            "sudoku": self.sudoku,
            "solution": self.solution
        }
        with open("sudoku_game_state.pkl", "wb") as f:
            pickle.dump(game_state, f)

    # Возвращаем исходное состояние sudoku
        self.sudoku = current_state

    def load_game(self):
        try:
            with open("sudoku_game_state.pkl", "rb") as f:
                game_state = pickle.load(f)

            self.sudoku = game_state["sudoku"]
            self.solution = game_state["solution"]
            self.create_grid()
        except:
            messagebox.showinfo("Ой ой...", "Сохранение повреждено, либо не существует!")
            self.reset_puzzle() #Обработка ввода дурака. 
