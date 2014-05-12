ROS-Blocks
==========

![ros blocks!](http://calumk.com/dissertation/assets/img/jumbo_header.png "The ROS::Blocks Logo")

This is a repo for my BEng Design Engineering project, ROS::Blocks

It is relesed under the MIT License.


### Pre-requisits
* Tested on Ubuntu 12.04
* ROS (Hydro)
* OpenCV - should be installed by default
* SimpleCV
* Baxter Research Robot (v1)



==========

To run the code, place the ros_blocks directory within your (Hydro) ROS workspace and execute the following commands. 


### ROS:: Blocks 'Builder'
```
$ ros-run ros-blocks ros-blocks-builder.py —f blocks.xml
```


### ROS:: Blocks 'Designer'
```
$ ros-run ros-blocks ros-blocks-designer.py —f blocks.xml
```

### ROS:: Blocks 'Basilisk'
```
$ ros-run ros-blocks ros-blocks-basilisk.py
```