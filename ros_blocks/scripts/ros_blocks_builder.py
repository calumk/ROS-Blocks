#!/usr/bin/env python

#    ____        _ _     _           
#   |  _ \      (_| |   | |          
#   | |_) |_   _ _| | __| | ___ _ __ 
#   |  _ <| | | | | |/ _` |/ _ | '__|
#   | |_) | |_| | | | (_| |  __| |   
#   |____/ \__,_|_|_|\__,_|\___|_|   
#                                    
#                                                                                                                        

import baxter_interface
import baxter_external_devices
import rospy
import ik_solver
from geometry_msgs.msg import (    
        Point,
        Quaternion,
)

import xml.etree.ElementTree as et

# Open the xml file
input_xml = open('blocks.xml','r')
tree = et.parse(input_xml)
root = tree.getroot()

# Define the pixel resolution of the grid, 
# All these settings could be hard-coded but are here for readability. They dont change.
resolution  =   25;
unit        =   50;
gridHeight  =   12; # IN UNITS!!!!
containerHeight = unit*gridHeight; #makes 600px

#Baxter measures real word units in SI (meters), Thus we must represent the blocks in SI units.
realUnit = 0.035 # = 35mm (the height of one block)


# These are some pre-defined points
above           =   Point(0.6059501636289412, 0.5326057625986961, 0.24199493679929163)
down            =   Point(0.6590901227570745, 0.08788621770233086, -0.026315913387707293)
factoryOrigin   =   Point(0.37284112809030295, 0.6110065725376852, -0.025201529789386102)

# These are some pre-defined orientations
faceDownOld     =   Quaternion(0.1420037188751932, 0.9894283329110493,0.0087150932319107, 0.028116987897641357)
faceDown        =   Quaternion(0.00, 1.00,0.00, 0.00)
faceRight       =   Quaternion(1.00, 1.00,0.00, 0.00)



# These are the factory Settings
# [X position in factory  ,  Y position in factory  ,  number of blocks  ,  block height (in units)]
factory_pos = dict([
        ('blockType_cube_h',     [1 ,2.05 ,3 ,1]), 
        ('blockType_cuboid_h',   [0 ,1    ,3 ,1]),
        ('blockType_pillar_h',   [2 ,1    ,1 ,1]),
        ('blockType_bridge_h',   [0 ,2    ,2 ,1]),
        ('blockType_arch_h',     [3 ,1    ,0 ,2]),
        ('blockType_window_h',   [1 ,1    ,1 ,2])
        ])

def factory(block,xy):
    return factory_pos.get(block)[xy]*0.095;





# The following class and functions are used to "generate" the block objects that the script passes around.
blocks_data = {}
class blockType(object):
        x = 0
        y = 0
        # The class "constructor" - It's actually an initializer 
        def __init__(self, x, y):
                self.x = y
                self.y = x

def make_block(x, y):
        block = blockType(x*unit, y*unit)
        return block

blocks_data["blockType_cube_h"]   = make_block(1,1)
blocks_data["blockType_cube_v"]   = make_block(1,1)
blocks_data["blockType_cuboid_h"] = make_block(1,2)
blocks_data["blockType_cuboid_v"] = make_block(2,1)
blocks_data["blockType_pillar_h"] = make_block(1,4)
blocks_data["blockType_pillar_v"] = make_block(4,1)

blocks_data["blockType_bridge_h"] = make_block(1,2)
blocks_data["blockType_bridge_v"] = make_block(2,1)
blocks_data["blockType_arch_h"]   = make_block(2,4)
blocks_data["blockType_arch_v"]   = make_block(2,4)
blocks_data["blockType_window_h"] = make_block(2,2)
blocks_data["blockType_window_v"] = make_block(2,2)

# two blank arrays are created 
places = []
blockOrder = []















#    __  __                  ______                _   _                 
#   |  \/  |                |  ____|              | | (_)                
#   | \  / | _____   _____  | |__ _   _ _ __   ___| |_ _  ___  _ __  ___ 
#   | |\/| |/ _ \ \ / / _ \ |  __| | | | '_ \ / __| __| |/ _ \| '_ \/ __|
#   | |  | | (_) \ V |  __/ | |  | |_| | | | | (__| |_| | (_) | | | \__ \
#   |_|  |_|\___/ \_/ \___| |_|   \__,_|_| |_|\___|\__|_|\___/|_| |_|___/
#                                                                        
#                                                                                                                    


