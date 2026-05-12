#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
北邮场景模拟数据生成器
生成课程、教室、活动数据用于算法演示
"""

import json
import random
from datetime import datetime, timedelta

# 北邮真实课程名称
COURSES = [
    "数据结构与算法", "计算机网络", "操作系统", "数据库原理", "软件工程",
    "计算机组成原理", "编译原理", "人工智能", "机器学习", "深度学习",
    "计算机图形学", "信息安全", "密码学", "网络安全", "云计算技术",
    "大数据技术", "分布式系统", "微服务架构", "区块链技术", "物联网技术",
    "移动应用开发", "Web前端开发", "Python程序设计", "Java程序设计", "C++程序设计",
    "数字信号处理", "通信原理", "电磁场与电磁波", "信号与系统", "数字电路",
    "模拟电路", "高等数学", "线性代数", "概率论与数理统计", "离散数学",
    "算法设计与分析", "形式语言与自动机", "计算理论", "量子计算", "神经网络",
    "自然语言处理", "计算机视觉", "语音识别", "推荐系统", "数据挖掘",
    "软件测试", "软件项目管理", "敏捷开发", "DevOps实践", "容器技术"
]

# 北邮教师姓氏
TEACHER_SURNAMES = ["张", "王", "李", "赵", "刘", "陈", "杨", "黄", "周", "吴",
                    "徐", "孙", "马", "朱", "胡", "郭", "何", "高", "林", "罗"]
TEACHER_TITLES = ["教授", "副教授", "讲师", "助教"]

# 时间段定义
WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
PERIODS = ["1-2", "3-4", "5-6", "7-8", "9-10"]

# 北邮教学楼和教室
BUILDINGS = {
    "教学三楼": {"prefix": "教三", "floors": 5, "rooms_per_floor": 10},
    "教学四楼": {"prefix": "教四", "floors": 6, "rooms_per_floor": 12},
    "科研楼": {"prefix": "科研", "floors": 8, "rooms_per_floor": 8},
    "学生活动中心": {"prefix": "学活", "floors": 3, "rooms_per_floor": 5}
}

# 活动类型
ACTIVITY_TYPES = ["专业课", "公选课", "学术讲座", "社团活动", "考试", "竞赛培训", "创业分享", "技术沙龙"]

# 社团和组织
ORGANIZATIONS = [
    "ACM协会", "创业协会", "机器人协会", "电子协会", "摄影协会",
    "计算机学院", "信息与通信工程学院", "网络空间安全学院", "人工智能学院",
    "学生会", "研究生会", "科技创新中心"
]


def generate_teacher_name():
    """生成教师姓名"""
    surname = random.choice(TEACHER_SURNAMES)
    title = random.choice(TEACHER_TITLES)
    return f"{surname}{title}"


def generate_classrooms():
    """生成教室数据"""
    classrooms = []
    room_id = 1

    for building_name, building_info in BUILDINGS.items():
        prefix = building_info["prefix"]
        floors = building_info["floors"]
        rooms_per_floor = building_info["rooms_per_floor"]

        for floor in range(1, floors + 1):
            for room_num in range(1, rooms_per_floor + 1):
                room_name = f"{prefix}{floor}{room_num:02d}"

                # 根据楼层和房间号确定容量
                if "学活" in prefix:
                    capacity = random.choice([200, 300, 500])  # 大型活动场地
                elif floor <= 2:
                    capacity = random.randint(30, 60)  # 小教室
                elif floor <= 4:
                    capacity = random.randint(80, 120)  # 中教室
                else:
                    capacity = random.randint(150, 200)  # 大教室

                classroom = {
                    "room_id": f"R{room_id:03d}",
                    "room_name": room_name,
                    "building": building_name,
                    "capacity": capacity,
                    "facilities": random.sample(
                        ["投影仪", "空调", "音响", "白板", "电脑", "网络"],
                        k=random.randint(3, 5)
                    ),
                    "available": True
                }
                classrooms.append(classroom)
                room_id += 1

    return classrooms


def generate_courses(classrooms, num_courses=40):
    """生成课程数据"""
    courses = []
    selected_courses = random.sample(COURSES, min(num_courses, len(COURSES)))

    for i, course_name in enumerate(selected_courses):
        # 随机选择教室
        classroom = random.choice(classrooms)

        # 随机选择时间段（每周2-3次课）
        num_sessions = random.choice([2, 3])
        time_slots = []
        selected_days = random.sample(WEEKDAYS, num_sessions)

        for day in selected_days:
            period = random.choice(PERIODS)
            time_slots.append({
                "day": day,
                "period": period
            })

        # 学分根据课程类型
        if "高等数学" in course_name or "线性代数" in course_name:
            credits = 5
        elif "实践" in course_name or "设计" in course_name:
            credits = 2
        else:
            credits = random.choice([3, 4])

        course = {
            "course_id": f"CS{i+101:03d}",
            "course_name": course_name,
            "credits": credits,
            "teacher": generate_teacher_name(),
            "time_slots": time_slots,
            "classroom": classroom["room_name"],
            "capacity": classroom["capacity"],
            "description": f"{course_name}是计算机相关专业的重要课程"
        }
        courses.append(course)

    return courses


def generate_activities(classrooms, num_activities=80):
    """生成活动数据"""
    activities = []

    # 生成一周的活动
    base_date = datetime(2026, 5, 12)  # 从周一开始

    for i in range(num_activities):
        # 随机选择日期（一周内）
        day_offset = random.randint(0, 6)
        activity_date = base_date + timedelta(days=day_offset)

        # 随机选择开始时间（8:00-20:00）
        start_hour = random.randint(8, 19)
        start_minute = random.choice([0, 30])
        start_time = activity_date.replace(hour=start_hour, minute=start_minute)

        # 活动时长（0.5-3小时）
        duration_hours = random.choice([0.5, 1, 1.5, 2, 2.5, 3])
        end_time = start_time + timedelta(hours=duration_hours)

        # 活动类型和名称
        activity_type = random.choice(ACTIVITY_TYPES)

        if activity_type == "学术讲座":
            activity_name = f"{random.choice(['人工智能', '区块链', '云计算', '大数据', '5G技术'])}前沿技术讲座"
        elif activity_type == "社团活动":
            activity_name = f"{random.choice(ORGANIZATIONS)}例会"
        elif activity_type == "竞赛培训":
            activity_name = f"{random.choice(['ACM', '蓝桥杯', '数学建模', '创新创业'])}赛前集训"
        elif activity_type == "考试":
            activity_name = f"{random.choice(COURSES)}期末考试"
        else:
            activity_name = f"{random.choice(COURSES)}"

        # 所需容量
        if activity_type in ["学术讲座", "考试"]:
            required_capacity = random.randint(100, 300)
        elif activity_type == "社团活动":
            required_capacity = random.randint(20, 60)
        else:
            required_capacity = random.randint(40, 120)

        # 优先级
        if activity_type == "考试":
            priority = "high"
        elif activity_type in ["专业课", "学术讲座"]:
            priority = "medium"
        else:
            priority = "low"

        activity = {
            "activity_id": f"ACT{i+1:03d}",
            "activity_name": activity_name,
            "activity_type": activity_type,
            "start_time": start_time.strftime("%Y-%m-%d %H:%M"),
            "end_time": end_time.strftime("%Y-%m-%d %H:%M"),
            "required_capacity": required_capacity,
            "priority": priority,
            "organizer": random.choice(ORGANIZATIONS),
            "description": f"{activity_name}活动安排"
        }
        activities.append(activity)

    # 按开始时间排序
    activities.sort(key=lambda x: x["start_time"])

    return activities


def generate_test_cases():
    """生成测试用例"""
    test_cases = {
        "course_selection": {
            "easy": {
                "description": "简单场景：10门课程，无复杂冲突",
                "num_courses": 10,
                "student_available_slots": 20,
                "min_credits": 12
            },
            "medium": {
                "description": "中等场景：20门课程，部分时间冲突",
                "num_courses": 20,
                "student_available_slots": 15,
                "min_credits": 16
            },
            "hard": {
                "description": "困难场景：30门课程，大量时间冲突",
                "num_courses": 30,
                "student_available_slots": 12,
                "min_credits": 20
            }
        },
        "room_allocation": {
            "weekday_peak": {
                "description": "工作日高峰：大量课程和活动",
                "day": "Monday",
                "num_activities": 50
            },
            "weekend": {
                "description": "周末场景：主要是社团活动和讲座",
                "day": "Saturday",
                "num_activities": 30
            },
            "exam_week": {
                "description": "考试周：大量考试安排",
                "day": "Wednesday",
                "num_activities": 40
            }
        }
    }
    return test_cases


def main():
    """主函数：生成所有数据"""
    print("开始生成北邮场景模拟数据...")

    # 1. 生成教室数据
    print("\n[1/4] 生成教室数据...")
    classrooms = generate_classrooms()
    print(f"✓ 已生成 {len(classrooms)} 个教室")

    # 2. 生成课程数据
    print("\n[2/4] 生成课程数据...")
    courses = generate_courses(classrooms, num_courses=40)
    print(f"✓ 已生成 {len(courses)} 门课程")

    # 3. 生成活动数据
    print("\n[3/4] 生成活动数据...")
    activities = generate_activities(classrooms, num_activities=80)
    print(f"✓ 已生成 {len(activities)} 个活动")

    # 4. 生成测试用例
    print("\n[4/4] 生成测试用例...")
    test_cases = generate_test_cases()
    print(f"✓ 已生成测试用例配置")

    # 保存数据到JSON文件
    print("\n保存数据到文件...")

    with open('classrooms.json', 'w', encoding='utf-8') as f:
        json.dump(classrooms, f, ensure_ascii=False, indent=2)
    print("✓ classrooms.json")

    with open('courses.json', 'w', encoding='utf-8') as f:
        json.dump(courses, f, ensure_ascii=False, indent=2)
    print("✓ courses.json")

    with open('activities.json', 'w', encoding='utf-8') as f:
        json.dump(activities, f, ensure_ascii=False, indent=2)
    print("✓ activities.json")

    with open('test_cases.json', 'w', encoding='utf-8') as f:
        json.dump(test_cases, f, ensure_ascii=False, indent=2)
    print("✓ test_cases.json")

    # 生成数据统计报告
    print("\n" + "="*50)
    print("数据生成完成！统计信息：")
    print("="*50)
    print(f"教室总数: {len(classrooms)}")
    print(f"  - 小教室(30-60人): {len([r for r in classrooms if r['capacity'] <= 60])}")
    print(f"  - 中教室(80-120人): {len([r for r in classrooms if 60 < r['capacity'] <= 120])}")
    print(f"  - 大教室(120+人): {len([r for r in classrooms if r['capacity'] > 120])}")
    print(f"\n课程总数: {len(courses)}")
    print(f"  - 2学分: {len([c for c in courses if c['credits'] == 2])}")
    print(f"  - 3学分: {len([c for c in courses if c['credits'] == 3])}")
    print(f"  - 4学分: {len([c for c in courses if c['credits'] == 4])}")
    print(f"  - 5学分: {len([c for c in courses if c['credits'] == 5])}")
    print(f"\n活动总数: {len(activities)}")
    for act_type in ACTIVITY_TYPES:
        count = len([a for a in activities if a['activity_type'] == act_type])
        print(f"  - {act_type}: {count}")
    print("="*50)


if __name__ == "__main__":
    main()
