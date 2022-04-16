# 拯救pandas计划（8）——当列聚合数与自身进行再次计算

最近发现周围的很多小伙伴们都不太乐意使用pandas，转而投向其他的数据操作库，身为一个数据工作者，基本上是张口pandas，闭口pandas了，故而写下此系列以让更多的小伙伴们爱上pandas。

系列文章说明：

> 系列名（系列文章序号）——此次系列文章具体解决的需求

**平台：**

- windows 10
- python 3.8
- pandas >=1.2.4

## / 数据需求

当列聚合数与自身进行再次计算，例如当列按照类别进行分组聚合后，使用这个单元格的数据使用四则运算或者其他计算方法对聚合结果进行再次计算。

## / 函数分享

本篇不解决任何需求，出门右转有很多对应的解决方案，这里分享一则针对题目思考后的函数，函数中有诸多纰漏，仅做抛砖引玉之用，大可拿去针对自我需求产出见解。

```python
def calculate_func(x, args):
    """
    平均值二次计算：使用四则运算选择器, 通过args传入的顺序，
    对相应列使用对应方法，使当前列四则运算分类结果的平均值
    :params x: pd.DataFrame
    :params args: tuple, 计算列对应的操作方式
    return 返回所有列横向合并后的pd.DataFrame对象

    example:
    df = pd.DataFrame([{'day': 'Fri', 'size': 4, 'total_bill': 40.17, 'tip': 4.73},
                 {'day': 'Fri', 'size': 2, 'total_bill': 28.97, 'tip': 3.0},
                 {'day': 'Fri', 'size': 2, 'total_bill': 27.28, 'tip': 4.0},
                 {'day': 'Sat', 'size': 3, 'total_bill': 50.81, 'tip': 10.0},
                 {'day': 'Sat', 'size': 4, 'total_bill': 48.33, 'tip': 9.0},
                 {'day': 'Sat', 'size': 4, 'total_bill': 48.27, 'tip': 6.73},
                 {'day': 'Sun', 'size': 6, 'total_bill': 48.17, 'tip': 5.0},
                 {'day': 'Sun', 'size': 3, 'total_bill': 45.35, 'tip': 3.5},
                 {'day': 'Sun', 'size': 2, 'total_bill': 40.55, 'tip': 3.0},
                 {'day': 'Thur', 'size': 4, 'total_bill': 43.11, 'tip': 5.0},
                 {'day': 'Thur', 'size': 5, 'total_bill': 41.19, 'tip': 5.0},
                 {'day': 'Thur', 'size': 4, 'total_bill': 34.83, 'tip': 5.17}])
    result = df.groupby(['day'])[['size','total_bill', 'tip']].apply(func, args=('sub', 'div', 'sub', ))
    >>>result
                    size  total_bill       tip
    day                                    
    Fri  0   1.333333    1.249844  0.820000
         1  -0.666667    0.901369 -0.910000
         2  -0.666667    0.848787  0.090000
    Sat  3  -0.666667    1.034055  1.423333
         4   0.333333    0.983583  0.423333
         5   0.333333    0.982362 -1.846667
    Sun  6   2.333333    1.077870  1.166667
         7  -0.666667    1.014768 -0.333333
         8  -1.666667    0.907362 -0.833333
    Thur 9  -0.333333    1.085621 -0.056667
         10  0.666667    1.037270 -0.056667
         11 -0.333333    0.877109  0.113333
    """
    mean = x.mean()
    index = mean.index
    calculate_map = {'add': x.add(mean),
                     'sub': x.sub(mean),
                     'mul': x.mul(mean),
                     'div': x.div(mean)}
    return pd.concat([calculate_map.get(i)[index[num]] for num, i in enumerate(args)], axis=1)
```

函数中使用了聚合函数`mean`作为聚合结果，可以聚合的列名作为`mean`后的`index`，通过`args`传入的计算方式，提取`calculate_map`中对应方法，之后再查找`args`中各序号对应的`columns`（在`mean`结果中为`index`）,结果为传入的各个列名的`pd.Series`，再通过`pd.concat(axis=1)`，横向结合各个结果，返回`pd.DataFrame`对象。

（手动水印：原创CSDN宿者朽命，https://blog.csdn.net/weixin_46281427?spm=1011.2124.3001.5343 ，公众号A11Dot派)

## / 总结

本篇分享一个小小的函数，功能实现如题，灵感来源于近日看见需求及部分代码，很多代码片段简单，需求处理也不复杂的代码，在常用代码中却没有现成的，就需要自己构建新的函数，其过程是需要一番思考及试错的，在多番头脑风暴后，拨开云雾见青天，是可用之用也。

你总觉得山上树木丛生，路况复杂，蛇虫布地，缺忘记了天空是蓝色的，野花是鲜艳的。

---

<p align="right">于二零二二年三月十六日作</p>
