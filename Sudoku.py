
import pycosat
import sys, getopt 
import time

def main(): 
    while True:
        choice = input("輸入 'manual' 手動輸入數獨拼圖或 'preset' 選擇預設拼圖: ").strip().lower()
        if choice == 'manual':
            puzzle = get_manual_input()
            solve_problem(puzzle)
        elif choice == 'preset':
            preset_choice = input("選擇預設拼圖難度 (easy, medium, hard, evil, blank): ").strip().lower()
            if preset_choice == 'easy':
                solve_problem(easy)
            elif preset_choice == 'medium':
                solve_problem(medium)
            elif preset_choice == 'hard':
                solve_problem(hard)
            elif preset_choice == 'evil':
                solve_problem(evil)
            elif preset_choice == 'blank':
                solve_problem(blank)
            else:
                print("無效的選擇，請重試。")
        else:
            print("無效的選擇，請重試。")

def get_manual_input():
    print("逐行輸入數獨拼圖，每個空格用0表示。")
    puzzle = []
    for i in range(9):
        while True:
            row = input(f"輸入第 {i + 1} 行 (9個數字，空格用0表示): ").strip()
            if len(row) == 9 and row.isdigit():
                puzzle.append([int(x) for x in row])
                break
            else:
                print("輸入無效。請輸入正好9個數字。")
    return puzzle
            
def help():
    print('Usage:')
    print('Sudoku.py -e [or] --easy')
    print('Sudoku.py -m [or] --medium')
    print('Sudoku.py -h [or] --hard')
    print('Sudoku.py -v [or] --evil')
    print('Sudoku.py -b [or] --blank')
    print('All problems generated by websudoku.com')
    sys.exit()

def solve_problem(problemset):
    print('Problem:') 
    pprint(problemset)  
    solve(problemset) 
    print('Answer:')
    pprint(problemset)  
    
def v(i, j, d): 
    return 81 * (i - 1) + 9 * (j - 1) + d

#Reduces Sudoku problem to a SAT clauses 
def sudoku_clauses(): 
    res = []
    # for all cells, ensure that the each cell:
    for i in range(1, 10):
        for j in range(1, 10):
            # denotes (at least) one of the 9 digits (1 clause)
            res.append([v(i, j, d) for d in range(1, 10)])
            # does not denote two different digits at once (36 clauses)
            for d in range(1, 10):
                for dp in range(d + 1, 10):
                    res.append([-v(i, j, d), -v(i, j, dp)])

    def valid(cells): 
        for i, xi in enumerate(cells):
            for j, xj in enumerate(cells):
                if i < j:
                    for d in range(1, 10):
                        res.append([-v(xi[0], xi[1], d), -v(xj[0], xj[1], d)])

    # ensure rows and columns have distinct values
    for i in range(1, 10):
        valid([(i, j) for j in range(1, 10)])
        valid([(j, i) for j in range(1, 10)])
        
    # ensure 3x3 sub-grids "regions" have distinct values
    for i in 1, 4, 7:
        for j in 1, 4 ,7:
            valid([(i + k % 3, j + k // 3) for k in range(9)])
      
    assert len(res) == 81 * (1 + 36) + 27 * 324
    return res

def solve(grid):
    #solve a Sudoku problem
    clauses = sudoku_clauses()
    for i in range(1, 10):
        for j in range(1, 10):
            d = grid[i - 1][j - 1]
            # For each digit already known, a clause (with one literal). 
            if d:
                clauses.append([v(i, j, d)])
    
    # Print number SAT clause  
    numclause = len(clauses)
    print ("P CNF " + str(numclause) +"(number of clauses)")
    
    # solve the SAT problem
    start = time.time()
    sol = set(pycosat.solve(clauses))
    end = time.time()
    print("Time: "+str(end - start))
    
    def read_cell(i, j):
        # return the digit of cell i, j according to the solution
        for d in range(1, 10):
            if v(i, j, d) in sol:
                return d

    for i in range(1, 10):
        for j in range(1, 10):
            grid[i - 1][j - 1] = read_cell(i, j)


if __name__ == '__main__':
    from pprint import pprint

    # Sudoku problem generated by websudoku.com
    easy = [[0, 0, 0, 1, 0, 9, 4, 2, 7],
            [1, 0, 9, 8, 0, 0, 0, 0, 6],
            [0, 0, 7, 0, 5, 0, 1, 0, 8],
            [0, 5, 6, 0, 0, 0, 0, 8, 2],
            [0, 0, 0, 0, 2, 0, 0, 0, 0],
            [9, 4, 0, 0, 0, 0, 6, 1, 0],
            [7, 0, 4, 0, 6, 0, 9, 0, 0],
            [6, 0, 0, 0, 0, 8, 2, 0, 5],
            [2, 9, 5, 3, 0, 1, 0, 0, 0]]
        
    medium = [[5, 8, 0, 0, 0, 1, 0, 0, 0],
            [0, 3, 0, 0, 6, 0, 0, 7, 0],
            [9, 0, 0, 3, 2, 0, 1, 0, 6],
            [0, 0, 0, 0, 0, 0, 0, 5, 0],
            [3, 0, 9, 0, 0, 0, 2, 0, 1],
            [0, 5, 0, 0, 0, 0, 0, 0, 0],
            [6, 0, 2, 0, 5, 7, 0, 0, 8],
            [0, 4, 0, 0, 8, 0, 0, 1, 0],
            [0, 0, 0, 1, 0, 0, 0, 6, 5]]

    evil = [[0, 2, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 6, 0, 0, 0, 0, 3],
            [0, 7, 4, 0, 8, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 3, 0, 0, 2],
            [0, 8, 0, 0, 4, 0, 0, 1, 0],
            [6, 0, 0, 5, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 7, 8, 0],
            [5, 0, 0, 0, 0, 9, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 4, 0]]

    hard = [[0, 2, 0, 0, 0, 0, 0, 3, 0],
            [0, 0, 0, 6, 0, 1, 0, 0, 0],
            [0, 6, 8, 2, 0, 0, 0, 0, 5],
            [0, 0, 9, 0, 0, 8, 3, 0, 0],
            [0, 4, 6, 0, 0, 0, 7, 5, 0],
            [0, 0, 1, 3, 0, 0, 4, 0, 0],
            [9, 0, 0, 0, 0, 7, 5, 1, 0],
            [0, 0, 0, 1, 0, 4, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 9, 0]]
    
    blank = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    
if __name__ == "__main__":
    main()
