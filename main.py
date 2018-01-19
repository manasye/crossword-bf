import timeit

global result,done

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

    # Separate words based on length
    for word in words:
        entry = {"word": word, "avail": 1}
        wlist[len(word)].append(entry)

    return wlist

def printMatrix(matrix):

    for x in range(0,len(matrix)):
        for y in range(0, len(matrix)):
            print(matrix[x][y],end = '')
        print('')

def accessSpaces(matrix):
    spaces = []
    counter = 0

    # access vertically
    for j in range(0,len(matrix)):
        i = 0
        while (i < len(matrix)-1):
            if(matrix[j][i] == '-') and (matrix[j][i+1] == '-'):
                spaces.append([])
                start = [j,i]

                a = i
                length = 1

                while (matrix[j][a+1] == '-') and (a+1 < len(matrix) - 1) :
                    length = length + 1
                    a = a + 1

                finish = [j,a+1]
                i = i + length

                # Append to list of spaces
                spaces[counter].append(start)
                spaces[counter].append(finish)
                spaces[counter].append(length+1)
                spaces[counter].append('h')
                counter = counter + 1
            else :
                i = i + 1

    # access horizontally
    for i in range(0,len(matrix)):
        j = 0
        while(j < len(matrix)-1):
            if (matrix[j][i] == '-') and (matrix[j+1][i] == '-'):
                spaces.append([])
                start = [j, i]

                a = j
                length = 1

                while (matrix[a+1][i] == '-') and (a + 1 < len(matrix) - 1):
                    length = length + 1
                    a = a + 1

                finish = [a + 1 ,i]
                j = j + length

                # Append to list of spaces
                spaces[counter].append(start)
                spaces[counter].append(finish)
                spaces[counter].append(length+1)
                spaces[counter].append('v')
                counter = counter + 1
            else:
                j = j + 1
    return spaces

# Function that do bruteforce to search for solution
def solveMatrix(matrix,spaces,words,inserted=0):

    # Basis (stop when all spaces been filled)
    if inserted == len(spaces):
        result = matrix
        done = True
        return True

    spStartRow = spaces[inserted][0][0]
    spStartCol = spaces[inserted][0][1]
    spLen = spaces[inserted][2]
    spType = spaces[inserted][3]

    for word in words[spLen]:
        if not word['avail']:
            continue
        else :
            matched = True

        if spType == 'hor':
            for i in range(0,spLen):
                curr = matrix[spStartRow][spStartCol+i]
                if curr != '-' and curr != word['word'][i]:
                    matched = False

        else :
            for i in range(0,spLen):
                curr = matrix[spStartRow+i][spStartCol]
                if curr != '-' and curr != word['word'][i]:
                    matched = False

        if matched:
            backtr = ''
            for i in range(0,spLen):
                if(spType == 'hor'):
                    backtr += matrix[spStartRow][spStartCol + i]
                    matrix[spStartRow][spStartCol+i] = word['word'][i]
                else:
                    backtr += matrix[spStartRow+i][spStartCol]
                    matrix[spStartRow+i][spStartCol] = word['word'][i]

        word['avail'] = 0

        solveMatrix(matrix,spaces,inserted=inserted+1)

        if done:
            return True
        else:
            word['avail'] = 1
            for i in range(0,spLen):
                if (spType == 'hor'):
                    matrix[spStartRow][spStartCol + i] = backtr[i]
                else:
                    matrix[spStartRow + i][spStartCol] = backtr[i]


if __name__ == '__main__':
    file = input('Please input the file name (with extension): ')
    myMatrix = accessMap(file)
    myWords = accessWord(file)
    mySpaces = accessSpaces(myMatrix)

    print('\nInitial state is :')
    printMatrix(myMatrix)

    #solveMatrix(myMatrix,mySpaces,myWords,inserted=0)
    #printMatrix(result)
    #print(len(myWords))
    #print(myWords)