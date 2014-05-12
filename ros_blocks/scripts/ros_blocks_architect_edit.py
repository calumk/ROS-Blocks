#!/usr/bin/env python
#    _____                            _       
#   |_   _|                          | |      
#     | |  _ __ ___  _ __   ___  _ __| |_ ___ 
#     | | | '_ ` _ \| '_ \ / _ \| '__| __/ __|
#    _| |_| | | | | | |_) | (_) | |  | |_\__ \
#   |_____|_| |_| |_| .__/ \___/|_|   \__|___/
#                   | |                       
#                   |_|                       

import cv2
import cv
import numpy as np
import SimpleCV as scv
import os
import shutil









class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    CYAN = '\033[96m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''

def printGreen(input):
	print bcolors.OKGREEN + input + bcolors.ENDC
def printCyan(input):
	print bcolors.CYAN + input + bcolors.ENDC
def printYellow(input):
	print bcolors.WARNING + input + bcolors.ENDC
def printBlue(input):
	print bcolors.OKBLUE + input + bcolors.ENDC
def printRed(input):
	print bcolors.FAIL + input + bcolors.ENDC
def printHeader(input):
	print bcolors.HEADER + input + bcolors.ENDC



path = os.path.dirname(os.path.realpath(__file__))
#    __  __      _   _               _     
#   |  \/  |    | | | |             | |    
#   | \  / | ___| |_| |__   ___   __| |___ 
#   | |\/| |/ _ \ __| '_ \ / _ \ / _` / __|
#   | |  | |  __/ |_| | | | (_) | (_| \__ \
#   |_|  |_|\___|\__|_| |_|\___/ \__,_|___/
#                                          
#                                          

def roundto25(number):
	return int(round(number / 25.0) * 25)
	#return number

output = ""
outputArr = []
highestY = 0
lowestX = 1000000
singleBlockHeight = False



def namestr(obj, namespace):
    return [name for name in namespace if namespace[name] is obj]

#    ______                           _                 _            
#   |  ____|                         | |               | |           
#   | |__ ___  _ __    ___  __ _  ___| |__     ___ ___ | | ___  _ __ 
#   |  __/ _ \| '__|  / _ \/ _` |/ __| '_ \   / __/ _ \| |/ _ \| '__|
#   | | | (_) | |    |  __/ (_| | (__| | | | | (_| (_) | | (_) | |   
#   |_|  \___/|_|     \___|\__,_|\___|_| |_|  \___\___/|_|\___/|_|   
#                                                                    
#                                                                    

