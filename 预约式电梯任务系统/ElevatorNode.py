import pandas as pd
from RandomModel import FloorsRandom


class BuildingList:
    """
    楼宇模型:
    最低楼层，最高楼层
    """

    def __init__(self, floor_min: int = -1, floor_max: int = 30):
        self.floor_min = floor_min
        self.floor_max = floor_max
        self.data = pd.DataFrame(columns=['floor', 'weight', 'up', 'floor_go'])
        self.set_data_all('simple')

    def is_pause(self):
        """楼宇各候厅层是否无请求"""
        return self.data.empty

    def random_model(self, model='simple'):
        """
        楼宇层随机生成模型.
        :param model: 默认`simple`: 生成人数适中，`complex`: 较多，其余不生成
        :return: pd.DataFrame
        """
        if model == 'complex':
            data = FloorsRandom(floor_min=self.floor_min, floor_max=self.floor_max, people=10).get_peoples()
        elif model == 'simple':
            data = FloorsRandom(floor_min=self.floor_min, floor_max=self.floor_max, people=6).get_peoples()
        else:
            data = FloorsRandom(floor_min=self.floor_min, floor_max=self.floor_max, people=0).get_peoples()
        return pd.concat([pd.DataFrame(i) for i in data])

    def get_floor_response(self):
        """获取有请求的楼层及其请求方向"""
        if self.data.empty:
            return pd.DataFrame(columns=['floor', 'up', 'up_flag'])
        data = self.data[['floor', 'up']].drop_duplicates(subset=['floor', 'up']).sort_values('floor').copy()
        data['up_flag'] = data.apply(
            lambda x: abs(x[1] - 1) if x[0] == self.floor_max or x[0] == self.floor_min else x[1], axis=1)
        return data

    def get_floor_single(self, floor, up=1):
        """
        单控单轨模式时，顺电梯方向运行，返回楼宇距电梯所在楼层的最远楼层
        :param floor: 电梯所在楼层
        :param up: 电梯方向
        :return: 目标最远楼层
        """
        data = self.get_floor_response()
        data = data[data['up_flag'] == up].copy()
        if up:
            bool_1 = data[data['floor'] >= floor]['floor'].unique().tolist()
            bool_2 = [self.floor_min]
        else:
            bool_1 = data[data['floor'] <= floor].sort_values('floor', ascending=False)['floor'].unique().tolist()
            bool_2 = [self.floor_max]
        return (bool_1 + bool_2)[0]

    def get_floor_multiple(self, name, floor, floor_go_max, up=1):
        """
        单控多轨电梯模式时，返回所有请求层与输入电梯的所在层的距离。
        :param name: 电梯名
        :param floor: 电梯所在层
        :param floor_go_max: 电梯内去往楼层的最远楼层
        :param up: 电梯方向
        :return: 所有请求层与输入电梯的所在层的距离
        """
        # 存在楼层为负数值，不存在0层，故将负数楼层都加1
        floor = floor if floor > 0 else floor + 1
        floor_go_max = floor_go_max if floor_go_max > 0 else floor_go_max + 1
        # 电梯内在不考虑外部请求的情况下，最远需要运行的楼层差
        go_max_distinct = abs(floor - floor_go_max) + 1
        data = self.get_floor_response()[['floor', 'up_flag']].copy()
        data.rename(columns={'up_flag': 'up'}, inplace=True)
        data['floor'] = data['floor'].map(lambda x: x if x > 0 else x + 1)

        def fix_distinct(x):
            """计算电梯到楼宇各层各需要运行的楼层差"""
            floor_data, up_data = x
            distinct = go_max_distinct + abs(floor_data - floor_go_max)
            if up_data == up:
                if (up == 0 and floor_data <= floor) or (up == 1 and floor_data >= floor):
                    return abs(floor_data - floor)
                else:
                    return distinct
            else:
                return distinct

        data[name] = data.apply(fix_distinct, axis=1)
        data['floor'] = data['floor'].map(lambda x: x if x > 0 else x - 1)
        return data

    def get_value_by_index(self, index):
        """获取当前楼层人数情况"""
        if not index or index < self.floor_min or index > self.floor_max:
            raise Exception('输入楼层数错误！')
        return self.data[self.data['floor'] == index].to_dict(orient='records')

    def update_data(self, index, data):
        """更新当前楼层人数，即电梯到达，人数减少。"""
        if not index or index < self.floor_min or index > self.floor_max:
            raise Exception('输入楼层数错误！')
        self.data.drop(self.data[self.data['floor'] == index].index, inplace=True)
        self.data = self.data.append(pd.DataFrame(data))
        self.data.reset_index(drop=True, inplace=True)

    def set_data_all(self, model='simple'):
        """
        输入楼层随机生成模型复杂度，返回当前楼宇所有候厅层基本情况。
        :param model: 默认`simple`: 每层楼人数生成数较少, `complex`: 生成数较多, 其他：不生成人数。
        :return: self.data: pd.DataFrame
        """
        self.data = pd.concat([self.data, self.random_model(model)])

    def clear(self):
        """清空当前楼宇候厅情况"""
        self.data = pd.DataFrame()

    def __str__(self):
        """
        重写__str__方法
        :return: print(class)输出为：[]->[]->[]样式
        """
        listing = []
        for i in range(self.floor_min, self.floor_max + 1):
            if i:
                listing.append(str(self.data[self.data['floor'] == i].to_dict(orient='records')))
        return '->'.join(listing)


