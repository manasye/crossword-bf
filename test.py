""" **********************************
                IMPORT
*********************************** """

import time

""" **********************************
                CONFIG
*********************************** """

char_not_accessible = '#'
char_accessible = '-'
word_separator = ';'
empty_cell = ' '

""" **********************************
            DEBUG ZONE
********************************** """


def print_board(board):
    """
    <DEBUG> print board
    :param board: crossword representation
    """

    if board is not None:
        for line in board:
            line = [word.replace(char_not_accessible, empty_cell) for word in line]
            print(line)
    else:
        print("This board is unsolvable")


def print_word_list(word_list):
    """
    <DEBUG> print word list
    :param word_list: words separated by len
    :type word_list: dict
    """

    for key, value in word_list.items():

        if len(value) != 0:
            print("\nlen = {} words".format(key))

            for word in value:
                print("{} ({})".format(word['word'], word['available']))


def print_stats(word, word_inserted, slot_list):
    """
    <DEBUG> show current stat of crossword
    :param word: current examined word
    :type word: dict
    :param word_inserted: how many word inserted into crossword
    :type word_inserted: int
    :param slot_list: list of slots to fill
    :type slot_list: list
    """

    text = "checking {}\n" \
           "word inserted {}\n" \
           "current slot : {}\n".format(word['word'], word_inserted, slot_list[word_inserted])
    print(text)


def print_progress(word_inserted, total):
    """
    <DEBUG> print current solving progress
    :param word_inserted: word inserted into the crossword
    :type word_inserted: int
    :param total: amount of word to be inserted
    :type total: int
    """

    print("{} / {}".format(word_inserted, total))


""" **********************************
            FUNCTION
********************************** """


def parse_file():
    """
    Function to parse map and text from file
    :return: list of word
    :rtype: list
    """

    filename = input("Please input filename (without extension) : ")
    filename = filename + ".txt"
    file = open(filename, 'r')

    board = []
    split_chained_words = []

    for line in file:

        # If it's crossword board
        if any(letter in line for letter in [char_accessible, char_not_accessible]):
            board.append(list(line.strip()))

        # If it's list of word (HAS TO BE IN ONE LINE)
        elif word_separator in line:
            chained_words = line.strip()
            split_chained_words = chained_words.split(word_separator)
            split_chained_words = list(filter(None, split_chained_words))

    return board, split_chained_words


def group_words_by_len(raw_word_list):
    """
    Function to group list of word by it's length
    :param raw_word_list: list of word (parsed from file)
    :type raw_word_list: list
    :return: dictionary of words
    :rtype: dictionary
    """

    max_len = len(max(raw_word_list, key=len))
    words = {}

    # Initialize
    for i in range(1, max_len + 1):
        words[i] = []

    # Separate words
    for word in raw_word_list:
        entry = {"word": word, "available": 1}
        words[len(word)].append(entry)

    return words


def get_board_data(board):
    """
    Function to gather slots data from raw board
    :param board: matrix represent crossword
    :type board: list of list
    :return: slot's data (slot type, start row, start col, slot length)
    :rtype: list of tuples
    """

    def is_edge(row, col):
        """
        Function to check whether a row,col is an edge
        :param row: cell row
        :type row: int
        :param col: cell col
        :type col: int
        :returns: is horizontal edge
        :rtype: bool, bool
        """

        if row - 1 >= 0:
            grow_up = bool(board[row - 1][col] != char_not_accessible)
        else:
            grow_up = False

        try:
            grow_down = bool(board[row + 1][col] != char_not_accessible)
        except:
            grow_down = False

        if col - 1 >= 0:
            grow_left = bool(board[row][col - 1] != char_not_accessible)
        else:
            grow_left = False

        try:
            grow_right = bool(board[row][col + 1] != char_not_accessible)
        except:
            grow_right = False

        hor_edge = grow_left ^ grow_right
        ver_edge = grow_up ^ grow_down

        return hor_edge, ver_edge

    # Iterate board to gather information
    slot_list = []
    for row in range(0, len(board)):
        for col in range(0, len(board[row])):

            # If it's accessible
            if board[row][col] != char_not_accessible:

                # Get cell information
                horizontal_edge, vertical_edge = is_edge(row, col)

                # Count length of horizontal empty slot
                if horizontal_edge:
                    length = 0
                    while True:
                        try:
                            if board[row][col + length] != char_not_accessible:
                                length += 1
                            else:
                                break
                        except:
                            break

                    if length > 1:
                        slot_list.append(("hor", row, col, length))

                # Count length of vertical empty slot
                if vertical_edge:
                    length = 0
                    while True:
                        try:
                            if board[row + length][col] != char_not_accessible:
                                length += 1
                            else:
                                break
                        except:
                            break

                    if length > 1:
                        slot_list.append(("ver", row, col, length))

    return slot_list


