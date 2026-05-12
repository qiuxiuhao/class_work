#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
贪心算法：北邮教室资源分配问题
问题类型：活动选择问题（区间调度问题）

场景描述：
北邮每天有大量的课程、讲座、社团活动需要使用教室。
每个活动有开始时间、结束时间和所需教室容量。
如何分配有限的教室资源，使得能够安排的活动数量最多？

算法设计：
- 贪心策略：按活动结束时间排序，优先选择结束时间早的活动
- 算法流程：
  1. 将所有活动按结束时间升序排序
  2. 为每个教室维护一个时间线
  3. 依次考虑每个活动，分配到第一个可用且容量满足的教室
- 时间复杂度：O(n log n)，主要是排序的复杂度
- 正确性：贪心选择性质 + 最优子结构
"""

import json
import time
from datetime import datetime
from typing import List, Dict, Tuple


class RoomAllocator:
    """教室资源分配器（贪心算法实现）"""

    def __init__(self, activities: List[Dict], classrooms: List[Dict]):
        """
        初始化教室分配器

        Args:
            activities: 活动列表
            classrooms: 教室列表
        """
        self.activities = activities
        self.classrooms = classrooms
        self.n_activities = len(activities)
        self.n_classrooms = len(classrooms)

        # 预处理：将时间字符串转换为datetime对象
        for activity in self.activities:
            activity["start_dt"] = datetime.strptime(
                activity["start_time"], "%Y-%m-%d %H:%M"
            )
            activity["end_dt"] = datetime.strptime(
                activity["end_time"], "%Y-%m-%d %H:%M"
            )

        # 用于记录算法执行过程
        self.execution_log = []

    def _has_time_conflict(self, activity: Dict, room_schedule: List[Dict]) -> bool:
        """
        检查活动是否与教室已有安排冲突

        Args:
            activity: 待检查的活动
            room_schedule: 教室的已有安排列表

        Returns:
            True表示有冲突，False表示无冲突
        """
        for scheduled in room_schedule:
            # 两个区间有重叠的条件：
            # activity.start < scheduled.end AND activity.end > scheduled.start
            if (activity["start_dt"] < scheduled["end_dt"] and
                activity["end_dt"] > scheduled["start_dt"]):
                return True
        return False

    def allocate_rooms(self, priority_weight: bool = True) -> Dict:
        """
        使用贪心算法分配教室

        Args:
            priority_weight: 是否考虑活动优先级（True时优先级高的活动优先）

        Returns:
            包含分配结果的字典
        """
        start_time = time.time()
        self.execution_log = []

        # 步骤1：按结束时间排序（贪心策略的核心）
        # 如果考虑优先级，则先按优先级排序，再按结束时间排序
        priority_map = {"high": 3, "medium": 2, "low": 1}

        if priority_weight:
            sorted_activities = sorted(
                self.activities,
                key=lambda x: (-priority_map.get(x["priority"], 1), x["end_dt"])
            )
            self.execution_log.append({
                "step": "排序",
                "description": "按优先级（降序）和结束时间（升序）排序活动"
            })
        else:
            sorted_activities = sorted(
                self.activities,
                key=lambda x: x["end_dt"]
            )
            self.execution_log.append({
                "step": "排序",
                "description": "按结束时间（升序）排序活动"
            })

        # 步骤2：初始化每个教室的时间表
        room_schedules = {room["room_id"]: [] for room in self.classrooms}

        # 步骤3：贪心选择
        allocated_activities = []
        rejected_activities = []

        for activity in sorted_activities:
            required_capacity = activity["required_capacity"]
            allocated = False

            self.execution_log.append({
                "step": "考虑活动",
                "activity": activity["activity_name"],
                "start": activity["start_time"],
                "end": activity["end_time"],
                "capacity": required_capacity,
                "priority": activity["priority"]
            })

            # 尝试为活动分配教室
            # 策略：选择容量满足且当前空闲的第一个教室
            for room in self.classrooms:
                # 检查容量是否满足
                if room["capacity"] < required_capacity:
                    continue

                # 检查时间是否冲突
                if not self._has_time_conflict(activity, room_schedules[room["room_id"]]):
                    # 分配成功
                    room_schedules[room["room_id"]].append(activity)
                    allocated_activities.append({
                        "activity": activity,
                        "room": room
                    })
                    allocated = True

                    self.execution_log.append({
                        "step": "分配成功",
                        "activity": activity["activity_name"],
                        "room": room["room_name"],
                        "capacity": room["capacity"]
                    })
                    break

            if not allocated:
                rejected_activities.append(activity)
                self.execution_log.append({
                    "step": "分配失败",
                    "activity": activity["activity_name"],
                    "reason": "无可用教室或容量不足"
                })

        end_time = time.time()
        execution_time = end_time - start_time

        # 构建结果
        result = {
            "algorithm": "贪心算法",
            "total_activities": self.n_activities,
            "allocated_count": len(allocated_activities),
            "rejected_count": len(rejected_activities),
            "allocation_rate": len(allocated_activities) / self.n_activities if self.n_activities > 0 else 0,
            "allocated_activities": allocated_activities,
            "rejected_activities": rejected_activities,
            "room_schedules": room_schedules,
            "execution_time": execution_time,
            "time_complexity": f"O(n log n) = O({self.n_activities} log {self.n_activities})",
            "space_complexity": f"O(n + m) = O({self.n_activities} + {self.n_classrooms})",
            "execution_log": self.execution_log
        }

        return result

    def get_room_utilization(self, result: Dict) -> Dict:
        """
        计算教室利用率

        Args:
            result: allocate_rooms返回的结果

        Returns:
            教室利用率统计
        """
        room_schedules = result["room_schedules"]
        utilization = {}

        for room in self.classrooms:
            room_id = room["room_id"]
            schedule = room_schedules[room_id]

            if not schedule:
                utilization[room["room_name"]] = {
                    "usage_count": 0,
                    "total_hours": 0,
                    "utilization_rate": 0
                }
                continue

            # 计算总使用时长
            total_hours = 0
            for activity in schedule:
                duration = (activity["end_dt"] - activity["start_dt"]).total_seconds() / 3600
                total_hours += duration

            utilization[room["room_name"]] = {
                "usage_count": len(schedule),
                "total_hours": total_hours,
                "capacity": room["capacity"],
                "activities": [a["activity_name"] for a in schedule]
            }

        return utilization

    def analyze_solution(self, result: Dict) -> Dict:
        """
        分析解决方案的质量

        Args:
            result: allocate_rooms返回的结果

        Returns:
            分析报告
        """
        allocated = result["allocated_activities"]
        rejected = result["rejected_activities"]

        # 统计活动类型分布
        allocated_types = {}
        rejected_types = {}

        for item in allocated:
            activity = item["activity"]
            act_type = activity["activity_type"]
            allocated_types[act_type] = allocated_types.get(act_type, 0) + 1

        for activity in rejected:
            act_type = activity["activity_type"]
            rejected_types[act_type] = rejected_types.get(act_type, 0) + 1

        # 统计优先级分布
        allocated_priorities = {}
        rejected_priorities = {}

        for item in allocated:
            priority = item["activity"]["priority"]
            allocated_priorities[priority] = allocated_priorities.get(priority, 0) + 1

        for activity in rejected:
            priority = activity["priority"]
            rejected_priorities[priority] = rejected_priorities.get(priority, 0) + 1

        # 计算教室利用率
        room_utilization = self.get_room_utilization(result)
        used_rooms = sum(1 for util in room_utilization.values() if util["usage_count"] > 0)

        analysis = {
            "allocation_rate": f"{result['allocation_rate']:.2%}",
            "allocated_count": result["allocated_count"],
            "rejected_count": result["rejected_count"],
            "allocated_by_type": allocated_types,
            "rejected_by_type": rejected_types,
            "allocated_by_priority": allocated_priorities,
            "rejected_by_priority": rejected_priorities,
            "used_rooms": used_rooms,
            "total_rooms": self.n_classrooms,
            "room_usage_rate": f"{used_rooms / self.n_classrooms:.2%}" if self.n_classrooms > 0 else "0%"
        }

        return analysis

    def get_timeline_visualization(self, result: Dict, room_name: str = None) -> Dict:
        """
        生成时间线可视化数据

        Args:
            result: allocate_rooms返回的结果
            room_name: 指定教室名称（可选，不指定则返回所有教室）

        Returns:
            时间线数据
        """
        room_schedules = result["room_schedules"]
        timeline = {}

        for room in self.classrooms:
            if room_name and room["room_name"] != room_name:
                continue

            room_id = room["room_id"]
            schedule = room_schedules[room_id]

            timeline[room["room_name"]] = {
                "capacity": room["capacity"],
                "events": [
                    {
                        "activity_name": activity["activity_name"],
                        "start": activity["start_time"],
                        "end": activity["end_time"],
                        "type": activity["activity_type"],
                        "priority": activity["priority"]
                    }
                    for activity in sorted(schedule, key=lambda x: x["start_dt"])
                ]
            }

        return timeline


def load_data_from_file(activities_path: str, classrooms_path: str) -> Tuple[List[Dict], List[Dict]]:
    """从JSON文件加载活动和教室数据"""
    with open(activities_path, 'r', encoding='utf-8') as f:
        activities = json.load(f)
    with open(classrooms_path, 'r', encoding='utf-8') as f:
        classrooms = json.load(f)
    return activities, classrooms


def main():
    """测试贪心算法"""
    print("="*60)
    print("贪心算法：北邮教室资源分配问题")
    print("="*60)

    # 加载数据
    activities, classrooms = load_data_from_file(
        '../data/activities.json',
        '../data/classrooms.json'
    )
    print(f"\n加载了 {len(activities)} 个活动")
    print(f"加载了 {len(classrooms)} 个教室")

    # 创建分配器
    allocator = RoomAllocator(activities, classrooms)

    # 测试场景1：不考虑优先级
    print("\n" + "-"*60)
    print("测试场景1：仅按结束时间贪心（不考虑优先级）")
    print("-"*60)
    result1 = allocator.allocate_rooms(priority_weight=False)

    print(f"分配成功：{result1['allocated_count']} 个活动")
    print(f"分配失败：{result1['rejected_count']} 个活动")
    print(f"分配率：{result1['allocation_rate']:.2%}")
    print(f"执行时间：{result1['execution_time']:.4f}秒")

    analysis1 = allocator.analyze_solution(result1)
    print(f"\n使用教室数：{analysis1['used_rooms']}/{analysis1['total_rooms']}")
    print(f"教室使用率：{analysis1['room_usage_rate']}")
    print("\n按类型分配统计：")
    for act_type, count in analysis1['allocated_by_type'].items():
        print(f"  - {act_type}: {count}")

    # 测试场景2：考虑优先级
    print("\n" + "-"*60)
    print("测试场景2：考虑优先级的贪心策略")
    print("-"*60)
    result2 = allocator.allocate_rooms(priority_weight=True)

    print(f"分配成功：{result2['allocated_count']} 个活动")
    print(f"分配失败：{result2['rejected_count']} 个活动")
    print(f"分配率：{result2['allocation_rate']:.2%}")
    print(f"执行时间：{result2['execution_time']:.4f}秒")

    analysis2 = allocator.analyze_solution(result2)
    print("\n按优先级分配统计：")
    for priority, count in analysis2['allocated_by_priority'].items():
        print(f"  - {priority}: {count}")

    print("\n" + "="*60)
    print("测试完成")
    print("="*60)


if __name__ == "__main__":
    main()