class Elevator:
    """
    电梯模型：
    能够运行到的最低楼层，最高楼层及当前楼层
    """

    def __init__(self, floor_min, floor_max, floor: int = 1):
        self.floor = floor
        self.go_max = self.floor
        self.floor_min = floor_min
        self.floor_max = floor_max
        self.up = 1  # 1: 电梯上行，0：电梯下行
        self.weight = 1000  # 电梯限重
        self.persons = 12  # 电梯限制人员数量
        self.person_data = pd.DataFrame(columns=['floor', 'weight', 'up', 'floor_go'])

    def update_person_data(self, data, agg='add'):
        """更新电梯内的人的情况"""
        persons = len(data)
        # time.sleep(persons)
        if agg == 'add':
            self.weight = round(self.weight + data['weight'].sum(), 2)  # 重量
            self.persons = self.persons + persons  # 数量
        elif agg == 'sub':
            self.weight = round(self.weight - data['weight'].sum(), 2)
            self.persons = self.persons - persons
        else:
            raise Exception('输入运算符错误！')

    def auto_reverse(self, floor):
        """电梯到达距离最远的目标楼层，换向运行"""
        if self.floor == floor or self.floor == self.floor_max:
            self.up = 0 if self.up else 1

    def floor_reverse(self, floor):
        """电梯反向"""
        self.go_max = self.floor
        if not self.person_data.empty:
            if self.up:
                floor = self.person_data['floor_go'].max()
            else:
                floor = self.person_data['floor_go'].min()
            self.go_max = floor
        if self.up and floor < self.floor:
            self.up = 0
        elif not self.up and floor > self.floor:
            self.up = 1

    def next(self):
        """电梯所有行为执行完毕，继续上升或下降"""
        if self.up:
            self.floor += 1
        else:
            self.floor -= 1
        if not self.floor:  # self.floor 逐次计数后为0时调整self.floor
            self.floor = self.floor + 1 if self.up else self.floor - 1

    def get_out_of_elevator(self):
        """出电梯"""
        self.person_data.reset_index(drop=True, inplace=True)
        data = self.person_data.copy()
        data = data[data['floor_go'] == self.floor].copy()
        self.update_person_data(data, 'add')
        self.person_data.drop(data.index, inplace=True)

    def take_elevator(self, elevator_data):
        """进电梯"""
        if not elevator_data:
            return elevator_data
        elevator_data = pd.DataFrame(elevator_data, dtype='int')
        data = elevator_data[elevator_data['up'] == self.up].copy()
        data2 = elevator_data[elevator_data['up'] != self.up].copy()
        while data['weight'].sum() > self.weight and not data.empty:  # 超重
            weight_max = data[data['weight'] == data['weight'].max()].index
            data2 = data2.append(data.loc[weight_max, :])
            data.drop(weight_max, inplace=True)
        while len(data) > self.persons and not data.empty:  # 超载
            weight_min = data[data['weight'] == data['weight'].min()].index
            data2 = data2.append(data.loc[weight_min, :])
            data.drop(weight_min, inplace=True)
        self.person_data = self.person_data.append(data)
        self.update_person_data(data, 'sub')
        return data2.to_dict(orient='records')

    def elevator(self, floor, data):
        """
        先下后上，返回电梯现状
        :param floor: 目标楼层
        :param data: 目标楼层的情况
        :return: 不满足上乘电梯的乘客
        """
        self.get_out_of_elevator()
        resp = self.take_elevator(data)
        self.floor_reverse(floor)
        return resp

    def independence_goto(self, floor, data):
        """独立运作"""
        self.auto_reverse(self.floor_min)
        resp = self.elevator(floor, data)
        print('--电梯---')
        print(self.person_data)
        self.next()
        return resp

    def coordination_goto(self, name, go_floor_min, data):
        """协同运作"""
        resp = -1
        go_fl_min, up = go_floor_min
        up = abs(up - 1) if go_fl_min == self.floor_max or go_fl_min == self.floor_min else up
        func = min if up else max
        fl_distinct = self.person_data[self.person_data['up'] == up]['floor_go'].agg(func)
        fl_distinct = fl_distinct if isinstance(fl_distinct, int) else self.floor
        distinct = func(fl_distinct, go_fl_min)
        self.auto_reverse(self.floor_min)
        if distinct == self.floor:
            resp = self.elevator(go_fl_min, data)
        print(f'---电梯{name}-{self.floor}--')
        print(self.person_data)
        print('---电梯---')
        # 模拟电梯无楼层请求响应，加速电梯驶过
        if go_fl_min == self.floor and not data:
            self.auto_reverse(self.floor_min)
            if self.person_data.empty:
                # 并且电梯内无乘客，电梯停靠在当前楼层
                return resp
            elif go_fl_min < fl_distinct - 1:
                self.next()
        self.next()
        return resp
