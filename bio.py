import sys
import numpy as np


NEG_INF = float("-inf")
alphabet = {}
MATRIX_BAD_DIMENSION_ERROR = "ERROR: Wymiary macierzy prawdopodobieństw nie pokrywają się z długością alfabetu"
GAP_TOP = 0
GAP_BOTTOM = 1
BOTH = 2
STOP = 3

def similarity(char_1, char_2, probability_matrix):
    return probability_matrix[alphabet[char_1]][alphabet[char_2]]

def NW(word1, word2, probability_matrix):
    word1_length = len(word1)
    word2_length = len(word2)
    S = np.ones((word1_length+1, word2_length+1), dtype=float) * NEG_INF
    operations = np.zeros((word1_length+1, word2_length+1), dtype=int)
    operations[0][0] = STOP

    S[0][0] = 0
    for i in range(1, word1_length+1):
        S[i][0] = S[i-1][0] + similarity(word1[i-1], '-', probability_matrix)
        operations[i][0] = GAP_BOTTOM
    for j in range(1, word2_length+1):
        S[0][j] = S[0][j-1] + similarity('-', word2[j-1], probability_matrix)
        operations[0][j] = GAP_TOP


    for i in range(1, word1_length+1):
        for j in range(1, word2_length+1):
            score_sub = S[i-1][j-1] + similarity(word1[i-1], word2[j-1], probability_matrix)
            score_del = S[i-1][j] + similarity(word1[i-1], '-', probability_matrix)
            score_ins = S[i][j-1] + similarity('-', word2[j-1], probability_matrix)
            S[i][j] = max(score_sub, score_del, score_ins)
            if S[i][j]  == score_sub:
                operations[i][j] = BOTH
            elif S[i][j]  == score_del:
                operations[i][j] = GAP_BOTTOM
            else:
                operations[i][j] = GAP_TOP

    return S, operations


def Smith(word1, word2, probability_matrix):
    word1_length = len(word1)
    word2_length = len(word2)
    S = np.ones((word1_length+1, word2_length+1), dtype=float) * NEG_INF
    operations = np.zeros((word1_length+1, word2_length+1), dtype=int)
    operations[0][0] = STOP

    S[0][0] = 0
    for i in range(1, word1_length+1):
        S[i][0] = 0
        operations[i][0] = STOP
    for j in range(1, word2_length+1):
        S[0][j] = 0
        operations[0][j] = STOP


    for i in range(1, word1_length+1):
        for j in range(1, word2_length+1):
            score_sub = S[i-1][j-1] + similarity(word1[i-1], word2[j-1], probability_matrix)
            score_del = S[i-1][j] + similarity(word1[i-1], '-', probability_matrix)
            score_ins = S[i][j-1] + similarity('-', word2[j-1], probability_matrix)
            S[i][j] = max(0, score_sub, score_del, score_ins)
            if S[i][j]  == score_sub:
                operations[i][j] = BOTH
            elif S[i][j]  == score_del:
                operations[i][j] = GAP_BOTTOM
            elif S[i][j] == score_ins:
                operations[i][j] = GAP_TOP
            else:
                operations[i][j] = STOP

    return S, operations 

def get_words_alligned(word1, word2, operations,ind_i = None, ind_j = None):
    if ind_i is not None:
        i = ind_i - 1 
        if i < 0: i = 0
    else:
        i = len(word1) - 1
    if ind_j is not None:
        j = ind_j - 1 
        if j < 0: j = 0
    else:
        j = len(word2) - 1
       
    word1_alligned = ""
    word2_alligned = ""
    while i >= 0 or j >= 0:
        operation = operations[i+1][j+1]
        if operation == GAP_BOTTOM:
            word1_alligned += word1[i]
            word2_alligned += "-"
            i -= 1
        elif operation == GAP_TOP:
            word1_alligned += "-"
            word2_alligned += word2[j]
            j -= 1
        elif operation == STOP:
            return word1_alligned[::-1], word2_alligned[::-1]
        else:
            word1_alligned += word1[i]
            word2_alligned += word2[j]
            i -= 1
            j -= 1
    
    return word1_alligned[::-1], word2_alligned[::-1]
    
def main():
    word1 = None
    word2 = None
    probability_matrix = []
    if len(sys.argv) < 3:
        print(
            "Wywołaj program ze wskazaniem plików zawierających (kolejno)"
            " słowa do analizy oraz z macierzą odległości symboli"
            )
        return
    words_file = sys.argv[1]
    matrix_file = sys.argv[2]
    mode = "normal"
    if len(sys.argv) > 3:
        mode = sys.argv[3]
    
    with open(words_file) as f:
        words = f.read().splitlines()
        word1 = words[0]
        word2 = words[1]
    
    with open(sys.argv[2]) as f:
        rows_read = 0
        symbols = f.readline()[:-1].split(',')
        for i, symbol in enumerate(symbols):
            alphabet[symbol] = i
        for line in f:
            if line == "":
                continue
            if line[-1] != "\n":
                line += "\n"
            rows_read += 1
            vals = [float(x) for x in line[:-1].split(',')]
            if len(vals) != len(alphabet):
                print(MATRIX_BAD_DIMENSION_ERROR)
                return
            
            probability_matrix.append(vals)
        if rows_read != len(alphabet):
            print(MATRIX_BAD_DIMENSION_ERROR)
            return
    

        S, operations = NW (word2, word1, probability_matrix)
        print("==========NW================")
        print("  ",end='')
        for char in word1:
            print("  ",char,end='')
        print()
        print(S)
        words = get_words_alligned(word2, word1, operations)
        operations = np.where(operations == 2, '\u21F1', operations)
        operations = np.where(operations == '1', '\u21E7', operations)
        operations = np.where(operations == '0', '\u21E6', operations)
        operations = np.where(operations == '3', 'S', operations)
        print(operations)
        print(f"Wynik podobieństwa = {S[len(word2)][len(word1)]}")
        print(words[1])
        print(words[0])

        S, operations = Smith(word2, word1, probability_matrix)
        print("==========Smith================")
        print("   ",end='')
        for char in word1:
            print("  ",char,end='')
        print()
        print(S)
        ind = np.unravel_index(np.argmax(S, axis=None), S.shape)
        words = get_words_alligned(word2, word1, operations,ind[0],ind[1])
        
        operations = np.where(operations == 2, '\u21F1', operations)
        operations = np.where(operations == '1', '\u21E7', operations)
        operations = np.where(operations == '0', '\u21E6', operations)
        operations = np.where(operations == '3', 'S', operations)

        print(operations)
        print(f"Wynik podobieństwa lokalnego= {S[ind[0]][ind[1]]}")
        print(words[1])
        print(words[0])

if __name__ == "__main__":
    main()