for filenameA in os.listdir(path+'/ros_blocks_basilisk/out/'):

	#     _____       _ _ _     _     _       _         
	#    / ____|     | (_) |   | |   | |     | |        
	#   | (___  _ __ | |_| |_  | |__ | | ___ | |__  ___ 
	#    \___ \| '_ \| | | __| | '_ \| |/ _ \| '_ \/ __|
	#    ____) | |_) | | | |_  | |_) | | (_) | |_) \__ \
	#   |_____/| .__/|_|_|\__| |_.__/|_|\___/|_.__/|___/
	#          | |                                      
	#          |_|                                      

	img = scv.Image(path+'/ros_blocks_basilisk/out/'+filenameA)
	#img.show()
	blobs = img.findBlobs()
	counter = 0
	xyArr = []

	for b in blobs:
		save_path = path+"/ros_blocks_basilisk/temp/img-" + str(counter) + ".png"
		img.crop(b).save(save_path)
		counter += 1
		xyArr.append([b.x,b.y])


	#    ______                           _       _     _       _     
	#   |  ____|                         | |     | |   | |     | |    
	#   | |__ ___  _ __    ___  __ _  ___| |__   | |__ | | ___ | |__  
	#   |  __/ _ \| '__|  / _ \/ _` |/ __| '_ \  | '_ \| |/ _ \| '_ \ 
	#   | | | (_) | |    |  __/ (_| | (__| | | | | |_) | | (_) | |_) |
	#   |_|  \___/|_|     \___|\__,_|\___|_| |_| |_.__/|_|\___/|_.__/ 
	#                                                                 
	#                                                                 

	counter = 0	
	for filename in os.listdir(path+'/ros_blocks_basilisk/temp/'):
		print filename
		bestret = 1.0000
		bestretxtra = 1.0000

		which = 0
		whichxtra = 0

		simg = cv2.imread(path+'/ros_blocks_basilisk/temp/'+filename,0)

		cube = cv2.imread(path+'/ros_blocks_basilisk/shapes/cube.png',0)
		cuboid = cv2.imread(path+'/ros_blocks_basilisk/shapes2/cuboid.png',0)
		bridge = cv2.imread(path+'/ros_blocks_basilisk/shapes2/bridge.png',0)
		window = cv2.imread(path+'/ros_blocks_basilisk/shapes2/window.png',0)
		pillar = cv2.imread(path+'/ros_blocks_basilisk/shapes2/pillar.png',0)

		bridge_CubeLeft = cv2.imread(path+'/ros_blocks_basilisk/shapes2/xtraShapes/bridge_CubeLeft.png',0)
		bridge_CubeRight = cv2.imread(path+'/ros_blocks_basilisk/shapes2/xtraShapes/bridge_CubeRight.png',0)
		bridge_CubeCenter = cv2.imread(path+'/ros_blocks_basilisk/shapes2/xtraShapes/bridge_CubeCenter.png',0)
		bridge_CubeFarLeft = cv2.imread(path+'/ros_blocks_basilisk/shapes2/xtraShapes/bridge_CubeFarLeft.png',0)
		bridge_CubeFarRight = cv2.imread(path+'/ros_blocks_basilisk/shapes2/xtraShapes/bridge_CubeFarRight.png',0)

		images = [cube,cuboid,bridge,window,pillar]

		xtraImages = [bridge_CubeLeft,bridge_CubeRight,bridge_CubeCenter,bridge_CubeFarLeft,bridge_CubeFarRight]

		allImages = images + xtraImages

		imagesInfo = ["blockType_cube_h","blockType_cuboid_h","blockType_bridge_h","blockType_window_h","blockType_pillar_h"]
		
		xtraInfo = ["crap","crap","crap","crap","crap"]


		allImagesInfo = imagesInfo + xtraInfo

		ret, thresh = cv2.threshold(simg, 127, 255,0)
		contours,hierarchy = cv2.findContours(thresh,2,1)
		scnt = contours[0]

		#    ______ _           _        _                     _   
		#   |  ____(_)         | |      | |                   | |  
		#   | |__   _ _ __   __| |   ___| | ___  ___  ___  ___| |_ 
		#   |  __| | | '_ \ / _` |  / __| |/ _ \/ __|/ _ \/ __| __|
		#   | |    | | | | | (_| | | (__| | (_) \__ \  __/\__ \ |_ 
		#   |_|    |_|_| |_|\__,_|  \___|_|\___/|___/\___||___/\__|
		#                                                          
		#     

		height, width = simg.shape
		if height > 45:
			if width > 45:                                                     

				for i in range(len(images)):
					ret, thresh2 = cv2.threshold(images[i], 127, 255,0)
					contours,hierarchy = cv2.findContours(thresh2,2,1)
					cnt2 = contours[0]
					ret = cv2.matchShapes(scnt,cnt2,1,0.0)
					print str(ret) + " : " + str(namestr(images[i], globals()))
					if ret < bestret:
						bestret = ret
						which = i


				printYellow("Currently the best match is..... " + str(which) + " : " + str(namestr(images[which], globals())))
				if bestret > 0.2:
					print " "
					print "It MIGHT be xtraShape"
					print "Comapring..."
					print " "
					

					for i in range(len(xtraImages)):
						ret, thresh2 = cv2.threshold(xtraImages[i], 127, 255,0)
						contours,hierarchy = cv2.findContours(thresh2,2,1)
						cnt2 = contours[0]
						ret = cv2.matchShapes(scnt,cnt2,1,0.0)
						printBlue("---" + str(ret) + " : " + str(namestr(xtraImages[i], globals())) )
						if ((ret < bestretxtra) & (ret < bestretxtra)):
							bestretxtra = ret
							whichxtra = i

					print ""
					printYellow ( "---The best xTra is...." )
					printYellow ( "----" + str(bestretxtra) + " : " + str(namestr(xtraImages[whichxtra], globals())) )
					print ""

					if bestretxtra < bestret:
						printCyan( "---The xTra shape is a better fit!:" )
						printCyan( "----" + str(bestretxtra) + " : " + str(namestr(xtraImages[whichxtra], globals())) )
						which = whichxtra + len(xtraImages)
					else:
						printCyan( "---The Origional shape is a better fit!:" )
						printCyan( "----" + str(bestret) + " : " + str(namestr(images[which], globals())) )
					print ""

				else:
					print ""
					print "NOT checking xtraShapes"
					print ""



				printGreen( "Shape Identified as: "+str(which)+" : " + str(namestr(allImages[which], globals()))  )

				outputed = False

				if which >= len(images): 
					outputed = True
					print ""
					print "Adding vals to outputArr: "
					filenameDesc = str(namestr(allImages[which], globals()))[2:-2]
					print filenameDesc
					with open (path+"/ros_blocks_basilisk/shapes2/xtraShapes/" + filenameDesc + ".blks", "r") as myfile:
						data=myfile.readlines()
					print ""
					print len(data)
					print len(data)/3

					print ""
					for i in range(len(data)/3):
						print data[(i*3)].replace('\n', '')
						print data[(i*3)+1].replace('\n', '')
						print data[(i*3)+2].replace('\n', '')
						x = int(data[(i*3)].replace('\n', ''))
						y = int(data[(i*3)+1].replace('\n', ''))
						x = x*25
						y = y*25
						outputArr.append([data[(i*3)+2].replace('\n', ''),"color_red",roundto25(xyArr[counter][0])+x,roundto25(xyArr[counter][1])-y])



					print ""
					print ""
				#    ______ _           _            _           _                   
				#   |  ____(_)         | |          (_)         | |                  
				#   | |__   _ _ __   __| | __      ___ _ __   __| | _____      _____ 
				#   |  __| | | '_ \ / _` | \ \ /\ / / | '_ \ / _` |/ _ \ \ /\ / / __|
				#   | |    | | | | | (_| |  \ V  V /| | | | | (_| | (_) \ V  V /\__ \
				#   |_|    |_|_| |_|\__,_|   \_/\_/ |_|_| |_|\__,_|\___/ \_/\_/ |___/
				#                                                                                            
				reallyShittyProblemSolver = 0
				if which in (0, 3):
					print "Its either a cube or a window!"
					height, width = simg.shape
					if simg[height/2,width/2] == 0:
						print "Its a Window!"
						which = 3
					else:
						print "Its a cube!"
						which = 0
						reallyShittyProblemSolver = 25
						if singleBlockHeight == False:
							singleBlockHeight = roundto25(height)
				


				print bestret
				print allImagesInfo[which] + "," + str(xyArr[counter][0]) + "," + str(xyArr[counter][1])

				if outputed == False:
					outputArr.append([allImagesInfo[which],filenameA[:-4],roundto25(xyArr[counter][0]+ reallyShittyProblemSolver),roundto25(xyArr[counter][1])])

				if highestY < roundto25(xyArr[counter][1]):
					highestY = roundto25(xyArr[counter][1])

				if lowestX > roundto25(xyArr[counter][0]):
					lowestX = roundto25(xyArr[counter][0])


				print "\n\n\n"
				#cv2.imshow('source image from camera',simg)
				#cv.MoveWindow('source image from camera', 200, 100) 
				#cv2.imshow('found match',images[which])
				#cv.MoveWindow('found match', 300, 100)
				#cv2.destroyAllWindows()
				counter += 1

	#    _____       _      _          __ _ _           
	#   |  __ \     | |    | |        / _(_) |          
	#   | |  | | ___| | ___| |_ ___  | |_ _| | ___  ___ 
	#   | |  | |/ _ \ |/ _ \ __/ _ \ |  _| | |/ _ \/ __|
	#   | |__| |  __/ |  __/ ||  __/ | | | | |  __/\__ \
	#   |_____/ \___|_|\___|\__\___| |_| |_|_|\___||___/
	#                               
	for root, dirs, files in os.walk(path+'/ros_blocks_basilisk/temp'):
	    for f in files:
	    	os.unlink(os.path.join(root, f))
	    for d in dirs:
	    	shutil.rmtree(os.path.join(root, d))



