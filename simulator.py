import os
from LZ77 import LZ77Compressor

input_file_path = "sample.txt"
output_file_path = "test/abc"
decompressed_file_path = "samplea.txt"
compressor = LZ77Compressor(400,100)
# compressor.compress(input_file_path,output_file_path)
compressor.decompress(output_file_path,decompressed_file_path)

# encoder experimental for different window size
# input_file_path = "test/lcet10/lcet10.txt"
# window_size_list = [15,20,50,100,200,400,600,800,1000]

# for i in window_size_list:
# 	compressor = LZ77Compressor(i,15)
# 	output_file_path = "test/lcet10/result/asyoulik_window_size_"+str(i)
# 	compressor.compress(input_file_path,output_file_path)

# encoder/decoder experimental for different window size
# input_file_path = "test/asyoulik/result/asyoulik_alookahead_buffer_size_"
# window_size_list = [15,20,50,100,200,400,600,800,1000]current_position-start_index

# for i in window_size_list:
# 	compressor = LZ77Compressor(i,15)
# 	output_file_path = "test/asyoulik/result/decompress/asyoulik_decompress_lookahead_"+str(i)+".txt"
# 	compressor.decompress(input_file_path+str(i),output_file_path)

# experimental for different lookahead buffer size
# input_file_path = "test/asyoulik/asyoulik.txt"
# lookahead_buffer_size = [15,20,50,100,200,400,600,800,1000]

# for i in lookahead_buffer_size:
# 	compressor = LZ77Compressor(400,i)
# 	output_file_path = "test/asyoulik/result/asyoulik_alookahead_buffer_size_"+str(i)
# 	compressor.compress(input_file_path,output_file_path)

# experimental for different lookahead buffer size
# file_size = [10,20,50,100,200,500,1000]

# for i in file_size:
# 	compressor = LZ77Compressor(400,15)
# 	input_file_path = "test/size/SampleTextFile_"+str(i)+"kb.txt"
# 	output_file_path = "test/size/result/SampleTextFile_output_"+str(i)
# 	compressor.compress(input_file_path,output_file_path)

# encode experiment for different file type
# input_file_directory = "test/type/"
# output_file_directory = "test/type/result/"

# files = os.listdir(input_file_directory)
# for f in files:
# 	if f == "result":
# 		continue
# 	else:
# 		print(f)
# 	compressor = LZ77Compressor(400,15)
# 	input_file_path = input_file_directory+f
# 	output_file_path = output_file_directory+f
# 	compressor.compress(input_file_path,output_file_path)
# 	print()

# decoder experiment for different file type
# input_file_directory = "test/type/result/"
# output_file_directory = "test/type/result/decompress/"

# files = os.listdir(input_file_directory)
# for f in files:
# 	if f == "decompress":
# 		continue
# 	else:
# 		print(f)
# 	compressor = LZ77Compressor(400,15)
# 	input_file_path = input_file_directory+f
# 	output_file_path = output_file_directory+f
# 	compressor.decompress(input_file_path,output_file_path)
# 	print()

# running time wide range window size
# input_file_path = "test/lcet10/lcet10.txt"
# for i in range(10,5001,10):
# 	compressor = LZ77Compressor(i,15)
# 	output_file_path = "test/lcet10/output/lcet10_window_size_"+str(i)
# 	compressor.compress(input_file_path,output_file_path)
# input_file_path = "test/asyoulik/asyoulik.txt"
# for i in range(10,5001,10):
# 	compressor = LZ77Compressor(i,15)
# 	output_file_path = "test/asyoulik/output/asyoulik_window_size_"+str(i)
# 	compressor.compress(input_file_path,output_file_path)