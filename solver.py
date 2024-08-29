import os
import pyautogui as pag

def get_board() -> list:
    """
    Asks the user to input each line of the Sudoku board

    :return: A 2D list of the Sudoku board
    """
    board = []
    for row in range(9):
        line = list(input(f"Enter line {row + 1} with space for blanks: "))
        if len(line) != 9:
            print("Invalid line")
            exit(1)
        else:
            board.append(line)
    return board

def print_board(board: list) -> None:
    """
    Displays the given board to the screen

    :param board: The board to be displayed
    """
    for row_num, row in enumerate(board):
        for num_num, num in enumerate(row):
            if num_num == 2 or num_num == 5:
                print(f"{num}|",end="")
            else:
                print(num, end="")
        print("")
        if row_num == 2 or row_num == 5:
            print("-----------")

def has_in_row(board: list, row_num: int) -> list:
    """
    Finds the numbers in the given row

    :param board: The board to search
    :param row_num: The row to search
    :return: A list of the numbers in the given row
    """
    has = board[row_num].copy()
    while " " in has:
        has.remove(" ")
    return has

def has_in_col(board: list, col_num: int) -> list:
    """
    Finds the numbers in the given column

    :param board: The board to search
    :param col_num: The column to search
    :return: A list of the numbers in the given column
    """
    has = []
    for row_num in range(len(board)):
        has.append(board[row_num][col_num])
    while " " in has:
        has.remove(" ")
    return has

def has_in_square(board: list, row_num: int, col_num: int) -> list:
    """
    Finds the numbers in the square of the row and col specified

    :param board: The board to search
    :param row_num: The row to search the square in
    :param col_num: The column to search the square in
    :return: A list of the numbers in the specified square
    """
    row_sq_num = int(row_num/3)
    col_sq_num = int(col_num/3)
    has = []
    for row in range(3):
        for col in range(3):
            has.append(board[row_sq_num * 3 + row][col_sq_num * 3 + col])
    while " " in has:
        has.remove(" ")
    return has

def get_candidates(unsolved: list) -> list:
    """
    Gets the candidate numbers for the board

    :param unsolved: The unsolved board
    :return: A board with candidate numberes filled in
    """
    candidates = [[ [] for _ in range(9)] for _ in range(9)]
    for row_num, row in enumerate(unsolved):
        for col_num, num in enumerate(row):
            if num == " ":        
                has = set()
                has.update(has_in_row(unsolved, row_num))
                has.update(has_in_col(unsolved, col_num))
                has.update(has_in_square(unsolved, row_num, col_num))
                needs = {"1", "2", "3", "4", "5", "6", "7", "8", "9"}
                candidates[row_num][col_num] = needs - has
    return candidates

def solve_iter(board, candidates) -> list:
    """
    Does a single iteration of solving

    :param board: The board to solve
    :param candidates: The current candidate list
    :return: The new board after solving with one iteration
    """
    #fill single candidates
    new_board = []
    for row in board:
        new_board.append(row.copy())
    did_cand_solve = False
    for row_num, row in enumerate(new_board):
        for col_num, num in enumerate(row):
            if num == " ":
                if len(list(candidates[row_num][col_num])) == 1:
                     new_board[row_num][col_num] = list(candidates[row_num][col_num])[0]
                     did_cand_solve = True
    if did_cand_solve:
        candidates = get_candidates(new_board)
    #TODO:do elimination solve

    return new_board

def is_solved(board: list) -> bool:
    """
    Checks if the board is solved

    :param board: The board to check
    :return: True if solved, False otherwise
    """
    #check filled
    for row in board:
        for num in row:
            if num == " ":
                return False
    #check rows
    for row in board:
        if sorted(row) != ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            return False
    #check cols
    for col_num in range(9):
        if sorted(has_in_col(board, col_num)) != ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            return False
    #check squares
    for i in range(3):
        for j in range(3):
            if sorted(has_in_square(board, i*3, j*3)) != ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                return False
    return True

def main():
    print("\n\nSudoku Solver")
    print("----------------------------")
    board = get_board()
    print("")
    print_board(board)
    print_board_state = True if input("\nWould you like board state updates? (y/n): ").lower() == "y" else False
    print("Starting solve...")
    while not is_solved(board):
        candidates = get_candidates(board)
        new_board = solve_iter(board, candidates)
        if board == new_board:
            print("\nERROR: Unable to solve")
            print("Current board state:")
            print_board(new_board)
            exit(1)
        else:
            board = new_board
            if print_board_state:
                print("\nCurrent board state:")
                print_board(board)  
    print("\nBoard solved!")
    print_board(board)
    fill_into_nytimes = True if input("\nWould you like to autofill into NY Times Sudoku? (y/n): ").lower() == "y" else False
    if fill_into_nytimes:
        print("Please click on the upper left cell and ensure you are not on candidate entry mode")
        print("Entry will begin in 5 seconds")
        pag.sleep(5)
        for row in board:
            for num in row:
                pag.press(row)
                pag.press("right")
            pag.press("down")
            for _ in range(8):
                pag.press("left")

if __name__ == "__main__":
    auto_fill = True if input("Would you like to autofill with fill.py? (y/n): ").lower() == "y" else False
    if auto_fill:
        os.system('start /D .\\ "filler" /min python fill.py')
        print("Autofill started, ensure you are clicked on the input field when it begins")
    main()
