import time

from connectfour import *

max_depth = 5

hash_table = {}

#evaluation function
#+ if it favours player 1, - if it favours player 2
def evaluate(board):
	#weight by 0.1
	return (total_consecutive_threes(board, True) - total_consecutive_threes(board, False)) * 0.1

#returns total number of 3s in a board
#note that if the 3s have no space next to it to become connect four, we do not count it
def total_consecutive_threes(board, player_one_turn=True):
	player_mark = 1 if player_one_turn else -1 
	total_threes = 0
	#for diagonals
	flipped_board = np.fliplr(board)
	#horizontal
	total_threes += sum([total_consecutive_threes_helper(row, player_mark) for row in board])
	#vertical (transpose the board)
	total_threes += sum([total_consecutive_threes_helper(row, player_mark) for row in board.T])

	#for diagonals - KIV (note that this is only for a 6x7 connect four board)
	#we do not include diagonals that have max length of 3 since we can't win with them
	for offset in range(-2, 4):
		total_threes += total_consecutive_threes_helper(np.diag(board, k=offset), player_mark)
		total_threes += total_consecutive_threes_helper(np.diag(flipped_board, k=offset), player_mark)
	return total_threes

#return number of 3 consecutive items in a list
def total_consecutive_threes_helper(li, player_mark):
	total_threes = 0

	#counter used to track number of consecutive pieces
	counter = 0
	start_index = None
	for i, val in enumerate(li):
		if val == player_mark:
			counter += 1
			if start_index == None:
				start_index = i
		else:
			counter = 0
			start_index = None
		
		if counter >= 3:
			#tests for empty space either before or after the sequence
			if ((start_index - 1 >= 0) and (li[start_index - 1] == 0)) or ((i + 1 < len(li) - 1) and (li[i + 1] == 0)):
				total_threes += 1
	return total_threes

def minimax(board, player_one_turn=True):
	#opening move when board is empty (place in center)
	if len(np.where(board == 0)[0]) == 6 * 7:
		return 3
	return minimax_helper(board, player_one_turn)

def minimax_helper(board, player_one_turn, status='ongoing', depth=0):
	player_mark = 1 if player_one_turn else -1

	#see if value is already stored
	hashed_board = board.tostring()
	if depth > 0 and hashed_board in hash_table:
		return hash_table[hashed_board]

	#game has ended
	elif status != 'ongoing':
		return get_reward(status)
	elif depth == max_depth:
		return evaluate(board)

	depth += 1
	scores = []
	moves = get_available_moves(board)

	next_turn = not player_one_turn
	for move in moves:
		possible_board = init_game(board)[0]
		possible_board, status = make_move(possible_board, move, player_one_turn)
		scores.append(minimax_helper(possible_board, next_turn, status, depth))

	if player_one_turn:
		if depth == 1:	
			return moves[np.argmax(scores)]

		#store value in hash table
		hash_table[board.tostring()] = max(scores)
		return max(scores)
	else:
		if depth == 1:
			return moves[np.argmin(scores)]

		#store value in hash table	
		hash_table[board.tostring()] = min(scores)			
		return min(scores)

if __name__ == '__main__':
	# s = convert(board)
	# print(s)
	# print('***')
	# print(convert(s, False))

	# board, _, _ = make_move(board, 0, False)
	# board, _, _ = make_move(board, 1, False)
	# # board, _, _ = make_move(board, 0, True)
	# board, _, _ = make_move(board, 0, False)
	# board, _, _ = make_move(board, 0, True)
	# board, _, _ = make_move(board, 0, True)
	# board, _, _ = make_move(board, 0, True)
	# board, _, _ = make_move(board, 0, False)
	# # board, _, _ = make_move(board, 1, False)
	# board, ongoing, reward = make_move(board, 0, False)
	# board, ongoing, reward = make_move(board, 0, False)
	# board, ongoing, reward = make_move(board, 0, False)

	# print(board)
	# print(total_consecutive_threes(board, True))
	# start_time = time.time()
	# minimax(board, False)
	# print(time.time() - start_time)
	# print(board)

	b, status = init_game()
	player_one_turn = True
	while status == 'ongoing':
		if player_one_turn:
			start_time = time.time()
			move = minimax(b, player_one_turn)
			print('Time taken: {:.2f}s'.format(time.time() - start_time))
			print('AI Move: {}'.format(move))
			b, status = make_move(b, move, player_one_turn)
		else:
			user_move = int(input('plese make a move\n'))
			b, status = make_move(b, user_move, player_one_turn)

		print(b)
		print('\n*******NEXT PLAYER*******\n')
		player_one_turn = not player_one_turn
