import time

from connectfour import *

max_depth = 5

#evaluation function
#+ if it favours player 1, - if it favours player 2
def evaluate(board):
	#weight by 0.1
	return (total_consecutive_threes(board, True) - total_consecutive_threes(board, False)) * 0.1

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
	for offset in range(-3, 5):
		total_threes += total_consecutive_threes_helper(np.diag(board, k=offset), player_mark)
		total_threes += total_consecutive_threes_helper(np.diag(flipped_board, k=offset), player_mark)
	return total_threes

#return number of 3 consecutive items in a list
def total_consecutive_threes_helper(li, player_mark):
	total_threes = 0
	#counter used to track number of consecutive pieces
	counter = 0
	for val in li:
		if val == player_mark:
			counter += 1
		else:
			counter = 0
		
		if counter >= 3:
			total_threes += 1
	return total_threes

def minimax(board, player_one_turn=True):
	return minimax_helper(board, True, 0, player_one_turn)

def minimax_helper(board, ongoing=True, reward=0, player_one_turn=True, depth=0):
	player_mark = 1 if player_one_turn else -1

	#will return the absolute value
	if not ongoing:
		return reward
	elif depth == max_depth:
		return evaluate(board)

	depth += 1
	scores = []
	moves = get_available_moves(board)

	next_turn = not player_one_turn
	for move in moves:
		possible_board = init_game(board)[0]
		possible_board, ongoing, reward = make_move(possible_board, move, player_one_turn)
		scores.append(minimax_helper(possible_board, ongoing, reward, next_turn, depth))

	if player_one_turn:
		if depth == 1:	
			return moves[np.argmax(scores)]
		return max(scores)
	else:
		if depth == 1:
			return moves[np.argmin(scores)]		
		return min(scores)

if __name__ == '__main__':
	board, _, _ = init_game()

	board, _, _ = make_move(board, 0, False)
	# board, _, _ = make_move(board, 1, False)
	board, _, _ = make_move(board, 0, False)
	# # board, _, _ = make_move(board, 1, False)
	# board, ongoing, reward = make_move(board, 0, False)
	# board, ongoing, reward = make_move(board, 0, False)
	# board, ongoing, reward = make_move(board, 0, False)

	start_time = time.time()
	minimax(board, False)
	print(time.time() - start_time)

	# board, _, _ = make_move(board, 3, True)
	# board, _, _ = make_move(board, 4, True)
	# board, _, _ = make_move(board, 4, True)
	# board, _, _ = make_move(board, 5, True)
	# board, _, _ = make_move(board, 5, False)
	# board, _, _ = make_move(board, 5, True)
	# print(total_consecutive_threes(board))
	# print(board)
	# board, _, _ = make_move(board, 1, False)
	# state = make_move(board, 0,True)    
	# print(state)

	# b, ongoing, reward = init_game()
	# player_one_turn = True
	# while ongoing:
	# 	if player_one_turn:
	# 		move = minimax(b, player_one_turn)
	# 		b, ongoing, reward = make_move(b, move, player_one_turn)
	# 	else:
	# 		user_move = int(input('plese make a move\n'))
	# 		b, ongoing, reward = make_move(b, user_move, player_one_turn)

	# 	print(b)
	# 	print('\n*******NEXT PLAYER*******\n')
	# 	player_one_turn = not player_one_turn
