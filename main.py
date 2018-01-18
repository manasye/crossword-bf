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

#def solveMatrix(matrix):


if __name__ == '__main__':
    myMatrix = accessMap('tc-5.txt')
    myWords = accessWord('tc-5.txt')
    printMatrix(myMatrix)
    print(len(myWords))
    print(myWords)