import timeit

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

    return words

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
                #print(start)

                a = i
                length = 1

                while (matrix[j][a+1] == '-') and (a+1 < len(matrix) - 1) :
                    length = length + 1
                    a = a + 1

                finish = [j,a+1]
                i = i + length

                spaces[counter].append(start)
                spaces[counter].append(finish)
                spaces[counter].append(length)
                spaces[counter].append('v')
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
                #print(start)

                a = j
                length = 1

                while (matrix[a+1][i] == '-') and (a + 1 < len(matrix) - 1):
                    length = length + 1
                    a = a + 1

                finish = [a + 1 ,i]
                j = j + length

                spaces[counter].append(start)
                spaces[counter].append(finish)
                spaces[counter].append(length)
                spaces[counter].append('h')
                counter = counter + 1
            else:
                j = j + 1
    return spaces

#def solveMatrix(matrix,words):

if __name__ == '__main__':
    file = input('Please input the file name (with extension): ')
    myMatrix = accessMap(file)
    myWords = accessWord(file)
    mySpaces = accessSpaces(myMatrix)
    print('Initial state is :\n')
    printMatrix(myMatrix)
    print('\nList of words :')
    print(myWords)

    print(mySpaces)
    #print(len(myWords))
    #print(myWords)