#!/usr/bin/python3

import struct
from PIL import Image

# Re-create the ROM memory space
lines = [0] * 0x200000

# Load line data
r1 = open('D400.bin', 'rb').read()
r2 = open('D401.bin', 'rb').read()

# De-interleave shorts
for x in range(0, len(r1), 2):
	lines[x * 2 + 0] = r1[x + 0]
	lines[x * 2 + 1] = r1[x + 1]
	lines[x * 2 + 2] = r2[x + 0]
	lines[x * 2 + 3] = r2[x + 1]

# Load the second set of ROMs at 0x80000
r1 = open('D402.bin', 'rb').read()
r2 = open('D403.bin', 'rb').read()

# De-interleave shorts
for x in range(0, len(r1), 2):
	lines[0x80000 + x * 2 + 0] = r1[x + 0]
	lines[0x80000 + x * 2 + 1] = r1[x + 1]
	lines[0x80000 + x * 2 + 2] = r2[x + 0]
	lines[0x80000 + x * 2 + 3] = r2[x + 1]

# Load the third set of ROMs at 0x100000
r1 = open('D404.bin', 'rb').read()
r2 = open('D405.bin', 'rb').read()

# De-interleave shorts
for x in range(0, len(r1), 2):
	lines[0x100000 + x * 2 + 0] = r1[x + 0]
	lines[0x100000 + x * 2 + 1] = r1[x + 1]
	lines[0x100000 + x * 2 + 2] = r2[x + 0]
	lines[0x100000 + x * 2 + 3] = r2[x + 1]

# Load the test pattern data
sequence = open('D408.bin', 'rb').read()
sequence = [struct.unpack('H', sequence[x:x + 2])[0] for x in range(0, len(sequence), 2)]

images = [sequence[x:x + 625] for x in range(0, len(sequence), 0x400)]

print('Dumping %d images...' % (len(sequence) / 0x400))

for i in range(0, len(images)):
	img = b''
	
	for x in range(0, 625):
		
		#x = (312 * x) % 625
		x = images[i][x]
		
		if x == 0xFFFF:
			# Undefined line, send all black
			line = b'\x00' * 1088
		
		else:
			line = bytes(lines[x * 64:x * 64 + 1088])
		
		# Incomplete line?
		if len(line) != 1088:
			print(hex(x))
			line = b'\x00' * 1088
		
		img += line
	
	Image.frombuffer('L', (1088, 625), img, 'raw', 'L', 0, 1).save('image%02d.png' % i, 'PNG')

print('Wrote %d lines, %d frames' % (len(sequence), len(sequence) / 1024))

