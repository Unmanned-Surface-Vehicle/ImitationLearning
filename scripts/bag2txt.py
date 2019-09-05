#!/usr/bin/env python

import rosbag
import argparse

parser = argparse.ArgumentParser(description='Extract vehicle data from ROS bag file, using python\'s rosbag API')
parser.add_argument('bag', action='store', type=str, help='Bag filename')
parser.add_argument('--output', type=str, default='out.txt', help='Output file name (default is out.txt)')
args = parser.parse_args()


if __name__ == "__main__":
    with open(args.output, 'w') as outfile:
        with rosbag.Bag(args.bag, 'r') as bag:
	    msgOdom = None
	    msgCostmap = None
	    msgPlan = None
	    msgStatus = None
	    msgVel = None
	    msgGoal = None
            for topic, msg, t in bag.read_messages(topics=['/move_base/local_costmap/costmap', '/move_base/DWAPlannerROS/global_plan', '/odom', '/move_base/goal', '/mobile_base/commands/velocity', '/move_base/status', '/move_base/goal']):
		if (msg._type == "nav_msgs/Odometry"):
			msgOdom = msg;
		elif (msg._type == "nav_msgs/Path"):
			msgPlan = msg;
		elif (msg._type == "nav_msgs/OccupancyGrid"):
			msgCostmap = msg;
		elif (msg._type == "actionlib_msgs/GoalStatusArray"):
			msgStatus = msg;
		elif (msg._type == "move_base_msgs/MoveBaseActionGoal"):
			msgGoal = msg;
		elif (msg._type == "geometry_msgs/Twist"):
			msgVel = msg;
			if (msgOdom != None and msgCostmap != None and msgPlan != None and msgStatus != None and msgGoal != None):
				outfile.write("%f %f %f %f %f %f %f %f %f %f %d %f %f %f %f %f %f %f %f %f %f %f %f %f %s\n" % (
				msgOdom.pose.pose.position.x, msgOdom.pose.pose.position.y, msgOdom.pose.pose.position.z, 
				msgGoal.goal.target_pose.pose.position.x, msgGoal.goal.target_pose.pose.position.y, msgGoal.goal.target_pose.pose.position.z, msgGoal.goal.target_pose.pose.orientation.x, msgGoal.goal.target_pose.pose.orientation.y, msgGoal.goal.target_pose.pose.orientation.z, msgGoal.goal.target_pose.pose.orientation.w,
				msgStatus.status_list[0].status,
				msgVel.linear.x, msgVel.linear.y, msgVel.linear.z, msgVel.angular.x, msgVel.angular.y, msgVel.angular.z,
				msgPlan.poses[0].pose.position.x, msgPlan.poses[0].pose.position.y, msgPlan.poses[0].pose.position.z, msgPlan.poses[0].pose.orientation.x, msgPlan.poses[0].pose.orientation.y, msgPlan.poses[0].pose.orientation.z, msgPlan.poses[0].pose.orientation.w,
				msgCostmap.data))
		else:
			print msg._type

#                outfile.write("%d %f %f %f\n" % (msg.status.status, msg.latitude, msg.longitude, msg.altitude))

