import mcpi.minecraft as minecraft
import math
import time

AS_STRING = ["EAST", "NORTH", "WEST", "SOUTH"]
AS_VECTOR = [[1, 1], [-1, 1], [-1, -1], [1, -1]]

# Constant used to acknowledge the fact that block positions are
# not at the center of the blocks.
CORRECTION = 0.5

# Returns the angle in degrees between the player and the blockhit
def getHitAngle(player, hit):
	deltaX = hit.x + CORRECTION - player.x
	deltaZ = hit.z + CORRECTION - player.z

	return getAngle(deltaX, deltaZ)

# Returns the angle in degrees given differences in X and Z.
def getAngle(deltaX, deltaZ):
	return (math.atan2(deltaX, deltaZ) * (180 / math.pi)) % 360

# Returns an int representation of the direction from a to b.
# The returned int can be used as an index in DIR_STR to
# retrieve a string representation.
def getDirectionFromPoints(a, b):
	angle = getAngle(b.x - a.x, b.z - a.z)
	return getDirection(angle)

# Returns an int representation of the direction given an angle.
# The returned int can be used as an index for DIR_STR to
# retrieve a string representation.
def getDirection(angle):
	if 45 < angle <= 135:
		return 0 # EAST
	if 135 < angle <= 225:
		return 1 # NORTH
	if 225 < angle <= 315:
		return 2 # WEST
	if angle > 315 or angle <= 45:
		return 3 # SOUTH

# Returns true if the positions p1 and p2 are not the same 
# ie. the measured object is moving, false otherwise.
def moving(p1, p2):
	return p1.x != p2.x or p1.z != p2.z 

# Sample usage of the above functions. Prints the direction 
# of the player in the console everytime it changes.
def main():
	mc = minecraft.Minecraft.create()
	mc.postToChat("Connected")

	oldPos = mc.player.getPos()
	oldDir = "UNDEFINED"

	while True:
		newPos = mc.player.getPos()
		newDir = getDirectionFromPoints(oldPos, newPos)

		# Hack to keep direction from being set to EAST 
		# when the player stops moving
		if not moving(oldPos, newPos):
			newDir = oldDir 			

		if newDir != oldDir:
			print "Moving {0}.".format(AS_STRING[newDir].lower())
	
		oldPos = newPos
		oldDir = newDir
		time.sleep(0.1)

if __name__ == "__main__":
	main()
