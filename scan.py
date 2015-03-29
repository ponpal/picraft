from __future__ import division
import mcpi.minecraft as minecraft
import mcpi.block as block
import pickle
from mcpi.vec3 import Vec3

mc = minecraft.Minecraft.create()
mc.postToChat("Connected")

SCAN_INIT  = block.MOSS_STONE.id
DUPLICATE  = block.DIRT.id
WRITE	   = block.GLASS.id
READ	   = block.BOOKSHELF.id

UNDEF_POS = Vec3(-1000, 0, 0)

scanToggle = True # Used for coordinating scan area
scanStart  = UNDEF_POS
scanStop   = UNDEF_POS

blocks  = []
file_id = 0

def setupScan(pos):
	global scanToggle, scanStart, scanStop

	if scanToggle:
		scanStart = pos
		scanToggle = False
		mc.postToChat("Scan start position set")
	else:
		scanStop = Vec3(pos.x + 1, pos.y + 1, pos.z + 1)
		scanToggle = True 
		mc.postToChat("Scan stop position set")
		
def scan(start, stop):
	global blocks

	toScan = ((stop.x - start.x) * 
		  (stop.y - start.y) * 
		  (stop.z - start.z))
	scanned = 0

	if start == UNDEF_POS or stop == UNDEF_POS:
		mc.postToChat("Please define where to start and end the scan")
	else:
		blocks = [] # Clear previous scan
		
		for x in range(start.x, stop.x):
			for y in range(start.y, stop.y):
				for z in range(start.z, stop.z):
					blocks.append([x - start.x, 
						       y - start.y, 
						       z - start.z, mc.getBlock(x, y, z)])
				scanned += (stop.z - start.z)					
				percentage = (scanned / toScan) * 100
				mc.postToChat("Scanning: {0:0.1f}%".format(percentage))
		mc.postToChat("Scan complete")

def duplicate(pos):
	global blocks

	if not blocks:
		mc.postToChat("No scan data available")
	else:							       
		mc.postToChat("Duplicating...")        
		for block in blocks:
				mc.setBlock(pos.x + block[0], 
        	                	    pos.y + block[1], 
                	            	    pos.z + block[2], block[3])
		mc.postToChat("Duplication complete")

def writeBlocks(id):
	global blocks

	mc.postToChat("Saving scanned structure into structures/s{0}.mcs...".format(id))
	file = open("structures/s{0}.mcs".format(id), "w")
	for b in blocks:
		file.write("{0} {1} {2} {3}\n".format(b[0], b[1], b[2], b[3]))
	mc.postToChat("Structure saved")

def readBlocks(id):
	global blocks
	
	blocks = [] # Clear any existing data
	mc.postToChat("Loading structure from structures/s{0}.mcs...".format(id))
	file = open("structures/s{0}.mcs".format(id), "r")
	for line in file:
		x, y, z, t = [int(x) for x in line.split()]
		blocks.append([x, y, z, t])
	mc.postToChat("Structure loaded")

def main():
	while True:
		blockhits = mc.events.pollBlockHits()
		if blockhits:
			for hit in blockhits:
				b = mc.getBlock(hit.pos)

				if b == SCAN_INIT:
					scan(scanStart, scanStop)
				elif b == DUPLICATE:
					duplicate(hit.pos)
				elif b == WRITE:
					writeBlocks(file_id)				
				elif b == READ:
					readBlocks(file_id)
				else:
					setupScan(hit.pos)

if __name__ == '__main__':
	main()
