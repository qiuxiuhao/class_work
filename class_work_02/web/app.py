#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flask Web应用 - 算法可视化展示
提供动态规划和贪心算法的交互式演示
"""

from flask import Flask, render_template, jsonify, request
import sys
import os
import json

# 添加父目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from algorithms.dynamic_programming import CourseSelector, load_courses_from_file
from algorithms.greedy import RoomAllocator, load_data_from_file

app = Flask(__name__)

# 数据文件路径
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
COURSES_PATH = os.path.join(DATA_DIR, 'courses.json')
ACTIVITIES_PATH = os.path.join(DATA_DIR, 'activities.json')
CLASSROOMS_PATH = os.path.join(DATA_DIR, 'classrooms.json')


@app.route('/')
def index():
    """首页"""
    return render_template('index.html')


@app.route('/dynamic-programming')
def dynamic_programming_page():
    """动态规划算法页面"""
    return render_template('dynamic_programming.html')


@app.route('/greedy')
def greedy_page():
    """贪心算法页面"""
    return render_template('greedy.html')


@app.route('/comparison')
def comparison_page():
    """算法对比页面"""
    return render_template('comparison.html')


# ==================== API接口 ====================

@app.route('/api/courses')
def get_courses():
    """获取课程列表"""
    try:
        courses = load_courses_from_file(COURSES_PATH)
        return jsonify({
            'success': True,
            'data': courses,
            'count': len(courses)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/activities')
def get_activities():
    """获取活动列表"""
    try:
        activities, _ = load_data_from_file(ACTIVITIES_PATH, CLASSROOMS_PATH)
        return jsonify({
            'success': True,
            'data': activities,
            'count': len(activities)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/classrooms')
def get_classrooms():
    """获取教室列表"""
    try:
        _, classrooms = load_data_from_file(ACTIVITIES_PATH, CLASSROOMS_PATH)
        return jsonify({
            'success': True,
            'data': classrooms,
            'count': len(classrooms)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/dp/run', methods=['POST'])
def run_dynamic_programming():
    """运行动态规划算法"""
    try:
        data = request.get_json()
        course_indices = data.get('course_indices', None)
        max_courses = data.get('max_courses', None)
        min_credits = data.get('min_credits', 0)

        # 加载课程数据
        all_courses = load_courses_from_file(COURSES_PATH)

        # 如果指定了课程索引，只使用这些课程
        if course_indices:
            courses = [all_courses[i] for i in course_indices if i < len(all_courses)]
        else:
            courses = all_courses

        # 创建选课器并运行
        selector = CourseSelector(courses)
        result = selector.select_courses(max_courses=max_courses, min_credits=min_credits)

        # 生成课程表可视化数据
        schedule = selector.get_schedule_visualization(result['selected_courses'])

        # 分析解决方案
        analysis = selector.analyze_solution(result)

        return jsonify({
            'success': True,
            'result': {
                'total_credits': result['total_credits'],
                'num_courses': result['num_courses'],
                'selected_courses': result['selected_courses'],
                'execution_time': result['execution_time'],
                'time_complexity': result['time_complexity'],
                'space_complexity': result['space_complexity'],
                'dp_states_explored': result['dp_states_explored'],
                'schedule': schedule,
                'analysis': analysis,
                'execution_log': result['execution_log'][:20]  # 只返回前20条日志
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/greedy/run', methods=['POST'])
def run_greedy():
    """运行贪心算法"""
    try:
        data = request.get_json()
        activity_indices = data.get('activity_indices', None)
        classroom_indices = data.get('classroom_indices', None)
        priority_weight = data.get('priority_weight', True)

        # 加载数据
        all_activities, all_classrooms = load_data_from_file(ACTIVITIES_PATH, CLASSROOMS_PATH)

        # 如果指定了索引，只使用这些数据
        if activity_indices:
            activities = [all_activities[i] for i in activity_indices if i < len(all_activities)]
        else:
            activities = all_activities

        if classroom_indices:
            classrooms = [all_classrooms[i] for i in classroom_indices if i < len(all_classrooms)]
        else:
            classrooms = all_classrooms

        # 创建分配器并运行
        allocator = RoomAllocator(activities, classrooms)
        result = allocator.allocate_rooms(priority_weight=priority_weight)

        # 获取教室利用率
        utilization = allocator.get_room_utilization(result)

        # 分析解决方案
        analysis = allocator.analyze_solution(result)

        # 获取时间线数据（只返回前5个教室）
        timeline = allocator.get_timeline_visualization(result)
        timeline_limited = dict(list(timeline.items())[:5])

        return jsonify({
            'success': True,
            'result': {
                'total_activities': result['total_activities'],
                'allocated_count': result['allocated_count'],
                'rejected_count': result['rejected_count'],
                'allocation_rate': result['allocation_rate'],
                'allocated_activities': result['allocated_activities'][:20],  # 限制返回数量
                'rejected_activities': result['rejected_activities'][:20],
                'execution_time': result['execution_time'],
                'time_complexity': result['time_complexity'],
                'space_complexity': result['space_complexity'],
                'utilization': utilization,
                'analysis': analysis,
                'timeline': timeline_limited,
                'execution_log': result['execution_log'][:20]
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/comparison/data')
def get_comparison_data():
    """获取算法对比数据"""
    try:
        comparison_path = os.path.join(DATA_DIR, 'comparison_report.json')
        with open(comparison_path, 'r', encoding='utf-8') as f:
            comparison_data = json.load(f)

        return jsonify({
            'success': True,
            'data': comparison_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    print("="*60)
    print("算法可视化Web应用启动")
    print("="*60)
    print("访问地址：")
    print("  - 首页: http://127.0.0.1:5000/")
    print("  - 动态规划: http://127.0.0.1:5000/dynamic-programming")
    print("  - 贪心算法: http://127.0.0.1:5000/greedy")
    print("  - 算法对比: http://127.0.0.1:5000/comparison")
    print("="*60)
    app.run(debug=True, host='0.0.0.0', port=5000)
