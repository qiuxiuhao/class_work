#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
动态规划算法：北邮学生选课优化问题
问题类型：带时间约束的0-1背包问题

场景描述：
学生需要在有限的时间内选择课程，使得总学分最大化，同时避免时间冲突。

算法设计：
- 状态定义：dp[i][mask] 表示考虑前i门课程，占用时间段为mask时的最大学分
- 状态转移：对于第i门课程，选或不选
  - 不选：dp[i][mask] = dp[i-1][mask]
  - 选：如果时间不冲突，dp[i][mask] = max(dp[i-1][mask], dp[i-1][prev_mask] + credits[i])
- 时间复杂度：O(n × 2^m)，n为课程数，m为时间段数
"""

import json
import time
from typing import List, Dict, Tuple, Set


class CourseSelector:
    """课程选择优化器（动态规划实现）"""

    def __init__(self, courses: List[Dict], time_slots_config: Dict = None):
        """
        初始化课程选择器

        Args:
            courses: 课程列表
            time_slots_config: 时间段配置（可选）
        """
        self.courses = courses
        self.n = len(courses)

        # 时间段映射：将(day, period)映射到唯一的bit位
        if time_slots_config is None:
            self.weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
            self.periods = ["1-2", "3-4", "5-6", "7-8", "9-10"]
        else:
            self.weekdays = time_slots_config.get("weekdays", [])
            self.periods = time_slots_config.get("periods", [])

        self.time_slot_to_bit = {}
        bit_index = 0
        for day in self.weekdays:
            for period in self.periods:
                self.time_slot_to_bit[(day, period)] = bit_index
                bit_index += 1

        self.total_time_slots = bit_index

        # 预处理每门课程的时间掩码
        self.course_time_masks = []
        for course in courses:
            mask = self._get_time_mask(course["time_slots"])
            self.course_time_masks.append(mask)

        # 用于记录算法执行过程
        self.execution_log = []
        self.dp_table = None

    def _get_time_mask(self, time_slots: List[Dict]) -> int:
        """
        将课程的时间段列表转换为位掩码

        Args:
            time_slots: 时间段列表，如 [{"day": "Monday", "period": "1-2"}]

        Returns:
            时间掩码（整数）
        """
        mask = 0
        for slot in time_slots:
            day = slot["day"]
            period = slot["period"]
            if (day, period) in self.time_slot_to_bit:
                bit = self.time_slot_to_bit[(day, period)]
                mask |= (1 << bit)
        return mask

    def _has_conflict(self, mask1: int, mask2: int) -> bool:
        """
        检查两个时间掩码是否有冲突

        Args:
            mask1: 时间掩码1
            mask2: 时间掩码2

        Returns:
            True表示有冲突，False表示无冲突
        """
        return (mask1 & mask2) != 0

    def select_courses(self, max_courses: int = None, min_credits: int = 0) -> Dict:
        """
        使用动态规划选择最优课程组合

        Args:
            max_courses: 最多选择的课程数（可选）
            min_credits: 最低学分要求（可选）

        Returns:
            包含选课结果的字典
        """
        start_time = time.time()
        self.execution_log = []

        # 初始化DP表：dp[i][mask] = (max_credits, selected_courses)
        # 使用字典存储，只记录有效状态
        dp = [{} for _ in range(self.n + 1)]
        dp[0][0] = (0, [])  # 初始状态：0门课程，0时间占用，0学分

        self.execution_log.append({
            "step": "初始化",
            "description": f"开始处理{self.n}门课程，总时间段数：{self.total_time_slots}"
        })

        # 动态规划主循环
        for i in range(1, self.n + 1):
            course = self.courses[i - 1]
            course_mask = self.course_time_masks[i - 1]
            credits = course["credits"]

            self.execution_log.append({
                "step": f"考虑第{i}门课程",
                "course": course["course_name"],
                "credits": credits,
                "time_mask": bin(course_mask)
            })

            # 不选择当前课程：继承上一状态
            for mask, (max_credits, selected) in dp[i - 1].items():
                if mask not in dp[i] or dp[i][mask][0] < max_credits:
                    dp[i][mask] = (max_credits, selected[:])

            # 选择当前课程：检查时间冲突
            for prev_mask, (prev_credits, prev_selected) in dp[i - 1].items():
                if not self._has_conflict(prev_mask, course_mask):
                    # 无冲突，可以选择
                    new_mask = prev_mask | course_mask
                    new_credits = prev_credits + credits
                    new_selected = prev_selected + [i - 1]

                    # 检查课程数量限制
                    if max_courses is None or len(new_selected) <= max_courses:
                        if new_mask not in dp[i] or dp[i][new_mask][0] < new_credits:
                            dp[i][new_mask] = (new_credits, new_selected)

        # 找到最优解
        best_credits = 0
        best_selected = []
        best_mask = 0

        for mask, (credits, selected) in dp[self.n].items():
            if credits > best_credits and credits >= min_credits:
                best_credits = credits
                best_selected = selected
                best_mask = mask

        end_time = time.time()
        execution_time = end_time - start_time

        # 构建结果
        selected_courses = [self.courses[idx] for idx in best_selected]

        result = {
            "algorithm": "动态规划",
            "total_credits": best_credits,
            "num_courses": len(best_selected),
            "selected_courses": selected_courses,
            "time_mask": best_mask,
            "execution_time": execution_time,
            "time_complexity": f"O(n × 2^m) = O({self.n} × 2^{self.total_time_slots})",
            "space_complexity": f"O(n × 2^m) = O({self.n} × 2^{self.total_time_slots})",
            "dp_states_explored": sum(len(states) for states in dp),
            "execution_log": self.execution_log
        }

        self.dp_table = dp

        return result

    def get_schedule_visualization(self, selected_courses: List[Dict]) -> Dict:
        """
        生成课程表可视化数据

        Args:
            selected_courses: 选中的课程列表

        Returns:
            课程表数据
        """
        schedule = {}
        for day in self.weekdays:
            schedule[day] = {period: None for period in self.periods}

        for course in selected_courses:
            for slot in course["time_slots"]:
                day = slot["day"]
                period = slot["period"]
                if day in schedule and period in schedule[day]:
                    schedule[day][period] = {
                        "course_name": course["course_name"],
                        "teacher": course["teacher"],
                        "classroom": course["classroom"],
                        "credits": course["credits"]
                    }

        return schedule

    def analyze_solution(self, result: Dict) -> Dict:
        """
        分析解决方案的质量

        Args:
            result: select_courses返回的结果

        Returns:
            分析报告
        """
        selected_courses = result["selected_courses"]

        # 统计学分分布
        credit_distribution = {}
        for course in selected_courses:
            credits = course["credits"]
            credit_distribution[credits] = credit_distribution.get(credits, 0) + 1

        # 统计时间利用率
        occupied_slots = bin(result["time_mask"]).count('1')
        utilization_rate = occupied_slots / self.total_time_slots

        # 统计每天的课程数
        daily_courses = {day: 0 for day in self.weekdays}
        for course in selected_courses:
            for slot in course["time_slots"]:
                daily_courses[slot["day"]] += 1

        analysis = {
            "total_credits": result["total_credits"],
            "num_courses": result["num_courses"],
            "credit_distribution": credit_distribution,
            "time_utilization": f"{utilization_rate:.2%}",
            "occupied_time_slots": occupied_slots,
            "total_time_slots": self.total_time_slots,
            "daily_courses": daily_courses,
            "avg_credits_per_course": result["total_credits"] / result["num_courses"] if result["num_courses"] > 0 else 0
        }

        return analysis


def load_courses_from_file(file_path: str) -> List[Dict]:
    """从JSON文件加载课程数据"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def main():
    """测试动态规划算法"""
    print("="*60)
    print("动态规划算法：北邮学生选课优化问题")
    print("="*60)

    # 加载课程数据
    courses = load_courses_from_file('../data/courses.json')
    print(f"\n加载了 {len(courses)} 门课程")

    # 创建选课器
    selector = CourseSelector(courses)

    # 测试场景1：简单场景（选择前10门课程）
    print("\n" + "-"*60)
    print("测试场景1：简单场景（前10门课程）")
    print("-"*60)
    simple_courses = courses[:10]
    simple_selector = CourseSelector(simple_courses)
    result1 = simple_selector.select_courses()

    print(f"最优学分：{result1['total_credits']}")
    print(f"选课数量：{result1['num_courses']}")
    print(f"执行时间：{result1['execution_time']:.4f}秒")
    print(f"探索状态数：{result1['dp_states_explored']}")
    print("\n选中的课程：")
    for course in result1['selected_courses']:
        print(f"  - {course['course_name']} ({course['credits']}学分)")

    # 分析解决方案
    analysis1 = simple_selector.analyze_solution(result1)
    print(f"\n时间利用率：{analysis1['time_utilization']}")
    print(f"平均学分：{analysis1['avg_credits_per_course']:.2f}")

    # 测试场景2：中等场景（选择前20门课程）
    print("\n" + "-"*60)
    print("测试场景2：中等场景（前20门课程）")
    print("-"*60)
    medium_courses = courses[:20]
    medium_selector = CourseSelector(medium_courses)
    result2 = medium_selector.select_courses(min_credits=16)

    print(f"最优学分：{result2['total_credits']}")
    print(f"选课数量：{result2['num_courses']}")
    print(f"执行时间：{result2['execution_time']:.4f}秒")
    print(f"探索状态数：{result2['dp_states_explored']}")

    print("\n" + "="*60)
    print("测试完成")
    print("="*60)


if __name__ == "__main__":
    main()
