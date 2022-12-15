// Copyright 2022 Andrew Symington
//
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
//
// The above copyright notice and this permission notice shall be included in
// all copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
// THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
// THE SOFTWARE.

#ifndef LIBSURVIVE_ROS2__COMPONENT_HPP_
#define LIBSURVIVE_ROS2__COMPONENT_HPP_

// STL libraries
#include <mutex>
#include <cstdint>
#include <thread>
#include <vector>

// ROS2 core
#include <rclcpp/rclcpp.hpp>

// ROS2 libraries
#include <tf2_ros/transform_broadcaster.h>
#include <tf2_ros/static_transform_broadcaster.h>

// ROS2 messages
#include <diagnostic_msgs/msg/key_value.hpp>
#include <sensor_msgs/msg/joy.hpp>
#include <sensor_msgs/msg/imu.hpp>
#include <geometry_msgs/msg/point_stamped.hpp>
#include <geometry_msgs/msg/pose_stamped.hpp>

// Libsurvive libraries
extern "C" {
#define SURVIVE_ENABLE_FULL_API
#include <os_generic.h>
#include <libsurvive/survive.h>
#include <libsurvive/survive_api.h>
}

namespace libsurvive_ros2 {

class Component : public rclcpp::Node {
public:
  explicit Component(const rclcpp::NodeOptions & options);
  virtual ~Component();
  rclcpp::Time get_ros_time(FLT timecode);
  void publish_imu(const sensor_msgs::msg::Imu& msg);
private:
  void work();
  SurviveSimpleContext *actx_;
  std::unique_ptr<tf2_ros::TransformBroadcaster> tf_broadcaster_;
  std::shared_ptr<tf2_ros::StaticTransformBroadcaster> tf_static_broadcaster_;
  rclcpp::Publisher<sensor_msgs::msg::Joy>::SharedPtr joy_publisher_;
  rclcpp::Publisher<sensor_msgs::msg::Imu>::SharedPtr imu_publisher_;
  rclcpp::Publisher<diagnostic_msgs::msg::KeyValue>::SharedPtr cfg_publisher_;
  std::thread worker_thread_;
  rclcpp::Time ros_time_;
  rclcpp::Time last_base_station_update_;
  std::string tracking_frame_;
  double lighthouse_rate_;
};

}  // namespace libsurvive_ros2

#endif  // LIBSURVIVE_ROS2__COMPONENT_HPP_