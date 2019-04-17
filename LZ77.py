import math
from bitarray import bitarray
import time

class LZ77Compressor:
	"""
	A simplified implementation of the LZ77 Compression Algorithm
	"""
	MAX_WINDOW_SIZE = 1023
	MIN_LOOKAHEAD_BUFFER_SIZE = 15

	def __init__(self, window_size=20, lookahead_buffer_size=15):
		self.window_size = min(window_size, self.MAX_WINDOW_SIZE)
		self.window_size_bit = math.ceil(math.log2(self.window_size+1))
		self.lookahead_buffer_size = max(lookahead_buffer_size, self.MIN_LOOKAHEAD_BUFFER_SIZE)
		self.lookahead_buffer_size_bit = math.ceil(math.log2(self.lookahead_buffer_size+1))

	def compress(self, input_file_path, output_file_path):
		"""
		Given the path of an input file, its content is compressed by applying a simple
		LZ77 compression algorithm.

		Before compression, two parameters are attached to the output_buffer:
			the window_size in binary representation
			the lookahead_buffer_size in binary representation
		Both parameters are stored in 10 bits (from 0 to 1023).

		The compressed format is:
		1 bit followed by 8 bits (1 byte character) when there are no previous matches
			within window
		1 bit followed by {param: window_size_bit} bits pointer (distance to the start 
			of the match from the current position), {param: lookahead_buffer_size} 
			bits (length of the match), and 8 bits (1 byte character) when there are 
			previous matches within window.

		Finally, the compressed data is written into a binary file for which the path 
		is provided. 
		"""

		data = None
		i = 0
		output_buffer = bitarray(endian='big')

		start = time.time()

		# read the input file
		try:
			with open(input_file_path, 'rb') as input_file:
				data = input_file.read()
		except IOError:
			print('Could not open input file')
			raise

		# window_size and lookahead_buffer_size is attached to the output_buffer
		# Both parameters are stored in 10 bits
		output_buffer.extend(toBinary(self.window_size_bit,10))
		output_buffer.extend(toBinary(self.lookahead_buffer_size_bit,10))

		while i < len(data):
			match = self.findLongestMatch(data, i)
			print(match)
			if match:
				(bestMatchDistance, bestMatchLength, character) = match

				# Add 1 bit flag, followed by {param: window_size_bit} bit for distance, 
				# and {param: lookahead_buffer_size} bit for the length of the match,
				# and 8 bits (1 byte character)
				output_buffer.append(True)
				output_buffer.extend(toBinary(bestMatchDistance,self.window_size_bit))
				output_buffer.extend(toBinary(bestMatchLength,self.lookahead_buffer_size_bit))
				output_buffer.frombytes(character)

				i += bestMatchLength + 1

			else:
				# No useful match was found. Add 0 bit flag, followed by 8 bit for the character
				output_buffer.append(False)
				output_buffer.frombytes(data[i:i+1])

				i += 1

		# fill the buffer with zeros if the number of bits is not a multiple of 8
		output_buffer.fill()

		# write the compressed data into a binary file
		try:
			with open(output_file_path, 'wb') as output_file:
				output_file.write(output_buffer.tobytes())
				stop = time.time()
				print("The size of orignal file: ", len(data))
				print("The size of compressed file: ", len(output_buffer.tobytes()))
				print("Compressed time: ", stop-start)
				return None
		except IOError:
			print('Could not write to output file path. Please check if the path is correct ...')
			raise

	def decompress(self, input_file_path, output_file_path):
		"""
		Given a string of the compressed file path, the data is decompressed back to its
		original form, and written into the output file path.
		"""
		data = bitarray(endian='big')
		output_buffer = []

		# the variable index stores the index of the element we'are looking at.
		index = 0

		# for experiment use
		start = time.time()

		# read the input file
		try:
			with open(input_file_path, 'rb') as input_file:
				data.fromfile(input_file)
		except IOError:
			print('Could not open input file')
			raise

		# initialize the decompression process by calculating the window_size and 
		# lookahead_buffer_size stored in the data
		window_size = int(data[0:10].to01(),2)
		lookahead_buffer_size = int(data[10:20].to01(),2)
		index += 20

		while len(data) - index >= 9:
			# print(len(data) - index)

			flag = data[index]
			index += 1

			if not flag:
				byte = data[index:index+8].tobytes()
				output_buffer.append(byte)
				index += 8
			else:
				distance = int(data[index:index+window_size].to01(),2)
				length = int(data[index+window_size:index+window_size+lookahead_buffer_size].to01(),2)
				index += window_size+lookahead_buffer_size
				for i in range(length):
					output_buffer.append(output_buffer[-distance])
				if len(data) - index > 7:
					character = data[index:index+8].tobytes()
					output_buffer.append(character)
					index += 8

		# write the decompressed data into a binary file
		try:
			with open(output_file_path, 'wb') as output_file:
				for i in output_buffer:
					output_file.write(i)
				stop = time.time()
				print("Decompression time: ", stop-start)
				print('File was decompressed successfully and saved to output path ...')
				return None
		except IOError:
			print('Could not write to output file path. Please check if the path is correct ...')
			raise


	def findLongestMatch(self, data, current_position):
		"""
		Finds the longest match to a substring starting at the current_position
		in the lookahead buffer from the history window
		"""
		end_of_buffer = min(current_position + self.lookahead_buffer_size, len(data))

		best_match_distance = -1
		best_match_length = -1
		window = ""
		character = ""
		flag = False

		start_index = max(0, current_position - self.window_size)

		for j in range(current_position + 1, end_of_buffer):

			substring = data[current_position:j]
			if best_match_length < current_position - start_index:
				window = data[start_index: current_position]
			else:
				window = data[start_index: start_index+len(substring)]

			# print(substring, window, best_match_length, best_match_distance,current_position-start_index)

			if substring in window:
				if best_match_length < current_position-start_index:
					best_match_length = len(substring);
					best_match_distance = len(window)-window.rfind(substring)
				else:
					best_match_length = len(substring);
					if j == end_of_buffer - 1:
						flag = True
				character = data[j:j+1];
				if flag:
					character = b''
					best_match_length += 1
			else:
				break
		if best_match_distance > 0 and best_match_length > 0:
			return (best_match_distance, best_match_length, character)
		return None

# return the binary representation of {param: num} that consists of {param: bits} bits
# num: the input integer
# bit: the length of output list
def toBinary(num,bit):
	output = format(num,"b")
	while len(output) < bit:
		output = "0" + output
	return output