#!/usr/bin/env python
import baxter_interface
import baxter_external_devices
import rospy
import ik_solver
from geometry_msgs.msg import (    
        Point,
        Quaternion,
)

import xml.etree.ElementTree as et
input_xml = open('blocks.xml','r')
tree = et.parse(input_xml)
root = tree.getroot()

resolution = 25;
unit = 50;
gridHeight = 12; #IN UNITS!!!!
containerHeight = unit*gridHeight;

realUnit = 0.035


#
# This is some pre-defined points
#
#

above =  Point(0.6059501636289412, 0.5326057625986961, 0.24199493679929163)
down =    Point(0.6590901227570745, 0.08788621770233086, -0.026315913387707293)
factoryOrigin =   Point(0.37284112809030295, 0.6110065725376852, -0.025201529789386102)

#
# This is the factory Settings
#
#




faceDownOld = Quaternion(0.1420037188751932, 0.9894283329110493,0.0087150932319107, 0.028116987897641357)
faceDown = Quaternion(0.00, 1.00,0.00, 0.00)
faceRight = Quaternion(1.00, 1.00,0.00, 0.00)


# THE THIRD ONE IS THE NUMBER OF BLOCKS

factory_pos = dict([('blockType_cube_h', [1,2.05 ,3 ,1]), 
        ('blockType_cuboid_h',   [0,1 ,3 ,1]),
        ('blockType_pillar_h',   [2,1 ,1 ,1]),
        ('blockType_bridge_h',   [0,2 ,2 ,1]),
        ('blockType_arch_h',     [3,1 ,0 ,2]),
        ('blockType_window_h',   [1,1 ,1 ,2])])

print(factory_pos.get('blockType_cube_h')[2])
def factory(block,xy):
    return factory_pos.get(block)[xy]*0.095;

#factory("blockType_arch_h",0)



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

blocks_data["blockType_cube_h"] =   make_block(1,1)
blocks_data["blockType_cube_v"] =   make_block(1,1)
blocks_data["blockType_cuboid_h"] = make_block(1,2)
blocks_data["blockType_cuboid_v"] = make_block(2,1)
blocks_data["blockType_pillar_h"] = make_block(1,4)
blocks_data["blockType_pillar_v"] = make_block(4,1)

blocks_data["blockType_bridge_h"] = make_block(1,2)
blocks_data["blockType_bridge_v"] = make_block(2,1)
blocks_data["blockType_arch_h"] =   make_block(2,4)
blocks_data["blockType_arch_v"] =   make_block(2,4)
blocks_data["blockType_window_h"] = make_block(2,2)
blocks_data["blockType_window_v"] = make_block(2,2)

places = []
blockOrder = []
























def moveRel(x,y,z):
    pose = left.endpoint_pose()
    print "current pose: ", pose
    curX = pose["position"].x
    curY = pose["position"].y
    curZ = pose["position"].z
    newX = curX + x
    newY = curY + y
    newZ = curZ + z
    loc = Point(newX,newY,newZ)
    print "loc: ", loc    
    print "orient: ", faceDown
    limb_joints = ik_solver.ik_solve('left', loc, faceDown)
    prev = loc
    if limb_joints != -1:
            print "limb_joints: ", limb_joints
            print "moving arm to limb_joints joints"
            left.move_to_joint_positions(limb_joints)

def moveRel_AbsOr(x,y,z, qx,qy,qz,qw):
    pose = left.endpoint_pose()
    print "current pose: ", pose
    curX = pose["position"].x
    curY = pose["position"].y
    curZ = pose["position"].z

    newX = curX + x
    newY = curY + y
    newZ = curZ + z
    ori = Quaternion(qx,qy,qz,qw)
    loc = Point(newX,newY,newZ)
    print "loc: ", loc    
    print "orient: ", ori
    limb_joints = ik_solver.ik_solve('left', loc, ori)
    prev = loc
    if limb_joints != -1:
            print "limb_joints: ", limb_joints
            print "moving arm to limb_joints joints"
            left.move_to_joint_positions(limb_joints)


def moveTo(goal,orien=faceDown):
    loc = goal
    ori = orien
    print "loc: ", loc    
    print "orient: ", ori
    limb_joints = ik_solver.ik_solve('left', loc, ori)
    prev = loc
    if limb_joints != -1:
            left.move_to_joint_positions(limb_joints)


def moveRelPreDef(point,rx,ry,rz,ori=faceDown):
    moveTo(Point(point.x+rx,point.y+ry,point.z+rz),ori) 


def moveFactory(blockType,vertOff=0.0):
    
    if factory_pos.get(blockType)[2] == 0:
        print("No More of thoes blocks left!! sorry :( ")

    blockHeight = (factory_pos.get(blockType)[3])*3.5
    blockHeight = blockHeight - 3.5
    print(blockHeight)
    vertOff = vertOff + ((((factory_pos.get(blockType)[2]-1)*3.5)+blockHeight)/100)
    print(vertOff)  
    moveRelPreDef(factoryOrigin, factory(blockType,0), -factory(blockType,1) , vertOff ,   faceRight)
    

def takeBlock(blockType):
    factory_pos.get(blockType)[2] = factory_pos.get(blockType)[2]-1



rospy.init_node('move_left_hand')
rs = baxter_interface.RobotEnable()
rs.enable()

left = baxter_interface.Limb('left')
leftGripper = baxter_interface.Gripper('left')
pose = left.endpoint_pose()
b = True
pos = pose.popitem()
orient = pose.popitem()
prev = pos[1]

left.set_joint_position_speed(1.0)
leftGripper.set_velocity(10)
print "-----------------------------------"
pose = left.endpoint_pose()
print "current pose: ", pose
s = raw_input("Press r to run ... ")
if s == 'r':

    for x in range(0, len(root)):
        print(root[x][0].text)
        print(root[x][1].text)
        print(root[x][2].text)
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
        print("CALUM PAY ATTENTION!!!!");
        print("CALUM PAY ATTENTION!!!!");
        print("CALUM PAY ATTENTION!!!!");
        print(places[x][1]);
        print("CALUM PAY ATTENTION!!!!");

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