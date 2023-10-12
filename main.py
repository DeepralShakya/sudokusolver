import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import ImageTk, Image
import time
import random


selected_cell = None
current_row = 0
current_col = 0
start_time = None
elapsed_time = 0

def select_cell(row, col):
    global selected_cell, current_row, current_col

    # Reset the background color of the previously selected cell
    if selected_cell is not None:
        prev_row, prev_col = selected_cell
        if (prev_row < 3 or prev_row > 5) and (prev_col < 3 or prev_col > 5):
            input_cells[prev_row][prev_col].configure(bg='lightgray')
        elif 2 < prev_row < 6 and 2 < prev_col < 6:
            input_cells[prev_row][prev_col].configure(bg='lightgray')
        else:
            input_cells[prev_row][prev_col].configure(bg='white')

    # Update the selected cell and change its background color
    selected_cell = (row, col)
    input_cells[row][col].configure(bg='lightblue')

    # Update the current position
    current_row, current_col = row, col

    # Set focus to the selected cell for input
    input_cells[row][col].focus()

def move_cell(event):
    global current_row, current_col

    # Get the current position of the selected cell
    row, col = current_row, current_col

    # Handle arrow key events
    if event.keysym == 'Up':
        row = (row - 1) % 9  # Move up and wrap around to the last row
    elif event.keysym == 'Down':
        row = (row + 1) % 9  # Move down and wrap around to the first row
    elif event.keysym == 'Left':
        col = (col - 1) % 9  # Move left and wrap around to the last column
    elif event.keysym == 'Right':
        col = (col + 1) % 9  # Move right and wrap around to the first column

    # Check if the new position is within the grid bounds
    if 0 <= row < 9 and 0 <= col < 9:
        select_cell(row, col)
        current_row, current_col = row, col


def solve_sudoku(board):
    empty_cells = find_empty_cells(board)
    if not empty_cells:
        return

    row, col = empty_cells[-1]

    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num

            solve_sudoku(board)

            if is_solved(board):  # Add a check for a solved puzzle
                return

            board[row][col] = 0


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
    global selected_cell, start_time, elapsed_time
    if start_time is not None:
        elapsed_time = time.time() - start_time
        start_time = None

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

    # Check if the puzzle is solved
    if is_solved(puzzle):

        # Format the solving time
        solving_time_formatted = "{:.2f} seconds".format(elapsed_time)

        # Display a message with the solving time
        messagebox.showinfo("Puzzle Solved", "Puzzle solved in {}".format(solving_time_formatted))

def reset_button_click():
    # Clear all input cells
    global selected_cell, start_time, elapsed_time
    start_time = None
    elapsed_time = 0
    for row in range(9):
        for col in range(9):
            input_cells[row][col].delete(0, tk.END)

# Function to generate a valid Sudoku puzzle
def generate_valid_puzzle():
    grid = [[0] * 9 for _ in range(9)]

    solve_sudoku(grid)

    return grid

def shuffle_puzzle(grid):
    numbers = list(range(1, 10))
    random.shuffle(numbers)

    # Create a dictionary to map old numbers to new numbers
    number_mapping = {i + 1: numbers[i] for i in range(9)}

    # Apply the number mapping to the puzzle grid
    shuffled_grid = [[number_mapping[num] if num != 0 else 0 for num in row] for row in grid]

    return shuffled_grid


# Function to generate a new puzzle based on difficulty
def generate_puzzle(difficulty):
    valid_puzzle = generate_valid_puzzle()

    if difficulty == "Easy":
        cells_to_remove = random.randint(40, 45)
    elif difficulty == "Medium":
        cells_to_remove = random.randint(46, 51)
    elif difficulty == "Hard":
        cells_to_remove = random.randint(52, 55)
    else:
        return None

    puzzle_grid = [row[:] for row in valid_puzzle]  # Create a copy of the valid puzzle

    # Count the number of cells removed
    cells_removed = 0

    while cells_removed < cells_to_remove:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        if puzzle_grid[row][col] != 0:
            puzzle_grid[row][col] = 0
            cells_removed += 1

    return puzzle_grid

def load_puzzle():
    global start_time
    start_time = time.time()

    selected_puzzle = puzzle_dropdown.get()

    puzzle = generate_puzzle(selected_puzzle)

    if puzzle is None:
        messagebox.showerror("Invalid Puzzle", "Please select a valid puzzle option.")
        return

    # Shuffle the numbers within the generated puzzle
    shuffled_puzzle = shuffle_puzzle(puzzle)

    # Clear the input cells and display the shuffled puzzle
    for row in range(9):
        for col in range(9):
            input_cells[row][col].delete(0, tk.END)
            if shuffled_puzzle[row][col] != 0:
                input_cells[row][col].insert(0, shuffled_puzzle[row][col])

    # Set the initial selected cell
    select_cell(current_row, current_col)




def update_timer():
    global start_time, elapsed_time
    if start_time is not None:
        elapsed_time = time.time() - start_time
    timer_label.config(text="Time: {:.2f} seconds".format(elapsed_time))
    window.after(100, update_timer)

def check_puzzle_solved():
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
                    return  # Exit the function if any invalid input is found

    # Check if the puzzle is solved
    if is_solved(puzzle):
        # Check if the solved puzzle is valid
        if is_valid_puzzle(puzzle):

            # Format the solving time
            solving_time_formatted = "{:.2f} seconds".format(elapsed_time)

            # Display a message with the solving time
            messagebox.showinfo("Puzzle Solved", "Puzzle solved in {}".format(solving_time_formatted))
        else:
            # Display a message indicating the puzzle is solved incorrectly
            messagebox.showinfo("Puzzle Solved Incorrectly", "The puzzle is solved, but it is incorrect.")



# Create the main window
window = tk.Tk()
window.title("Sudoku Master")
window.configure(bg='white')

# Use a specific theme
style = ttk.Style()
style.theme_use('clam')

# Create the timer label
timer_label = ttk.Label(window, text="Time: 0.00 seconds")
timer_label.grid(row=11, column=0, columnspan=9, padx=10, pady=10)
update_timer()

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

        # Bind the select_cell function to the left mouse button click event
        input_cell.bind('<Button-1>', lambda event, r=row, c=col: select_cell(r, c))

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
puzzle_dropdown = tk.StringVar(window)
puzzle_options = {
    "Easy": "Easy",
    "Medium": "Medium",
    "Hard": "Hard"
}

puzzle_dropdown.set("SELECT PUZZLE")  # Set the initial option
puzzle_dropdown.trace("w", lambda *args: load_puzzle())  # Call load_puzzle() when the option changes

puzzle_menu = tk.OptionMenu(window, puzzle_dropdown, *puzzle_options.keys())
puzzle_menu.config(font=("Helvetica", 14))
puzzle_menu.grid(row=10, column=0, columnspan=9, padx=10, pady=10, sticky="ew")

# Bind the arrow key events to the move_cell function
window.bind('<Up>', move_cell)
window.bind('<Down>', move_cell)
window.bind('<Left>', move_cell)
window.bind('<Right>', move_cell)

# Bind the <KeyRelease> event to check if the puzzle is solved after each cell input
window.bind('<KeyRelease>', lambda event: check_puzzle_solved())

# Set the initial selected cell
select_cell(current_row, current_col)

# Run the GUI main loop
window.mainloop()
