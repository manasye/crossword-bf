import time

def accessMap(fileName):

    data = open(fileName,"r")
    rawParsed = data.readlines()
    parsed = []
    matrix = []
    counter = 0

    for raw in rawParsed:
        parsed.append([])
        parsed[counter].append(raw.strip('\n'))
        counter = counter + 1

    size = int(parsed[0][0])
    i = 0

    for x in range(1,size+1):
        matrix.append([])
        split = list(parsed[x][0])

        for item in split:
            matrix[i].append(item)

        i = i + 1

    return matrix

def accessWord(fileName):

    data = open(fileName,"r")
    rawParsed = data.readlines()
    parsed = []
    counter = 0

    for raw in rawParsed:
        parsed.append([])
        parsed[counter].append(raw.strip('\n'))
        counter = counter + 1

    size = int(parsed[0][0])
    words = parsed[size+1][0].split(';')

    print('\nList of words: ')
    print(words)

    max_len = len(max(words, key=len))
    wlist = {}

    for i in range(1, max_len + 1):
        wlist[i] = []

    # Separate words based on it's length
    for word in words:
        entry = {"word": word, "avail": True}
        wlist[len(word)].append(entry)

    return wlist

def printMatrix(matrix):

    for x in range(0,len(matrix)):
        for y in range(0, len(matrix)):
            print(matrix[x][y],end = '')
            print(' ',end = '')
        print('')

def accessSpaces(matrix):
    spaces = []
    counter = 0

    # access vertical spaces
    for i in range(0,len(matrix)):
        j = 0
        while(j < len(matrix) - 1):
            if (matrix[j][i] == '-') and (matrix[j+1][i] == '-'):
                spaces.append([])
                start = [j, i]
                #print(start)
                a = j
                length = 0

                while (matrix[a][i] == '-') and (a < len(matrix) - 1):
                    length = length + 1
                    a = a + 1

                if(a == len(matrix)-1) and matrix[a][i] == '-':
                    finish = [a , i]
                    j = j + length
                    length = length + 1
                else:
                    finish = [a-1 ,i]
                    j = j + length

                # Append to list of spaces
                spaces[counter].append(start)
                spaces[counter].append(finish)
                spaces[counter].append(length)
                spaces[counter].append('v')
                counter = counter + 1
            else:
                j = j + 1

    # access horizontal spaces
    for j in range(0, len(matrix)):
        i = 0
        while (i < len(matrix) - 1):
            if (matrix[j][i] == '-') and (matrix[j][i + 1] == '-'):
                spaces.append([])
                start = [j, i]

                a = i
                length = 0

                while (matrix[j][a] == '-') and (a < len(matrix) - 1):
                    length = length + 1
                    a = a + 1

                if (a == len(matrix) - 1) and matrix[a][i] == '-':
                    finish = [j,a]
                    i = i + length
                    length = length + 1

                else:
                    finish = [j,a - 1]
                    i = i + length

                # Append to list of spaces
                spaces[counter].append(start)
                spaces[counter].append(finish)
                spaces[counter].append(length)
                spaces[counter].append('h')
                counter = counter + 1
            else:
                i = i + 1

    return spaces

# Function that do bruteforce to search for solution
def solveMatrix(matrix,spaces,words,filled=0):

    global result, done

    # Basis (stop when all spaces been filled)
    if filled == len(spaces):
        result = matrix
        done = True
        return True

    spStartRow = spaces[filled][0][0]
    spStartCol = spaces[filled][0][1]
    spLen = spaces[filled][2]
    spType = spaces[filled][3]

    for word in words[spLen]:

        if not word['avail']:
            continue

        matched = True

        if spType == 'v':
            for i in range(0,spLen):
                curr = matrix[spStartRow+i][spStartCol]
                if (curr != '-') and (curr != word['word'][i]):
                    matched = False
                #print(matched)

        elif spType == 'h':
            for i in range(0,spLen):
                curr = matrix[spStartRow][spStartCol+i]
                if (curr != '-') and (curr != word['word'][i]):
                    matched = False

        if matched:
            backtr = ''

            for i in range(0,spLen):
                if(spType == 'v'):
                    backtr += matrix[spStartRow + i][spStartCol]
                    matrix[spStartRow + i][spStartCol] = word['word'][i]

                elif spType == 'h':
                    backtr += matrix[spStartRow][spStartCol + i]
                    matrix[spStartRow][spStartCol + i] = word['word'][i]

            word['avail'] = False

            print('\n')
            printMatrix(matrix)
            print(filled)

            solveMatrix(matrix,spaces,words,filled=filled+1)

            if done:
                return True
            else:
                word['avail'] = True
                for i in range(0,spLen):
                    if (spType == 'v'):
                        matrix[spStartRow + i][spStartCol] = backtr[i]
                    elif spType == 'h':
                        matrix[spStartRow][spStartCol + i] = backtr[i]

if __name__ == '__main__':
    file = input('Please input the file name (with extension): ')
    myMatrix = accessMap(file)
    myWords = accessWord(file)
    #print(myWords)
    mySpaces = accessSpaces(myMatrix)
    #print(mySpaces)

    print('\nInitial state is :')
    printMatrix(myMatrix)

    # Initialization
    result = None
    done = False

    begin = time.clock()
    solveMatrix(myMatrix,mySpaces,myWords,filled=0)
    end = time.clock()

    print('\nResult is :\n')

    if(result == None):
        print('Unsolvable..')
    else:
        printMatrix(result)
        print('\nTime taken is ' + str(end-begin) + ' s')