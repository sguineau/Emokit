import emotiv
headset = emotiv.Emotiv()

'''
string_to_num(string)
Converts a string, 'string' into a number that represents its binary notation.
'a' becomes '61' and 'aa' becomes '61 61'
'''
def string_to_num(string):
	binary = "" #Binary is an empty string
	for char in string: #For each character in the provided 'string'
		binary += char_to_bin(char) #Append the binary representation string of the character to binary
	return int(binary, 2) #Convert the binary into an integer and return.

'''
char_to_bin(char)
Converts a character into its corresponding binary number
'''
def char_to_bin(char):
	ascii = ord(char) #Convert char into an integer that represents it. 'a' becomes '61'
	bin = [] #an empty array to store the binary representation of char

	while (ascii > 0): #While the value is positive (greater than 0), there are still 1-bits left
		#Append a 1 to the array if the least significant bit is 1
		if (ascii & 1) == 1:
			bin.append("1")
		#Append a 0 otherwise
		else:
			bin.append("0")
		ascii = ascii >> 1 #Shift the bits of ascii over so the next iteration deals with the next bit
			
	bin.reverse() #The array char was evaluated backwards, so reverse the array.
	binary = "".join(bin) #Convert the array into a string
	return binary.zfill(8) #Ensure that each char is 8 bits long by appending 0's to the start and return.

'''
printStream()
Prints out a formatted version of the bitstream the headset sends.
Saves all data to output.txt
'''
def printStream():
	try:
		f = open('output.txt', 'w') #Open the output.txt file for writing
		while True: #Continuously loop through (allows for user to turn on / off the headset without change in the program
			for packet in headset.dequeue(): #headset.dequeue contains a list of sent packets that need to be evaluated.
				printString = ("%x" % string_to_num(packet.data)).zfill(64) #Convert the packet string into a 64-character hexstring
				#Write and print the first block of data (from 0 to the first byte of the first block of bytes in discoveredBytes
				f.write(printString[0:discoveredBytes[0][0] * 2])
				print   printString[0:discoveredBytes[0][0] * 2],
				
				#Loop through each of the discoveredBytes
				for i in range(0, len(discoveredBytes)):
					#Print out a '.' followed by the interesting block of bytes
					f.write("." + printString[discoveredBytes[i][0] * 2: discoveredBytes[i][-1] * 2 + 2] + " ")
					print   "." + printString[discoveredBytes[i][0] * 2: discoveredBytes[i][-1] * 2 + 2],
					
					#Fill in the bytes between the current block of discoveredBytes and the next one.
					#Ignore if you're working with the last block.
					if i < len(discoveredBytes) - 1:
						f.write(printString[discoveredBytes[i][-1] * 2 + 2: discoveredBytes[i + 1][-1] * 2] + " ")
						print   printString[discoveredBytes[i][-1] * 2 + 2: discoveredBytes[i + 1][-1] * 2],
				
				#Print out any remaining bytes in the stream.
				f.write(printString[discoveredBytes[-1][-1] * 2 + 2:])
				f.write("\n")
				print   printString[discoveredBytes[-1][-1] * 2 + 2:]
	finally:
		headset.close()

'''
discoveredBytes
An array that contains all byte ranges that may be of interest.

Each entry into the array is of the form [i, j] where i is the start byte and j is the end byte.

Entering [i, j] into this array will cause the printout to single out the specified bytes.
For instance, in a 8-byte stream:
	0123456789ABCDEF
Entering [3, 5] will result in:
	0123 .456789 ABCDEF
The . denotes a block that is defined in this array.

Each [i, j] is interpretted by evaluating the first and last item in the array, so [3] is the same as [3, 3] and [3, 4, 3].

Known values (as found from :
	[0] is the first byte and is known to be a counter.
	[29] and [30] are bytes for the accelerometer
'''
discoveredBytes = [[0], [29], [30]]

printStream()
