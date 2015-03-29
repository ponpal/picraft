import mcpi.minecraft as minecraft
import mcpi.block as block

mc = minecraft.Minecraft.create()
mc.postToChat("Connected")

BUILD_MODES = ["Solid", "Box", "Demolition", "Dig", "Pool"]

BUILD_MODE_BLOCK = block.CRAFTING_TABLE.id

X_BLOCK = block.COBBLESTONE.id
Y_BLOCK = block.BRICK_BLOCK.id
Z_BLOCK = block.WOOD_PLANKS.id

INC_TYPE_BLOCK = block.GOLD_ORE.id
DEC_TYPE_BLOCK = block.DIAMOND_ORE.id
RESET_TYPE_BLOCK = block.COAL_ORE.id

BUILD_BLOCK = 245 # Weird crafting table
RESET_BLOCK = block.GLASS.id
REMOVE_TOOLS_BLOCK = block.TNT.id

GRASS_BLOCK = block.GRASS.id
SAND_BLOCK = block.SAND.id
POOLSIDE_BLOCK = 24

# Used for placing tools with an offset from the player
OFFSET = 2

# buildMode is initialized to 0 (Pool mode)
buildMode = 0 

# XYZ values used by build modes
bx = by = bz = 0

# Building block type
# Can be used by build modes 
type = block.STONE.id

def nextBuildMode():
	global buildMode
	buildMode = (buildMode + 1) % len(BUILD_MODES) # Cycle through list of build-modes
	mc.postToChat("{0} mode activated".format(BUILD_MODES[buildMode])) 

def createTools():
	pos = mc.player.getPos()
	mc.setBlock(pos.x + OFFSET, pos.y, pos.z - 1, BUILD_MODE_BLOCK)
	
	mc.setBlock(pos.x + OFFSET, pos.y, pos.z, X_BLOCK)
	mc.setBlock(pos.x + OFFSET, pos.y, pos.z + 1, Y_BLOCK)
	mc.setBlock(pos.x + OFFSET, pos.y, pos.z + 2, Z_BLOCK)
	
	mc.setBlock(pos.x + OFFSET, pos.y + 1, pos.z, INC_TYPE_BLOCK)
	mc.setBlock(pos.x + OFFSET, pos.y + 1, pos.z + 1, DEC_TYPE_BLOCK)
	mc.setBlock(pos.x + OFFSET, pos.y + 1, pos.z + 2, RESET_TYPE_BLOCK)

	mc.setBlock(pos.x + OFFSET, pos.y, pos.z + 3, RESET_BLOCK)
	mc.setBlock(pos.x + OFFSET, pos.y + 1, pos.z + 3, REMOVE_TOOLS_BLOCK)

def removeTools(pos):
	# Set all tool blocks to air
	mc.setBlocks(pos.x, pos.y, pos.z,
		     pos.x, pos.y - 1, pos.z - 4,
		     block.AIR.id)

def build(pos):
	if buildMode == 0:
        	buildSolid(pos)
	elif buildMode == 1:
        	buildBox(pos)
        elif buildMode == 2:
        	demolish(pos)
	elif buildMode == 3:
		dig(pos)
	elif buildMode == 4:
	        buildPool(pos)

def buildSolid(pos):
	mc.setBlocks(pos.x, pos.y, pos.z,
                     pos.x + bx, pos.y + by, pos.z + bz,
		     type)

def buildPool(pos):
        # Build solid poolside block
	mc.setBlocks(pos.x, pos.y, pos.z,
                     pos.x + bx, pos.y + by, pos.z + bz, 
		     POOLSIDE_BLOCK)
	
	# Set inner block to water
	mc.setBlocks(pos.x + 1, pos.y + 1, pos.z + 1,
	             pos.x + bx - 1, pos.y + by, pos.z + bz - 1,
		     block.WATER.id)

def buildBox(pos):
	# Build solid block
	mc.setBlocks(pos.x, pos.y - 1, pos.z,
		     pos.x + bx, pos.y + by, pos.z + bz,
		     type)	
	
	# Set inner block to air
	mc.setBlocks(pos.x + 1, pos.y, pos.z + 1,
		     pos.x + bx - 1, pos.y + by - 1, pos.z + bz - 1,
		     block.AIR.id)

def dig(pos):
	mc.setBlocks(pos.x, pos.y, pos.z,
		     pos.x + bx, pos.y - by, pos.z + bz,
		     block.AIR.id)

def demolish(pos):
	mc.setBlocks(pos.x, pos.y, pos.z,
		     pos.x + bx, pos.y + by, pos.z + bz,
		     block.AIR.id)	

def reset():
	global bx, by, bz
	bx = by = bz = 0
	mc.postToChat("Reset")

# Where the magic happens...
while True:
	blockhits = mc.events.pollBlockHits()
	if blockhits:
		for hit in blockhits:
			b = mc.getBlock(hit.pos)

			if b == BUILD_BLOCK:
				build(hit.pos)
			elif b == BUILD_MODE_BLOCK:
				nextBuildMode()
			elif b == GRASS_BLOCK or b == SAND_BLOCK:
				createTools()
			elif b == INC_TYPE_BLOCK:
				type = (type + 1) % 250
				mc.postToChat("Type: {0}".format(type))
			elif b == DEC_TYPE_BLOCK:
				type = (type - 1) % 250
				mc.postToChat("Type: {0}".format(type))
			elif b == RESET_TYPE_BLOCK:
				type = 0
				mc.postToChat("Type: 0")
			elif b == X_BLOCK:
				bx += 1
				mc.postToChat("X: {0}".format(bx + 1))
			elif b == Y_BLOCK:
				by += 1
				mc.postToChat("Y: {0}".format(by + 1))
			elif b == Z_BLOCK:
				bz += 1
				mc.postToChat("Z: {0}".format(bz + 1))
			elif b == RESET_BLOCK:
				reset()
			elif b == REMOVE_TOOLS_BLOCK:
				removeTools(hit.pos)
			else:
				mc.postToChat(b)
