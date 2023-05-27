import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import ImageTk, Image

def solve_sudoku(board):
    empty_cells = find_empty_cells(board)
    if not empty_cells:
        return True

    row, col = empty_cells[-1]

    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num

            if solve_sudoku(board):
                return True

            board[row][col] = 0

    return False

def is_solved(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                return False
    return True

def find_empty_cells(board):
    empty_cells = []
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                empty_cells.append((row, col))
    return empty_cells

def is_valid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False

    start_row = (row // 3) * 3
    start_col = (col // 3) * 3

    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False

    return True

def is_valid_puzzle(board):
    for row in range(9):
        for col in range(9):
            num = board[row][col]
            if num != 0:
                board[row][col] = 0  # Temporarily set the cell to 0
                if not is_valid(board, row, col, num):
                    board[row][col] = num  # Restore the original number
                    return False
                board[row][col] = num  # Restore the original number
    return True


def is_row_valid(board, row, num):
    for col in range(9):
        if board[row][col] == num:
            return False
    return True

def is_col_valid(board, col, num):
    for row in range(9):
        if board[row][col] == num:
            return False
    return True

def is_box_valid(board, start_row, start_col, num):
    for row in range(3):
        for col in range(3):
            if board[row + start_row][col + start_col] == num:
                return False
    return True


def solve_button_click():
    # Get the puzzle from the input cells
    puzzle = []
    for row in range(9):
        puzzle.append([])
        for col in range(9):
            input_value = input_cells[row][col].get()
            if input_value == "":
                puzzle[row].append(0)
            else:
                try:
                    num = int(input_value)
                    if num < 1 or num > 9:
                        raise ValueError
                    puzzle[row].append(num)
                except ValueError:
                    messagebox.showerror("Invalid Input", "Please enter valid numbers (1-9) or leave empty cells.")
                    return

    # Check if the puzzle is valid
    if not is_valid_puzzle(puzzle):
        messagebox.showerror("Invalid Sudoku", "Please input a valid Sudoku puzzle.")
        return

    # Solve the Sudoku puzzle
    solve_sudoku(puzzle)

    # Display the solved puzzle
    for row in range(9):
        for col in range(9):
            input_cells[row][col].delete(0, tk.END)
            input_cells[row][col].insert(0, puzzle[row][col])


def reset_button_click():
    # Clear all input cells
    for row in range(9):
        for col in range(9):
            input_cells[row][col].delete(0, tk.END)

def load_puzzle():
    selected_puzzle = puzzle_dropdown.get()

    if selected_puzzle in puzzle_options:
        puzzle = puzzle_options[selected_puzzle]

        # Clear the input cells
        for row in range(9):
            for col in range(9):
                input_cells[row][col].delete(0, tk.END)
                if puzzle[row][col] != 0:
                    input_cells[row][col].insert(0, puzzle[row][col])

# Create the main window
window = tk.Tk()
window.title("Sudoku Solver")
window.configure(bg='white')

# Use a specific theme
style = ttk.Style()
style.theme_use('clam')

# Load solve icon
solve_icon = Image.open("solve_icon.png").resize((24, 24))
solve_image = ImageTk.PhotoImage(solve_icon)

# Create the input cells for the Sudoku puzzle
input_cells = []
for row in range(9):
    input_cells.append([])
    for col in range(9):
        def validate_input(value):
            if value in ["", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                return True
            else:
                return False

        validation = window.register(validate_input)
        input_cell = tk.Entry(window, width=3, font=("Helvetica", 20), validate="key", validatecommand=(validation, "%P"))
        input_cell.grid(row=row, column=col, padx=2, pady=2)
        input_cells[row].append(input_cell)

        # Add some styling to the input cells
        if (row < 3 or row > 5) and (col < 3 or col > 5):
            input_cell.configure(bg='lightgray')
        elif 2 < row < 6 and 2 < col < 6:
            input_cell.configure(bg='lightgray')
        else:
            input_cell.configure(bg='white')

# Create the solve button
solve_button = ttk.Button(window, text="Solve", command=solve_button_click, image=solve_image, compound=tk.LEFT)
solve_button.grid(row=9, column=0, columnspan=4, padx=10, pady=10)

# Create the reset button
reset_button = ttk.Button(window, text="Reset", command=reset_button_click)
reset_button.grid(row=9, column=5, columnspan=4, padx=10, pady=10)

# Disable window resizing
window.resizable(0, 0)

# Add some styling to the buttons
style.configure('TButton', font=('Helvetica', 14), padding=10, width=10)
style.map('TButton', foreground=[('pressed', 'white'), ('active', 'blue')], background=[('pressed', '!disabled', 'blue'), ('active', 'lightgray')])

# Define the puzzle options
puzzle_options = {
    "Easy": [
        [1, 0, 3, 4, 8, 0, 2, 7, 6],
        [2, 0, 5, 0, 0, 0, 9, 0, 0],
        [6, 0, 4, 9, 1, 2, 0, 5, 8],
        [0, 0, 0, 0, 9, 8, 4, 0, 7],
        [0, 2, 0, 3, 0, 0, 0, 0, 0],
        [4, 0, 0, 0, 0, 0, 0, 8, 3],
        [0, 4, 0, 0, 2, 3, 0, 6, 0],
        [9, 6, 0, 8, 5, 0, 0, 0, 0],
        [8, 0, 0, 0, 0, 0, 7, 0, 0]
    ],
    "Medium": [
        [0, 0, 8, 0, 0, 0, 5, 0, 0],
        [0, 6, 3, 0, 0, 0, 0, 0, 9],
        [4, 1, 5, 0, 0, 9, 0, 7, 0],
        [0, 0, 0, 1, 3, 0, 0, 8, 0],
        [8, 0, 0, 9, 0, 0, 2, 0, 7],
        [0, 0, 0, 0, 0, 0, 6, 0, 0],
        [0, 5, 0, 6, 0, 0, 8, 3, 0],
        [0, 0, 0, 8, 1, 0, 0, 0, 0],
        [2, 0, 4, 3, 0, 7, 1, 9, 0]
    ],
    "Hard": [
        [0, 0, 0, 0, 6, 0, 0, 0, 1],
        [0, 0, 7, 0, 0, 0, 0, 0, 5],
        [6, 0, 1, 0, 0, 0, 3, 0, 0],
        [0, 0, 0, 2, 0, 0, 1, 9, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 9, 2, 0, 0, 6, 0, 0, 0],
        [0, 0, 9, 0, 0, 0, 2, 0, 3],
        [7, 0, 0, 0, 0, 0, 8, 0, 0],
        [3, 0, 0, 0, 4, 0, 0, 0, 0]
    ],
"Expert": [
    [8, 5, 0, 0, 0, 2, 4, 0, 0],
    [7, 2, 0, 0, 0, 0, 0, 0, 9],
    [0, 0, 4, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 7, 0, 0, 2],
    [3, 0, 5, 0, 0, 0, 9, 0, 0],
    [0, 4, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 8, 0, 0, 7, 0],
    [0, 1, 7, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 3, 6, 0, 4, 0]
    ]
}

# Create the puzzle dropdown menu
puzzle_dropdown = tk.StringVar(window)
puzzle_dropdown.set("Select Puzzle")
puzzle_dropdown.trace("w", lambda *args: load_puzzle())  # Updated line
puzzle_menu = tk.OptionMenu(window, puzzle_dropdown, *puzzle_options.keys())
puzzle_menu.config(font=("Helvetica", 14))
puzzle_menu.grid(row=10, column=0, columnspan=9, padx=10, pady=10, sticky="ew")

# Run the GUI main loop
window.mainloop()
