import mcpi.minecraft as minecraft
import mcpi.block as block
from mcpi.vec3 import Vec3

mc = minecraft.Minecraft.create()
mc.postToChat("Connected")

def main():
	mc.postToChat("Removing obstacles")
	mc.setBlocks(-128, 0, -128, 128, 100, 128, block.AIR.id)
	mc.postToChat("Creating floor")
	mc.setBlocks(-128, -5, -128, 128,   0, 128, 155)
	mc.postToChat("Flatmap created")

if __name__ == '__main__':
	main()
