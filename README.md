# pipeline
Minor Mobile Robotics - Robot Architecture ROS2 assingment

build:
  colcon build

run:
  terminal 1:
    . install/setup.bash
    ros2 run py_pubsub talker
    
  terminal 2:
    . install/setup.bash
    ros2 run py_srvcli client_subscriber
    
  terminal  3:
    . install/setup.bash
    ros2 run py_srvcli service
