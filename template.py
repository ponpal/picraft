import mcpi.minecraft as minecraft

def main():
	mc = minecraft.Minecraft.create()
	mc.postToChat("Connected")
	
if __name__ == '__main__':
	main()
