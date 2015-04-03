from __future__ import division
from mcpi.vec3 import Vec3
import mcpi.minecraft as minecraft
import mcpi.block as block
import direction as dir

mc = minecraft.Minecraft.create()
mc.postToChat("Connected")

SCAN_INIT  = block.NETHER_REACTOR_CORE.id
DUPLICATE  = block.DIRT.id
WRITE	   = block.CRAFTING_TABLE.id
READ	   = block.BOOKSHELF.id

UNDEF_POS = Vec3(-1000, 0, 0)

SPECIAL_BLOCKS = [block.BED.id,
                  block.TORCH.id,
                  block.DOOR_WOOD.id,
                  block.LADDER.id,
                  block.FENCE.id,
                  block.GLASS_PANE.id,
                  block.FENCE_GATE.id]

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

	if start == UNDEF_POS or stop == UNDEF_POS:
		mc.postToChat("Please define where to start and end the scan")
	else:
                toScan = ((stop.x - start.x) * 
                          (stop.y - start.y) * 
                          (stop.z - start.z))
                scanned = 0
		blocks = [] # Clear previous scan

                # Special blocks that should be added to the end of the scanned
                # data for correct duplication.
                specials = [] 
		
		for x in range(start.x, stop.x):
			for y in range(start.y, stop.y):
				for z in range(start.z, stop.z):
                                        bx = x - start.x
                                        by = y - start.y
                                        bz = z - start.z
					type, data = mc.getBlockWithData(x, y, z)

                                        if type in SPECIAL_BLOCKS:
                                                specials.append([bx, by, bz, type, data])
                                        else:
                                                blocks.append([bx, by, bz, type, data])
				scanned += (stop.z - start.z)
				percentage = (scanned / toScan) * 100
				mc.postToChat("Scanning: {0:0.1f}%".format(percentage))
                blocks.extend(specials)
		mc.postToChat("Scan complete")
                
def duplicate(playerPos, hitPos):
	global blocks

        direction = dir.getDirectionFromPoints(playerPos, hitPos)
        dirvec = dir.AS_VECTOR[direction]
        dirstr = dir.AS_STRING[direction]
        
        mc.postToChat("X: {0} Y: {1} ({2})".format(dirvec[0], dirvec[1], dirstr))
        
	if not blocks:
		mc.postToChat("No scan data available for duplication")
	else:							       
		mc.postToChat("Duplicating...")        
		for block in blocks:
				mc.setBlock(hitPos.x + block[0] * direction[0], 
        	                	    hitPos.y + block[1], 
                	            	    hitPos.z + block[2] * direction[1],
                                            block[3],
                                            block[4])
		mc.postToChat("Duplication complete")

def writeBlocks(id):
	global blocks

	mc.postToChat("Saving scanned structure into structures/s{0}.mcs...".format(id))
	file = open("structures/s{0}.mcs".format(id), "w")
	for b in blocks:
		file.write("{0} {1} {2} {3} {4}\n".format(
			b[0], b[1], b[2], b[3], b[4]))
	mc.postToChat("Structure saved")

def readBlocks(id):
	global blocks
	
	blocks = [] # Clear any existing data
	mc.postToChat("Loading structure from structures/s{0}.mcs...".format(id))
	file = open("structures/s{0}.mcs".format(id), "r")
	for line in file:
		x, y, z, t, d = [int(x) for x in line.split()]
		blocks.append([x, y, z, t, d])
	mc.postToChat("Structure loaded")

def main():
	while True:
                playerPos = mc.player.getPos()
		blockhits = mc.events.pollBlockHits()
		if blockhits:
			for hit in blockhits:
				b = mc.getBlock(hit.pos)

				if b == SCAN_INIT:
					scan(scanStart, scanStop)
				elif b == DUPLICATE:
					duplicate(playerPos, hit.pos)
				elif b == WRITE:
					writeBlocks(file_id)				
				elif b == READ:
					readBlocks(file_id)
				else:
					setupScan(hit.pos)

if __name__ == '__main__':
	main()
