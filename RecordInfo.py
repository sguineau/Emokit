import emotiv
headset = emotiv.Emotiv()
	
def string_to_num(string):
	binary = ""
	for char in string:
		binary += char_to_bin(char)
	return int(binary, 2)
def char_to_bin(char):
	ascii = ord(char)
	bin = []

	while (ascii > 0):
		if (ascii & 1) == 1:
			bin.append("1")
		else:
			bin.append("0")
		ascii = ascii >> 1
			
	bin.reverse()
	binary = "".join(bin)	
	return binary.zfill(8)

def countZero(data, counts, first = False):
	index = 0
	while(data > 0):
		if (data & 1) == 1:
			if first:
				counts.append(1)
			else:
				counts[index] += 1
		elif first:
				counts.append(0)
		index += 1
		data = data >> 1

discoveredBytes = [[0]]
try:
	f = open('output.txt', 'w')
	while True:
		for packet in headset.dequeue():
			printString = ("%x" % string_to_num(packet.data)).zfill(64)
			f.write(printString[0:discoveredBytes[0][0] * 2])
			print   printString[0:discoveredBytes[0][0] * 2],
			for i in range(0, len(discoveredBytes)):
				f.write(printString[discoveredBytes[i][0] * 2: discoveredBytes[i][-1] * 2 + 2] + " ")
				print   printString[discoveredBytes[i][0] * 2: discoveredBytes[i][-1] * 2 + 2],
				if i < len(discoveredBytes) - 1:
					f.write(printString[discoveredBytes[i][-1] * 2 + 2: discoveredBytes[i + 1][-1] * 2] + " ")
					print   printString[discoveredBytes[i][-1] * 2 + 2: discoveredBytes[i + 1][-1] * 2],
			f.write(printString[discoveredBytes[-1][-1] * 2 + 2:])
			print   printString[discoveredBytes[-1][-1] * 2 + 2:]
			f.write("\n")
finally:
	headset.close()
	
	
	
	
	
	