def solve_crossword(board, slot_list, word_inserted=0):
    """
    Main function of brute force crossword solving
    :param board: crossword representation
    :type board: list of list
    :param slot_list: list of slot to be filled
    :type slot_list: list
    :param word_inserted: word inserted into crossword
    :type word_inserted: int
    """
    global final_result, process_done

    # Check if there's no more slot to fill (basis)
    if word_inserted == len(slot_list):
        final_result = board
        process_done = True
        return True

    # Gather slot data to be filled
    slot_type = slot_list[word_inserted][0]
    start_row = slot_list[word_inserted][1]
    start_col = slot_list[word_inserted][2]
    slot_len = slot_list[word_inserted][3]

    # Try every word with same length as slot
    for word in word_list[slot_len]:

        # Check if word still available to use
        if not word['available']:
            continue

        # If it's available, try to match it to slot
        match = True

        if slot_type == "hor":
            # Check letter by letter horizontally
            for span in range(0, slot_len):
                current_cell = board[start_row][start_col + span]
                if current_cell != char_accessible and current_cell != word['word'][span]:
                    match = False

        elif slot_type == "ver":
            # Check letter by letter vertically
            for span in range(0, slot_len):
                current_cell = board[start_row + span][start_col]
                if current_cell != char_accessible and current_cell != word['word'][span]:
                    match = False

        if match:

            # Try to slot the word in (replace letter by letter), store previous state for backtrack purpose
            previous_state = ""
            for span in range(0, slot_len):

                if slot_type == "hor":
                    previous_state += board[start_row][start_col + span]
                    board[start_row][start_col + span] = word['word'][span]

                elif slot_type == "ver":
                    previous_state += board[start_row + span][start_col]
                    board[start_row + span][start_col] = word['word'][span]

            # Set that word to unavailable (used)
            word['available'] = 0

            # Recursive until all slot filled
            solve_crossword(board, slot_list, word_inserted=word_inserted + 1)

            # Bypass if crossword is solved
            if process_done:
                return

            # If the crossword filled with wrong word, do backtrack
            else:

                # Set previous filled word to available again
                word['available'] = 1

                # Revert crossword to previous condition
                for span in range(0, slot_len):
                    if slot_type == "hor":
                        board[start_row][start_col + span] = previous_state[span]

                    elif slot_type == "ver":
                        board[start_row + span][start_col] = previous_state[span]


if __name__ == "__main__":

    # Gather required information
    board, raw_words = parse_file()
    word_list = group_words_by_len(raw_words)
    #print(word_list)# Separated word by len
    slot_list = get_board_data(board)
    print(slot_list)

    # Solving the crossword
    final_result = None
    process_done = False

    # Start timer
    tic = time.clock()
    solve_crossword(board, slot_list, word_inserted=0)

    # Stop timer
    toc = time.clock()
    print(toc-tic)

    # Display output
    print_board(final_result)
#print_word_list(word_list)