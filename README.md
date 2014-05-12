ROS-Blocks
==========

![ros blocks!](http://calumk.com/dissertation/assets/img/jumbo_header.png "The ROS::Blocks Logo")

This is a repo for my BEng Design Engineering major project, ROS::Blocks

Full documentation of the project, including sample videos, and the PDF can be obtained from my website [Calumk.com](https://www.calumk.com/dissertation)


It is relesed under the MIT License.


#### Pre-requisits
* Tested on Ubuntu 12.04
* [ROS (Hydro)](http://wiki.ros.org/hydro)
* OpenCV - should be installed by default
* [SimpleCV](https://github.com/sightmachine/SimpleCV)
* [Baxter Research Robot (v1)](http://www.rethinkrobotics.com)



==========

To run the code, place the ros_blocks directory within your (Hydro) ROS workspace and execute the following commands. 


#### ROS:: Blocks 'Builder'
```
$ ros-run ros-blocks ros-blocks-builder.py —f blocks.xml
```


#### ROS:: Blocks 'Designer'
```
$ ros-run ros-blocks ros-blocks-designer.py —f blocks.xml
```

#### ROS:: Blocks 'Basilisk'
```
$ ros-run ros-blocks ros-blocks-basilisk.py
```