#             _ _               ____        _       ___           __ _   
#       /\   | (_)             |  _ \      | |     / / |         / _| |  
#      /  \  | |_  __ _ _ __   | |_) | ___ | |_   / /| |     ___| |_| |_ 
#     / /\ \ | | |/ _` | '_ \  |  _ < / _ \| __| / / | |    / _ \  _| __|
#    / ____ \| | | (_| | | | | | |_) | (_) | |_ / /  | |___|  __/ | | |_ 
#   /_/    \_\_|_|\__, |_| |_| |____/ \___/ \__/_/   |______\___|_|  \__|
#                  __/ |                                                 
#                 |___/                                                  

print outputArr
print "\n\n"
for i in range(len(outputArr)):
	outputArr[i][3] = 600 - (highestY - outputArr[i][3]) - 50 #This is shit Im so sorry!!!! 
	outputArr[i][2] = outputArr[i][2] - lowestX

print outputArr

print "singleBlockHeight: " + str(singleBlockHeight)


output = "<blocks>"
for i in range(len(outputArr)):
	output += "<block>"
	output += "<id>BlockID"+str(i)+"</id>"
	output += "<color>"+str(outputArr[i][1])+"</color>"
	output += "<type>"+str(outputArr[i][0])+"</type>"
	output += "<x>"+str(outputArr[i][2]/25)+"</x>"
	output += "<y>"+str(outputArr[i][3]/25)+"</y>"
	output += "</block>"

output += "</blocks>"

text_file = open(path+"/ros_blocks_basilisk/output.xml", "w")
text_file.write(output)
text_file.close()

text_file = open(path+"/ros_blocks_designer/basilisk.xml", "w")
text_file.write(output)
text_file.close()