def moveRel(x,y,z):
    pose = left.endpoint_pose()
    print "current pose: ", pose
    # get the current position
    curX = pose["position"].x
    curY = pose["position"].y
    curZ = pose["position"].z
    # set the new position
    newX = curX + x
    newY = curY + y
    newZ = curZ + z
    # generate the location point from the new postions
    loc = Point(newX,newY,newZ)
    print "loc: ", loc    
    print "orient: ", faceDown
    # solve the IK to the new position
    limb_joints = ik_solver.ik_solve('left', loc, faceDown)
    prev = loc
    # IF the IK is ok, then go to the next position (it will stall and print an error if the IK is not needed so not "Catch" is needed)
    if limb_joints != -1:
            print "limb_joints: ", limb_joints
            print "moving arm to limb_joints joints"
            left.move_to_joint_positions(limb_joints)

def moveRel_AbsOr(x,y,z, qx,qy,qz,qw):
    pose = left.endpoint_pose()
    print "current pose: ", pose
    # get the current position
    curX = pose["position"].x
    curY = pose["position"].y
    curZ = pose["position"].z
    # set the new position
    newX = curX + x
    newY = curY + y
    newZ = curZ + z
    # set the new orientation / location
    ori = Quaternion(qx,qy,qz,qw)
    loc = Point(newX,newY,newZ)
    print "loc: ", loc    
    print "orient: ", ori
    # solve the IK to the new position
    limb_joints = ik_solver.ik_solve('left', loc, ori)
    prev = loc
    # IF the IK is ok, then go to the next position (it will stall and print an error if the IK is not needed so not "Catch" is needed)
    if limb_joints != -1:
            print "limb_joints: ", limb_joints
            print "moving arm to limb_joints joints"
            left.move_to_joint_positions(limb_joints)


def moveTo(goal,orien=faceDown):
    # move directly to a goal, (not relative to anything)
    loc = goal
    ori = orien
    print "loc: ", loc    
    print "orient: ", ori
    # solve the IK to the new position
    limb_joints = ik_solver.ik_solve('left', loc, ori)
    prev = loc
    # IF the IK is ok, then go to the next position (it will stall and print an error if the IK is not needed so not "Catch" is needed)
    if limb_joints != -1:
            left.move_to_joint_positions(limb_joints)


def moveRelPreDef(point,rx,ry,rz,ori=faceDown):
    #move relative to a point, without actually being there first
    moveTo(Point(point.x+rx,point.y+ry,point.z+rz),ori) 


def moveFactory(blockType,vertOff=0.0):
    #a specific movement function that move to a point above a selected blocktype in the factory
    if factory_pos.get(blockType)[2] == 0:
        print("No More of thoes blocks left!! sorry :( ")
    blockHeight = (factory_pos.get(blockType)[3])*3.5
    blockHeight = blockHeight - 3.5
    print(blockHeight)
    vertOff = vertOff + ((((factory_pos.get(blockType)[2]-1)*3.5)+blockHeight)/100)
    print(vertOff)  
    moveRelPreDef(factoryOrigin, factory(blockType,0), -factory(blockType,1) , vertOff ,   faceRight)
    

def takeBlock(blockType):
    # Not a movement function, this decrements the value that stores how many of each block is avaliable. 
    factory_pos.get(blockType)[2] = factory_pos.get(blockType)[2]-1








#    __  __       _         _____                                     
#   |  \/  |     (_)       |  __ \                                    
#   | \  / | __ _ _ _ __   | |__) _ __ ___   __ _ _ __ __ _ _ __ ___  
#   | |\/| |/ _` | | '_ \  |  ___| '__/ _ \ / _` | '__/ _` | '_ ` _ \ 
#   | |  | | (_| | | | | | | |   | | | (_) | (_| | | | (_| | | | | | |
#   |_|  |_|\__,_|_|_| |_| |_|   |_|  \___/ \__, |_|  \__,_|_| |_| |_|
#                                            __/ |                    
#                                           |___/                     


# we are talking to baxters LEFT hand by default. You can change this here by switching the commented lines...
rs = baxter_interface.RobotEnable()
rs.enable()

#rospy.init_node('move_left_hand')
rospy.init_node('move_left_hand')

