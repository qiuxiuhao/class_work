#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
算法对比分析模块
对比动态规划和贪心算法在不同场景下的性能表现
"""

import json
import time
import matplotlib.pyplot as plt
import matplotlib
from typing import Dict, List
import sys
import os

# 设置中文字体
matplotlib.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'STHeiti']
matplotlib.rcParams['axes.unicode_minus'] = False

# 添加父目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from algorithms.dynamic_programming import CourseSelector, load_courses_from_file
from algorithms.greedy import RoomAllocator, load_data_from_file


class AlgorithmComparator:
    """算法对比分析器"""

    def __init__(self):
        self.comparison_results = []

    def compare_time_complexity(self, courses_path: str, activities_path: str, classrooms_path: str):
        """
        对比时间复杂度

        Args:
            courses_path: 课程数据路径
            activities_path: 活动数据路径
            classrooms_path: 教室数据路径

        Returns:
            对比结果
        """
        print("="*60)
        print("算法时间复杂度对比")
        print("="*60)

        # 加载数据
        courses = load_courses_from_file(courses_path)
        activities, classrooms = load_data_from_file(activities_path, classrooms_path)

        results = {
            "dynamic_programming": {},
            "greedy": {}
        }

        # 测试不同规模的数据
        test_sizes = [5, 10, 15, 20]

        print("\n动态规划算法（课程选择）：")
        print("-"*60)
        dp_times = []
        dp_sizes = []

        for size in test_sizes:
            if size > len(courses):
                break

            test_courses = courses[:size]
            selector = CourseSelector(test_courses)

            start = time.time()
            result = selector.select_courses()
            end = time.time()

            execution_time = end - start
            dp_times.append(execution_time)
            dp_sizes.append(size)

            print(f"数据规模 n={size:2d}: 执行时间 {execution_time:.4f}秒, "
                  f"探索状态数 {result['dp_states_explored']}")

        results["dynamic_programming"] = {
            "sizes": dp_sizes,
            "times": dp_times,
            "complexity": "O(n × 2^m)",
            "description": "时间复杂度随课程数和时间段数指数增长"
        }

        print("\n贪心算法（教室分配）：")
        print("-"*60)
        greedy_times = []
        greedy_sizes = []

        for size in test_sizes:
            if size > len(activities):
                break

            test_activities = activities[:size]
            allocator = RoomAllocator(test_activities, classrooms)

            start = time.time()
            result = allocator.allocate_rooms()
            end = time.time()

            execution_time = end - start
            greedy_times.append(execution_time)
            greedy_sizes.append(size)

            print(f"数据规模 n={size:2d}: 执行时间 {execution_time:.4f}秒, "
                  f"分配成功 {result['allocated_count']}/{size}")

        results["greedy"] = {
            "sizes": greedy_sizes,
            "times": greedy_times,
            "complexity": "O(n log n)",
            "description": "时间复杂度主要由排序决定，增长较慢"
        }

        return results

    def compare_space_complexity(self, courses_path: str):
        """
        对比空间复杂度

        Args:
            courses_path: 课程数据路径

        Returns:
            对比结果
        """
        print("\n" + "="*60)
        print("算法空间复杂度对比")
        print("="*60)

        courses = load_courses_from_file(courses_path)

        results = {
            "dynamic_programming": {
                "complexity": "O(n × 2^m)",
                "description": "需要存储所有状态的DP表，空间消耗大",
                "example": f"对于{len(courses)}门课程，25个时间段，理论最大状态数为 {len(courses)} × 2^25 ≈ {len(courses) * (2**25) / 1e9:.2f}B"
            },
            "greedy": {
                "complexity": "O(n + m)",
                "description": "只需存储活动列表和教室时间表，空间消耗小",
                "example": f"对于80个活动，201个教室，空间复杂度为 O(80 + 201) = O(281)"
            }
        }

        print("\n动态规划：")
        print(f"  复杂度: {results['dynamic_programming']['complexity']}")
        print(f"  说明: {results['dynamic_programming']['description']}")
        print(f"  示例: {results['dynamic_programming']['example']}")

        print("\n贪心算法：")
        print(f"  复杂度: {results['greedy']['complexity']}")
        print(f"  说明: {results['greedy']['description']}")
        print(f"  示例: {results['greedy']['example']}")

        return results

    def compare_optimality(self, courses_path: str, activities_path: str, classrooms_path: str):
        """
        对比算法最优性

        Args:
            courses_path: 课程数据路径
            activities_path: 活动数据路径
            classrooms_path: 教室数据路径

        Returns:
            对比结果
        """
        print("\n" + "="*60)
        print("算法最优性对比")
        print("="*60)

        results = {
            "dynamic_programming": {
                "optimality": "全局最优",
                "guarantee": "保证找到最优解",
                "reason": "通过穷举所有可能的状态组合，确保找到全局最优解"
            },
            "greedy": {
                "optimality": "全局最优",
                "guarantee": "对于区间调度问题，贪心策略保证全局最优",
                "reason": "按结束时间排序的贪心策略具有贪心选择性质和最优子结构"
            }
        }

        print("\n动态规划（课程选择）：")
        print(f"  最优性: {results['dynamic_programming']['optimality']}")
        print(f"  保证: {results['dynamic_programming']['guarantee']}")
        print(f"  原因: {results['dynamic_programming']['reason']}")

        print("\n贪心算法（教室分配）：")
        print(f"  最优性: {results['greedy']['optimality']}")
        print(f"  保证: {results['greedy']['guarantee']}")
        print(f"  原因: {results['greedy']['reason']}")

        # 实际测试
        print("\n实际测试验证：")
        print("-"*60)

        # 测试动态规划
        courses = load_courses_from_file(courses_path)[:10]
        selector = CourseSelector(courses)
        dp_result = selector.select_courses()
        print(f"动态规划: 选择了{dp_result['num_courses']}门课程，总学分{dp_result['total_credits']}")

        # 测试贪心算法
        activities, classrooms = load_data_from_file(activities_path, classrooms_path)
        allocator = RoomAllocator(activities[:30], classrooms[:10])
        greedy_result = allocator.allocate_rooms()
        print(f"贪心算法: 分配了{greedy_result['allocated_count']}/{len(activities[:30])}个活动")

        return results

    def compare_applicability(self):
        """
        对比算法适用场景

        Returns:
            对比结果
        """
        print("\n" + "="*60)
        print("算法适用场景对比")
        print("="*60)

        results = {
            "dynamic_programming": {
                "problem_type": "0-1背包变种（带时间约束）",
                "characteristics": [
                    "需要考虑多重约束（时间冲突、学分要求）",
                    "目标是优化某个指标（最大学分）",
                    "子问题之间有重叠",
                    "具有最优子结构"
                ],
                "advantages": [
                    "保证全局最优解",
                    "可以处理复杂约束",
                    "适合优化问题"
                ],
                "disadvantages": [
                    "时间复杂度高（指数级）",
                    "空间复杂度高",
                    "数据规模受限"
                ],
                "suitable_scenarios": [
                    "课程选择优化",
                    "资源分配优化",
                    "背包问题",
                    "最优路径问题"
                ]
            },
            "greedy": {
                "problem_type": "区间调度问题",
                "characteristics": [
                    "贪心选择性质明确（按结束时间）",
                    "具有最优子结构",
                    "局部最优能导致全局最优",
                    "问题可以分解为独立子问题"
                ],
                "advantages": [
                    "时间复杂度低（O(n log n)）",
                    "空间复杂度低",
                    "实现简单",
                    "可处理大规模数据"
                ],
                "disadvantages": [
                    "只适用于特定问题",
                    "需要证明贪心策略的正确性",
                    "不能处理复杂约束"
                ],
                "suitable_scenarios": [
                    "活动选择问题",
                    "教室分配问题",
                    "任务调度问题",
                    "区间覆盖问题"
                ]
            }
        }

        print("\n动态规划：")
        print(f"  问题类型: {results['dynamic_programming']['problem_type']}")
        print("  优点:")
        for adv in results['dynamic_programming']['advantages']:
            print(f"    - {adv}")
        print("  缺点:")
        for dis in results['dynamic_programming']['disadvantages']:
            print(f"    - {dis}")

        print("\n贪心算法：")
        print(f"  问题类型: {results['greedy']['problem_type']}")
        print("  优点:")
        for adv in results['greedy']['advantages']:
            print(f"    - {adv}")
        print("  缺点:")
        for dis in results['greedy']['disadvantages']:
            print(f"    - {dis}")

        return results

    def generate_comparison_report(self, output_path: str = "comparison_report.json"):
        """
        生成完整的对比报告

        Args:
            output_path: 输出文件路径
        """
        report = {
            "title": "动态规划 vs 贪心算法对比分析",
            "algorithms": {
                "dynamic_programming": {
                    "name": "动态规划",
                    "problem": "北邮学生选课优化问题",
                    "time_complexity": "O(n × 2^m)",
                    "space_complexity": "O(n × 2^m)",
                    "optimality": "全局最优"
                },
                "greedy": {
                    "name": "贪心算法",
                    "problem": "北邮教室资源分配问题",
                    "time_complexity": "O(n log n)",
                    "space_complexity": "O(n + m)",
                    "optimality": "全局最优"
                }
            },
            "comparison_dimensions": [
                "时间复杂度",
                "空间复杂度",
                "最优性保证",
                "适用场景",
                "实现难度"
            ]
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        print(f"\n对比报告已保存到: {output_path}")

    def visualize_time_complexity(self, time_results: Dict, output_path: str = "time_complexity.png"):
        """
        可视化时间复杂度对比

        Args:
            time_results: compare_time_complexity的返回结果
            output_path: 输出图片路径
        """
        plt.figure(figsize=(10, 6))

        # 绘制动态规划
        dp_data = time_results["dynamic_programming"]
        plt.plot(dp_data["sizes"], dp_data["times"], 'o-', label=f'动态规划 {dp_data["complexity"]}', linewidth=2)

        # 绘制贪心算法
        greedy_data = time_results["greedy"]
        plt.plot(greedy_data["sizes"], greedy_data["times"], 's-', label=f'贪心算法 {greedy_data["complexity"]}', linewidth=2)

        plt.xlabel('数据规模 (n)', fontsize=12)
        plt.ylabel('执行时间 (秒)', fontsize=12)
        plt.title('算法时间复杂度对比', fontsize=14, fontweight='bold')
        plt.legend(fontsize=10)
        plt.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"时间复杂度对比图已保存到: {output_path}")
        plt.close()


def main():
    """主函数"""
    print("="*60)
    print("算法对比分析")
    print("="*60)

    # 创建对比器
    comparator = AlgorithmComparator()

    # 数据文件路径
    courses_path = '../data/courses.json'
    activities_path = '../data/activities.json'
    classrooms_path = '../data/classrooms.json'

    # 1. 时间复杂度对比
    time_results = comparator.compare_time_complexity(
        courses_path, activities_path, classrooms_path
    )

    # 2. 空间复杂度对比
    space_results = comparator.compare_space_complexity(courses_path)

    # 3. 最优性对比
    optimality_results = comparator.compare_optimality(
        courses_path, activities_path, classrooms_path
    )

    # 4. 适用场景对比
    applicability_results = comparator.compare_applicability()

    # 5. 生成对比报告
    comparator.generate_comparison_report('../data/comparison_report.json')

    # 6. 生成可视化图表
    comparator.visualize_time_complexity(time_results, '../data/time_complexity.png')

    print("\n" + "="*60)
    print("对比分析完成")
    print("="*60)


if __name__ == "__main__":
    main()
