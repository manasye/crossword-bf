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
        wlist[len(word)].append({"word": word})

    return wlist

def printMatrix(matrix):

    for x in range(0,len(matrix)):
        for y in range(0, len(matrix)):
            print(matrix[x][y],end = '')
            print(' ',end = '')
        print('')

# Function to check whether certain coordinate is in edge (for spaces checking purposes)
def horOrVer(matrix,i,j):

    if i-1 >=0:
        up = (matrix[i-1][j] == '-')
    else:
        up = False

    try:
        down = (matrix[i+1][j] == '-')
    except:
        down = False

    if j-1 >= 0:
        left = (matrix[i][j-1] == '-')
    else:
        left = False

    try:
        right = (matrix[i][j+1] == '-')
    except:
        right = False

    return (not(up and down)),(not(left and right))

def accessSpaces(matrix):
    spaces = []
    counter = 0

    for i in range (0,len(matrix)):
        for j in range (0,len(matrix)):

            if(matrix[i][j]) == '-':
                ver,hor = horOrVer(matrix,i,j)
                #print(ver,hor)
                if hor:
                    length = 0
                    check = True
                    while check:
                        try:
                            if matrix[i][j+length] == '-':
                                length = length + 1
                            else :
                                check = False
                        except:
                            check = False
                    if(length >= 2):
                        spaces.append([])
                        spaces[counter].append([i, j])
                        spaces[counter].append(length)
                        spaces[counter].append('h')
                        counter += 1

                if ver:
                    length = 0
                    check = True
                    while check:
                        try:
                            if matrix[i + length][j] == '-':
                                length = length + 1
                            else:
                                check = False
                        except:
                            check = False
                    if (length >= 2):
                        spaces.append([])
                        spaces[counter].append([i, j])
                        spaces[counter].append(length)
                        spaces[counter].append('v')
                        counter += 1

    return spaces

# Function that do bruteforce to search for solution
def solveMatrix(matrix,spaces,words,filled=0):

    global result,done

    # Basis (stop when all spaces been filled)
    if filled == len(spaces):
        result = matrix
        done = True
        return True

    spStartRow = spaces[filled][0][0]
    spStartCol = spaces[filled][0][1]
    spLen = spaces[filled][1]
    spType = spaces[filled][2]

    for word in words[spLen]:


        matched = True

        if spType == 'v':
            i = 0
            while(i<spLen) and matched :
                curr = matrix[spStartRow+i][spStartCol]
                if (curr != '-') and (curr != word['word'][i]):
                    matched = False
                else :
                    i += 1

        else :
            i = 0
            while (i < spLen) and matched:
                curr = matrix[spStartRow][spStartCol+i]
                if (curr != '-') and (curr != word['word'][i]):
                    matched = False
                else :
                    i += 1

        if matched:

            backtr = ""
            for i in range(0,spLen):
                if(spType == 'v'):
                    backtr += matrix[spStartRow + i][spStartCol]
                    matrix[spStartRow + i][spStartCol] = word['word'][i]

                else :
                    backtr += matrix[spStartRow][spStartCol + i]
                    matrix[spStartRow][spStartCol + i] = word['word'][i]

            #print('\n')
            #printMatrix(matrix)
            #print(filled)

            solveMatrix(matrix,spaces,words,filled=filled+1)

            if done:
                return True

            else:

                for i in range(0,spLen):
                    if (spType == 'v'):
                        matrix[spStartRow + i][spStartCol] = backtr[i]
                    else :
                        matrix[spStartRow][spStartCol + i] = backtr[i]


if __name__ == '__main__':
    file = input('Please input the file name (with extension): ')
    myMatrix = accessMap(file)
    myWords = accessWord(file)
    #print(myWords)
    mySpaces = accessSpaces(myMatrix)
   # print(mySpaces)

    print('\nInitial state is :')
    printMatrix(myMatrix)

    # Initialization
    result = []
    done = False

    begin = time.clock()
    solveMatrix(myMatrix,mySpaces,myWords,filled=0)
    end = time.clock()

    print('\nResult is :\n')

    if(result == []):
        print('Unsolvable..')
    else:
        printMatrix(result)
        print('\nTime taken is ' + str(end-begin) + ' s')