# left = baxter_interface.Limb('right')
left = baxter_interface.Limb('left')

#leftGripper = baxter_interface.Gripper('right')
leftGripper = baxter_interface.Gripper('left')


pose = left.endpoint_pose()
b = True
pos = pose.popitem()
orient = pose.popitem()
prev = pos[1]

# set the robot speeds
left.set_joint_position_speed(1.0)
leftGripper.set_velocity(10)


# There is (unapologetically) A lot of printing in this next section... It's usefull for debugging, :D
print "-----------------------------------"
pose = left.endpoint_pose()
print "current pose: ", pose

# Wait for the user to say "yes build" by pressing r
s = raw_input("Enter r to run ... ")
if s == 'r':
    for x in range(0, len(root)):
        # for each block in the xml file..... 
        print(root[x][0].text)
        print(root[x][1].text)
        print(root[x][2].text)
        # make a block class object thigny...
        currentBlock = make_block(int(root[x][3].text) ,int(root[x][4].text))
        tl_x = int(root[x][3].text)*resolution
        tl_y = int(root[x][4].text)*resolution
        print("TL.x: "+ str(tl_x))
        print("TL.y: "+ str(tl_y))
        print("bd : "+ str(blocks_data[root[x][2].text].x/2))
        pl_x = float(float(tl_x)/float(unit))
        pl_y = (containerHeight - tl_y)/unit
        print("PL.x: "+ str(pl_x))
        print("PL.y: "+ str(pl_y))
        
        print("WIDE: "+ str( blocks_data[root[x][2].text].x))
        print("TALL: "+ str( blocks_data[root[x][2].text].y))
        wide = blocks_data[root[x][2].text].x/unit
        tall = blocks_data[root[x][2].text].y/unit

        print("wide1 : "+ str(wide))
        print(float(wide)/2)
        
        half_width = ((float(wide)/2)*realUnit)
        print(half_width)
        print("xPOS1 : " + str((pl_x*realUnit)))
        print("xPOS2 : " + str((pl_x*realUnit)+((float(wide)/2)*realUnit)))

        places.append([(pl_x*realUnit) + half_width , pl_y*realUnit])
        blockOrder.append(root[x][2].text)
        print(":::::::::::::")

    print(places)
    moveRel(0,0,0.2)
    moveRelPreDef(factoryOrigin,0,0,0.3,faceRight)
    moveTo(factoryOrigin,faceRight) 
    leftGripper.open()
    s = raw_input("Was Origin Correct? IF NOT, move to the correct position, and then press 'r' to recalibrate")
    if s == 'r':
        pose = left.endpoint_pose()
        print "current pose: ", pose
        curX = pose["position"].x
        curY = pose["position"].y
        curZ = pose["position"].z
        global factoryOrigin
        factoryOrigin = Point(curX,curY,curZ)
        print(factoryOrigin)
        moveTo(factoryOrigin,faceRight)
        s = raw_input("Do you want to quit now? 'y' to quit")
        if s == 'y':
            exit();

    moveRelPreDef(factoryOrigin,0,0,0.3,faceRight)  
    for x in range(0, len(places)):
        print places[x]
        print blockOrder[x]
        moveFactory(blockOrder[x],0.1)
    
        moveFactory(blockOrder[x])
        leftGripper.close()
        
        takeBlock(blockOrder[x])
        rospy.sleep(3)
        
        moveFactory(blockOrder[x],0.2)
        print("Important Value.... Should probably think of a better comment than this...");
        print(places[x][1]);
        

        moveRelPreDef(down,0,-places[x][0],places[x][1]+0.100,faceRight)
        moveRelPreDef(down,0,-places[x][0],places[x][1]-0.035,faceRight)  
        print("IT SHOULD BE 3.5 in box above. dont change. IF you need to change it, the robot is not correctly callibrated")
        leftGripper.open()
        rospy.sleep(1)
        moveRelPreDef(down,0,-places[x][0],places[x][1]+0.1,faceRight)

        leftGripper.open()
        moveRelPreDef(factoryOrigin,0,0,0.3,faceRight)
        rospy.sleep(1)

    s = raw_input("Press 'f' to return to factoryOrigin")
    if s == 'f':
        moveTo(above)
        moveTo(factoryOrigin,faceRight)




        