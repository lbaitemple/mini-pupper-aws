#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Pose
from std_msgs.msg import String
from .math_operations import *
import math, sys
import time

class DanceDemo(Node):
    def __init__(self):
        super().__init__('dance_demo')
        self.r = self.create_rate(100)
        self.roll = 0
        self.pitch = 0
        self.yaw = 0
        self.declare_parameter('dance_config_path', rclpy.Parameter.Type.STRING) 

        self.dance_config_path = self.get_parameter('dance_config_path').get_parameter_value().string_value
        self.get_logger().info(self.dance_config_path)
        self.get_logger().info(str(self.dance_config_path))
        self.dance_config_name = ' '
        self.commands = []
        self.ready_to_dance = 0
        self.dance_config_sub = self.create_subscription(String, '/dance_config', self.dance_config_callback, 10)
        self.velocity_publisher = self.create_publisher(Twist, 'cmd_vel', 100)
        #self.pose_publisher = self.create_publisher(Pose, 'target_body_pose', 100)
        self.pose_publisher = self.create_publisher(Pose, 'reference_body_pose', 100)

    def dance_config_callback(self, msg):
        self.dance_config_name = msg.data
        self.dance_config = __import__(self.dance_config_name)
        self.commands = self.dance_config.dance_commands
        self.get_logger().info('executing command: .... ' )
        self.commands.insert(0, 'stop')
        self.commands.append('stop')
        self.ready_to_dance = 1
        self.dance()

    def dance(self):
 
        while (self.dance_config_name == ' ' or not self.ready_to_dance) and rclpy.ok():
            self.r.sleep()

        for command in self.commands:
            velocity_cmd = Twist()
            pose_cmd = Pose()
            self.roll = 0
            self.pitch = 0
            self.yaw = 0



            if rclpy.ok():
                if command == 'move_forward':
                    self.get_logger().info('executing command: ' + str(command))
                    velocity_cmd.linear.x = 0.5
                    self.velocity_publisher.publish(velocity_cmd)
                    time.sleep(self.dance_config.interval_time)

                elif command == 'move_backward':
                    self.get_logger().info('executing command: ' + str(command))
                    velocity_cmd.linear.x = -0.5
                    self.velocity_publisher.publish(velocity_cmd)
                    time.sleep(self.dance_config.interval_time)
                elif(command == 'move_left' ):
                    velocity_cmd.linear.y = 0.5
                    self.velocity_publisher.publish(velocity_cmd)
                    self.get_logger().info('Publishing: "%s"' % command)
                    time.sleep(self.dance_config.interval_time)

                elif(command == 'move_right' ):
                    velocity_cmd.linear.y = -0.5
                    self.velocity_publisher.publish(velocity_cmd)
                    self.get_logger().info('Publishing: "%s"' % command)
                    time.sleep(self.dance_config.interval_time)
                    
                elif(command == 'turn_left' ):
                    velocity_cmd.angular.z = 1.0
                    self.velocity_publisher.publish(velocity_cmd)
                    self.get_logger().info('Publishing: "%s"' % command)
                    time.sleep(self.dance_config.interval_time)
 
                elif(command == 'turn_right' ):
                    velocity_cmd.angular.z = -1.0
                    self.velocity_publisher.publish(velocity_cmd)
                    self.get_logger().info('Publishing: "%s"' % command)
                    time.sleep(self.dance_config.interval_time)
        
                elif(command == 'look_up' ):
                    #pose_cmd.orientation.x, pose_cmd.orientation.y, pose_cmd.orientation.z, pose_cmd.orientation.w = quaternion_from_euler(0.0, -0.3, 0.0)
                    pose_cmd.orientation.x, pose_cmd.orientation.y, pose_cmd.orientation.z, pose_cmd.orientation.w = quaternion_from_euler(0.0, -0.3, 0.0)
                    self.pose_publisher.publish(pose_cmd)
                    self.get_logger().info('Publishing: "%s"' % command)
                    time.sleep(self.dance_config.interval_time)
        
                elif(command == 'look_down' ):
                   # pose_cmd.orientation.x, pose_cmd.orientation.y, pose_cmd.orientation.z, pose_cmd.orientation.w = quaternion_from_euler(0.0, 0.3, 0.0)
                    pose_cmd.orientation.x, pose_cmd.orientation.y, pose_cmd.orientation.z, pose_cmd.orientation.w = quaternion_from_euler(0.0, 0.3, 0.0)
                    self.pose_publisher.publish(pose_cmd)
                    self.get_logger().info('Publishing: "%s"' % command)
                    time.sleep(self.dance_config.interval_time)
        
                elif(command == 'look_left' ):
#                    pose_cmd.orientation.x, pose_cmd.orientation.y, pose_cmd.orientation.z, pose_cmd.orientation.w = quaternion_from_euler(0.0, 0.0, 0.3)
                    pose_cmd.orientation.x, pose_cmd.orientation.y, pose_cmd.orientation.z, pose_cmd.orientation.w = quaternion_from_euler(0.0, 0.0, 0.3)
                    self.pose_publisher.publish(pose_cmd)
                    self.get_logger().info('Publishing: "%s"' % command)
                    time.sleep(self.dance_config.interval_time)
        
                elif(command == 'look_right' ):
#                    pose_cmd.orientation.x, pose_cmd.orientation.y, pose_cmd.orientation.z, pose_cmd.orientation.w = quaternion_from_euler(0.0, 0.0, -0.3)
                    pose_cmd.orientation.x, pose_cmd.orientation.y, pose_cmd.orientation.z, pose_cmd.orientation.w = quaternion_from_euler(0.0, 0.0, -0.3)
                    self.pose_publisher.publish(pose_cmd)
                    self.get_logger().info('Publishing: "%s"' % command)
                    time.sleep(self.dance_config.interval_time)
        
                elif(command == 'look_middle' ):
#                    pose_cmd.orientation.x, pose_cmd.orientation.y, pose_cmd.orientation.z, pose_cmd.orientation.w = quaternion_from_euler(0.0, 0.0, 0.0)
                    pose_cmd.orientation.x, pose_cmd.orientation.y, pose_cmd.orientation.z, pose_cmd.orientation.w = quaternion_from_euler(0.0, 0.0, 0.0)
                    self.pose_publisher.publish(pose_cmd)
                    self.get_logger().info('Publishing: "%s"' % command)
                    time.sleep(self.dance_config.interval_time)
        
                elif(command == 'stay' ):
#                    time.sleep(self.interval) # do nothing
                    time.sleep(self.dance_config.interval_time)
                        
                elif(command == 'stop' ):
                    velocity_cmd.linear.x = 0.0
                    velocity_cmd.linear.y = 0.0
                    velocity_cmd.linear.z = 0.0
                    self.velocity_publisher.publish(velocity_cmd)
                    pose_cmd.orientation.x, pose_cmd.orientation.y, pose_cmd.orientation.z, pose_cmd.orientation.w = quaternion_from_euler(0.0, 0.0, 0.0)
                    self.pose_publisher.publish(pose_cmd)
                    self.get_logger().info('Publishing: "%s"' % command)
                    time.sleep(self.dance_config.interval_time)
 
                else:
                    self.get_logger().warn('wrong command: ' + str(command))

                
                velocity_cmd = Twist()
                self.velocity_publisher.publish(velocity_cmd)
                time.sleep(self.dance_config.interval_time)

def main(args=None):
    rclpy.init(args=args)
    lets_dance = DanceDemo()
    rclpy.spin(lets_dance)
    lets_dance.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
