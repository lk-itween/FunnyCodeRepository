import random


class PeopleRandom:
    """
    构造随机人物模型
    返回各人物属性值，包含：所在楼层，体重，是否上楼，去往楼层
    """

    def __init__(self, floor: int, floors: tuple = (1, 30), people: int = 1):
        self.floor = floor
        self.floor_min, self.floor_max = floors
        self.people = people
        self.weight = self.set_weight()
        self.up = random.randint(0, 1)
        self.floor_go = self.go()

    def __call__(self, *args, **kwargs):
        """重载类"""
        self.weight = self.set_weight()
        self.up = random.randint(0, 1)
        self.floor_go = self.go()

    @classmethod
    def people_random(cls, floor, floors):
        """重载当前类，定义类属性"""
        dic = cls(floor, floors).__dict__
        dic.pop('people')
        dic.pop('floor_min')
        dic.pop('floor_max')
        return dic

    @staticmethod
    def set_weight():
        """设置人物模型体重"""
        while True:
            weight = round(random.normalvariate(60, 10), 2)
            if 20 <= weight <= 150:
                break
        return weight

    def go(self):
        """
        返回人上下楼倾向
        """
        if self.floor == self.floor_min:  # 当在最低层时，只有上楼倾向
            self.up = 1
        elif self.floor == self.floor_max:  # 当在最高层时，只有下楼倾向
            self.up = 0
        if self.up == 1:  # 上楼
            floor_random = [i for i in range(self.floor + 1, self.floor_max + 1) if i != 0]
            return random.choice(floor_random)
        else:  # 下楼
            floor_random = [i for i in range(self.floor_min, self.floor) if i != 0]
            return random.choice(floor_random)

    def to_dict(self):
        """
        属性值字典化
        :return: `list`
        """
        people = self.people
        floor_min = self.floor_min
        floor_max = self.floor_max
        self.__dict__.pop('people')
        self.__dict__.pop('floor_min')
        self.__dict__.pop('floor_max')
        listing = [self.__dict__]
        for _ in range(1, people):
            listing.append(self.people_random(self.floor, (floor_min, floor_max)))
        return listing


class FloorsRandom:
    """
    随机楼层生成，楼层随机人数生成。
    """

    def __init__(self, floor_min: int, floor_max: int, people: int = 6):
        """
        输入的楼层是不存在0层，故而在floor_min进行加1后进行随机取数，如果小于等于0则减去1还原最低楼层。
        :param floor_min: 最低楼层
        :param floor_max: 最高楼层
        """
        self.floors = (floor_min, floor_max)
        self.people = people
        self.respond_floors = random.sample(range(floor_min + 1, floor_max + 1), random.randint(1, floor_max // 3))
        self.respond_floors = [i if i > 0 else i - 1 for i in self.respond_floors]

    def __call__(self, floor_min: int, floor_max: int, people: int = 6):
        """类重载，不需要重新实例化更改当前类"""
        self.floors = (floor_min, floor_max)
        self.people = people
        self.respond_floors = random.sample(range(floor_min + 1, floor_max + 1), random.randint(1, floor_max // 3))
        self.respond_floors = [i if i > 0 else i - 1 for i in self.respond_floors]

    def get_peoples(self):
        """获取楼层人数"""
        floor = self.respond_floors
        if self.people:
            return [PeopleRandom(i, self.floors, random.randint(1, self.people)).to_dict() for i in floor]
        else:
            return []
