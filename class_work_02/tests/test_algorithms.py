#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
算法单元测试
测试动态规划和贪心算法的正确性
"""

import unittest
import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from algorithms.dynamic_programming import CourseSelector
from algorithms.greedy import RoomAllocator


class TestDynamicProgramming(unittest.TestCase):
    """测试动态规划算法"""

    def setUp(self):
        """准备测试数据"""
        self.test_courses = [
            {
                "course_id": "CS101",
                "course_name": "数据结构",
                "credits": 4,
                "teacher": "张教授",
                "time_slots": [{"day": "Monday", "period": "1-2"}],
                "classroom": "教三301",
                "capacity": 80
            },
            {
                "course_id": "CS102",
                "course_name": "计算机网络",
                "credits": 3,
                "teacher": "李教授",
                "time_slots": [{"day": "Monday", "period": "1-2"}],  # 与CS101冲突
                "classroom": "教三302",
                "capacity": 80
            },
            {
                "course_id": "CS103",
                "course_name": "操作系统",
                "credits": 4,
                "teacher": "王教授",
                "time_slots": [{"day": "Tuesday", "period": "3-4"}],
                "classroom": "教三303",
                "capacity": 80
            },
            {
                "course_id": "CS104",
                "course_name": "数据库原理",
                "credits": 3,
                "teacher": "赵教授",
                "time_slots": [{"day": "Wednesday", "period": "5-6"}],
                "classroom": "教三304",
                "capacity": 80
            }
        ]

    def test_no_conflict_selection(self):
        """测试无冲突的课程选择"""
        # 只选择无冲突的课程
        courses = [self.test_courses[0], self.test_courses[2], self.test_courses[3]]
        selector = CourseSelector(courses)
        result = selector.select_courses()

        # 应该选择所有3门课程
        self.assertEqual(result["num_courses"], 3)
        self.assertEqual(result["total_credits"], 11)  # 4 + 4 + 3

    def test_conflict_resolution(self):
        """测试时间冲突的处理"""
        # CS101和CS102时间冲突，应该选择学分更高的CS101
        selector = CourseSelector(self.test_courses)
        result = selector.select_courses()

        # 应该选择CS101(4学分)而不是CS102(3学分)
        selected_ids = [c["course_id"] for c in result["selected_courses"]]
        self.assertIn("CS101", selected_ids)
        self.assertNotIn("CS102", selected_ids)

    def test_max_credits(self):
        """测试最大学分优化"""
        selector = CourseSelector(self.test_courses)
        result = selector.select_courses()

        # 最优解应该是CS101(4) + CS103(4) + CS104(3) = 11学分
        self.assertEqual(result["total_credits"], 11)

    def test_min_credits_constraint(self):
        """测试最低学分约束"""
        selector = CourseSelector(self.test_courses)
        result = selector.select_courses(min_credits=10)

        # 应该满足最低学分要求
        self.assertGreaterEqual(result["total_credits"], 10)

    def test_empty_courses(self):
        """测试空课程列表"""
        selector = CourseSelector([])
        result = selector.select_courses()

        self.assertEqual(result["num_courses"], 0)
        self.assertEqual(result["total_credits"], 0)

    def test_schedule_visualization(self):
        """测试课程表可视化"""
        selector = CourseSelector(self.test_courses)
        result = selector.select_courses()
        schedule = selector.get_schedule_visualization(result["selected_courses"])

        # 检查schedule结构
        self.assertIn("Monday", schedule)
        self.assertIn("Tuesday", schedule)


class TestGreedyAlgorithm(unittest.TestCase):
    """测试贪心算法"""

    def setUp(self):
        """准备测试数据"""
        self.test_activities = [
            {
                "activity_id": "ACT001",
                "activity_name": "算法课",
                "activity_type": "专业课",
                "start_time": "2026-05-12 08:00",
                "end_time": "2026-05-12 10:00",
                "required_capacity": 50,
                "priority": "high",
                "organizer": "计算机学院"
            },
            {
                "activity_id": "ACT002",
                "activity_name": "数据库课",
                "activity_type": "专业课",
                "start_time": "2026-05-12 09:00",
                "end_time": "2026-05-12 11:00",  # 与ACT001冲突
                "required_capacity": 50,
                "priority": "high",
                "organizer": "计算机学院"
            },
            {
                "activity_id": "ACT003",
                "activity_name": "社团活动",
                "activity_type": "社团活动",
                "start_time": "2026-05-12 14:00",
                "end_time": "2026-05-12 16:00",
                "required_capacity": 30,
                "priority": "low",
                "organizer": "ACM协会"
            }
        ]

        self.test_classrooms = [
            {
                "room_id": "R001",
                "room_name": "教三301",
                "building": "教学三楼",
                "capacity": 80,
                "facilities": ["投影仪", "空调"],
                "available": True
            },
            {
                "room_id": "R002",
                "room_name": "教三302",
                "building": "教学三楼",
                "capacity": 50,
                "facilities": ["投影仪"],
                "available": True
            }
        ]

    def test_no_conflict_allocation(self):
        """测试无冲突的活动分配"""
        # 只使用无冲突的活动
        activities = [self.test_activities[0], self.test_activities[2]]
        allocator = RoomAllocator(activities, self.test_classrooms)
        result = allocator.allocate_rooms()

        # 应该成功分配所有活动
        self.assertEqual(result["allocated_count"], 2)
        self.assertEqual(result["rejected_count"], 0)

    def test_conflict_handling(self):
        """测试时间冲突的处理"""
        allocator = RoomAllocator(self.test_activities, self.test_classrooms)
        result = allocator.allocate_rooms(priority_weight=False)

        # ACT001和ACT002冲突，贪心算法应该选择结束时间早的
        allocated_ids = [item["activity"]["activity_id"] for item in result["allocated_activities"]]
        self.assertIn("ACT001", allocated_ids)

    def test_capacity_constraint(self):
        """测试容量约束"""
        # 创建一个容量不足的场景
        large_activity = {
            "activity_id": "ACT004",
            "activity_name": "大型讲座",
            "activity_type": "学术讲座",
            "start_time": "2026-05-12 19:00",
            "end_time": "2026-05-12 21:00",
            "required_capacity": 200,  # 超过所有教室容量
            "priority": "high",
            "organizer": "学院"
        }

        activities = [large_activity]
        allocator = RoomAllocator(activities, self.test_classrooms)
        result = allocator.allocate_rooms()

        # 应该分配失败
        self.assertEqual(result["allocated_count"], 0)
        self.assertEqual(result["rejected_count"], 1)

    def test_priority_weight(self):
        """测试优先级权重"""
        allocator = RoomAllocator(self.test_activities, self.test_classrooms)
        result = allocator.allocate_rooms(priority_weight=True)

        # 高优先级活动应该被优先分配
        allocated = result["allocated_activities"]
        if len(allocated) > 0:
            first_allocated = allocated[0]["activity"]
            self.assertEqual(first_allocated["priority"], "high")

    def test_empty_activities(self):
        """测试空活动列表"""
        allocator = RoomAllocator([], self.test_classrooms)
        result = allocator.allocate_rooms()

        self.assertEqual(result["allocated_count"], 0)
        self.assertEqual(result["rejected_count"], 0)

    def test_room_utilization(self):
        """测试教室利用率计算"""
        allocator = RoomAllocator(self.test_activities, self.test_classrooms)
        result = allocator.allocate_rooms()
        utilization = allocator.get_room_utilization(result)

        # 检查utilization结构
        self.assertIsInstance(utilization, dict)
        for room_name, util_data in utilization.items():
            self.assertIn("usage_count", util_data)
            self.assertIn("total_hours", util_data)


class TestAlgorithmComparison(unittest.TestCase):
    """测试算法对比"""

    def test_time_complexity(self):
        """测试时间复杂度标注"""
        # 动态规划
        courses = [
            {
                "course_id": f"CS{i}",
                "course_name": f"课程{i}",
                "credits": 3,
                "teacher": "教授",
                "time_slots": [{"day": "Monday", "period": "1-2"}],
                "classroom": "教室",
                "capacity": 80
            }
            for i in range(5)
        ]
        selector = CourseSelector(courses)
        result_dp = selector.select_courses()

        # 检查时间复杂度标注
        self.assertIn("O(n", result_dp["time_complexity"])

        # 贪心算法
        activities = [
            {
                "activity_id": f"ACT{i}",
                "activity_name": f"活动{i}",
                "activity_type": "活动",
                "start_time": f"2026-05-12 {8+i}:00",
                "end_time": f"2026-05-12 {9+i}:00",
                "required_capacity": 50,
                "priority": "medium",
                "organizer": "组织"
            }
            for i in range(5)
        ]
        classrooms = [
            {
                "room_id": "R001",
                "room_name": "教室1",
                "building": "教学楼",
                "capacity": 80,
                "facilities": [],
                "available": True
            }
        ]
        allocator = RoomAllocator(activities, classrooms)
        result_greedy = allocator.allocate_rooms()

        # 检查时间复杂度标注
        self.assertIn("O(n log n)", result_greedy["time_complexity"])


def run_tests():
    """运行所有测试"""
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # 添加测试
    suite.addTests(loader.loadTestsFromTestCase(TestDynamicProgramming))
    suite.addTests(loader.loadTestsFromTestCase(TestGreedyAlgorithm))
    suite.addTests(loader.loadTestsFromTestCase(TestAlgorithmComparison))

    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result


if __name__ == "__main__":
    print("="*60)
    print("算法单元测试")
    print("="*60)
    result = run_tests()

    print("\n" + "="*60)
    print("测试总结")
    print("="*60)
    print(f"运行测试数: {result.testsRun}")
    print(f"成功: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")
    print("="*60)
