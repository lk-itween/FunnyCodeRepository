"""
构建任务系统：
获取所有楼层响应，对已有电梯当前所在楼层依次对响应的楼层进行距离测算，按照距离优先将楼层划分成任务并派发。
"""
import pandas as pd
from ElevatorNode import BuildingList, Elevator


def get_task_list(name_list):
    """创建多任务列表"""
    elevator_task = []
    for i in name_list:
        elevator_i = eval(i)
        elevator_task.append(linked.get_floor_multiple(i, elevator_i.floor, elevator_i.go_max, elevator_i.up))
    return elevator_task


def get_floor_min_data(elevator_task, name_list):
    """划分楼层任务"""
    data = pd.DataFrame()
    for num, i in enumerate(elevator_task):
        if num == 0:
            data = i
        else:
            data = data.merge(i, on=['floor', 'up'])
    data['arg_min'] = data[name_list].apply(lambda x: x.argmin(), axis=1)
    data['floor_min'] = data[['floor', 'up']].apply(lambda x: x[0] if x[1] > 0 else -x[0], axis=1)
    return data


def get_task_dict(name_list, data):
    """派发楼层任务至各个电梯"""
    task_dict = {}
    for num, i in enumerate(name_list):
        data_c = data[data['arg_min'] == num].copy()
        if data_c.empty:
            task_dict[i] = [eval(i).floor, eval(i).up]
        else:
            go_min_data = data_c[data_c['up'] == 1]
            if go_min_data.empty:
                go_min_data = data_c[data_c['up'] == 0]
            go_min = go_min_data['floor_min'].min()
            task_dict[i] = data_c[data_c['floor_min'] == go_min][['floor', 'up']].to_numpy()[0]
    return task_dict


def task_execute(task_dict):
    """电梯任务执行"""
    for name, floor_index in task_dict.items():
        elevator_i = eval(name)
        elevator_i_floor = elevator_i.floor
        print(elevator_i_floor)
        linked_data = linked.get_value_by_index(elevator_i_floor)
        linked_data_resp = elevator_i.coordination_goto(name, floor_index, linked_data)
        if linked_data_resp == -1:
            continue
        linked.update_data(elevator_i_floor, linked_data_resp)


def direct_finally(name_list):
    """楼宇无响应请求，将仍在运行的电梯分别处理成单电梯模式运行"""
    for i in name_list:
        elevator_i = eval(i)
        if elevator_i.person_data.empty:
            name_list.remove(i)
            continue
        elevator_i.independence_goto(elevator_i.floor, [])
    return name_list


def multi_elevator(name_list):
    """多电梯模式运行"""
    while True:
        task_elevator_list = get_task_list(name_list)
        floor_min_data = get_floor_min_data(task_elevator_list, name_list)
        task_elevator_dict = get_task_dict(name_list, floor_min_data)
        task_execute(task_elevator_dict)
        # 可增加更新楼层响应部分
        print('---楼层---')
        print(linked.data)
        print('---楼层---')
        if linked.is_pause():
            while True:
                name_list = direct_finally(name_list)
                if not name_list:
                    break
            break


def single_elevator(name_list):
    """独立电梯模式运行"""
    elevator = eval(name_list[0])
    while True:
        print('---当前楼层：', elevator.floor)
        data = linked.get_value_by_index(elevator.floor)
        floor_distinct_max = linked.get_floor_single(elevator.floor, elevator.up)
        linked.update_data(elevator.floor, elevator.independence_goto(floor_distinct_max, data))
        # 可增加更新楼层响应部分
        print('--楼层---')
        print(linked.data)
        if linked.is_pause() and elevator.person_data.empty:
            break


if __name__ == '__main__':
    model = '多电梯'
    min_floor, max_floor = -1, 30
    linked = BuildingList(min_floor, max_floor)
    elevator_1 = Elevator(min_floor, max_floor)
    elevator_2 = Elevator(min_floor, max_floor, 5)
    elevator_3 = Elevator(min_floor, max_floor, 10)
    elevator_2.go_max = 10
    elevator_3.go_max = 15
    elevator_name_list = ['elevator_1', 'elevator_2', 'elevator_3']
    if model == '多电梯':
        multi_elevator(elevator_name_list)
    elif model == '单电梯':
        single_elevator(elevator_name_list)
    else:
        print('未运行')
