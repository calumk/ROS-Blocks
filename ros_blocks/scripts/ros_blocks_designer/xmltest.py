import xml.etree.ElementTree as et
input_xml = open('blocks2.xml','r')
tree = et.parse(input_xml)
root = tree.getroot()

resolution = 25;
unit = 50;
gridHeight = 12; #IN UNITS!!!!
containerHeight = unit*gridHeight;

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
blocks_data["blockType_cube_v"] =   make_block(1,2)
blocks_data["blockType_cuboid_h"] = make_block(2,1)
blocks_data["blockType_cuboid_v"] = make_block(1,2)
blocks_data["blockType_pillar_h"] = make_block(1,4)
blocks_data["blockType_pillar_v"] = make_block(4,1)

blocks_data["blockType_bridge_h"] = make_block(1,2)
blocks_data["blockType_bridge_v"] = make_block(2,1)
blocks_data["blockType_arch_h"] =   make_block(2,4)
blocks_data["blockType_arch_v"] =   make_block(2,4)
blocks_data["blockType_window_h"] = make_block(2,2)
blocks_data["blockType_window_v"] = make_block(2,2)

places = []

for x in range(0, len(root)):
    print(root[x][0].text)
    print(root[x][1].text)
    print(root[x][2].text)
    currentBlock = make_block(int(root[x][3].text) ,int(root[x][4].text))
    tl_x = int(root[x][3].text)*resolution
    tl_y = int(root[x][4].text)*resolution
    print("TL.x: "+ str(tl_x))
    print("TL.y: "+ str(tl_y))

    pl_x = (tl_x + (blocks_data[root[x][2].text].x/2))/unit
    pl_y = (containerHeight - tl_y)/unit
    print("PL.x: "+ str(pl_x))
    print("PL.y: "+ str(pl_y))
    places.append([pl_x, pl_y])
    print("WIDE: "+ str( blocks_data[root[x][2].text].x))
    print("TALL: "+ str( blocks_data[root[x][2].text].y))
    print(":::::::::::::")
    
for x in range(0, len(places)):
    print places[x]
    #moveRelBottom(0,places[x][0],places[x][1])
    print "moveRelBottom(0,"+str(places[x][0])+","+str(places[x][1])+")"
