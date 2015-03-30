import mcpi.minecraft as minecraft
import math
import time
from mcpi.vec3 import Vec3

mc = minecraft.Minecraft.create()
mc.postToChat("Connected")

# Acknowledges the fact that block positions
# are not at the center of the blocks.
CORRECTION = 0.5

# Returns the angle in degrees between the player and the blockhit
def getHitAngle(hit, player):
	deltaX = hit.x + CORRECTION - player.x
	deltaZ = hit.z + CORRECTION - player.z

	return getAngle(deltaX, deltaZ)

# Returns the angle given the differences in X and Z.
def getAngle(deltaX, deltaZ):
	return (math.atan2(deltaX, deltaZ) * (180 / math.pi)) % 360

# Returns a string representation of the direction from a to b
def getDirection(a, b):
	angle = getAngle(b.x - a.x, b.z - a.z)
	
	if angle > 45 and angle <= 135:
		return "NORTH"
	if angle > 135 and angle <= 225:
		return "WEST"
	if angle > 225 and angle <= 315:
		return "SOUTH"
	if angle > 315 or angle <= 45:
		return "EAST"

# Returns true if the positions p1 and p2 are not the same, false otherwise
def moving(p1, p2):
	return p1.x != p2.x or p1.z != p2.z 

def main():
	oldPos = mc.player.getPos()
	oldDir = "UNDEFINED"

	while True:
		newPos = mc.player.getPos()
		newDir = getDirection(oldPos, newPos)	

		# Hack to keep direction from being set to EAST 
		# when the player stops moving
		if not moving(oldPos, newPos):
			newDir = oldDir 			

		if newDir != oldDir:
			print "Walking {0}".format(newDir)
	
		oldPos = newPos
		oldDir = newDir
		time.sleep(0.1)

if __name__ == "__main__":
	main()
