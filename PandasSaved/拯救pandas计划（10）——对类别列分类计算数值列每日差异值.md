@[ToC](拯救pandas计划（10）——对类别列分类计算数值列每日差异值)

最近发现周围的很多小伙伴们都不太乐意使用pandas，转而投向其他的数据操作库，身为一个数据工作者，基本上是张口pandas，闭口pandas了，故而写下此系列以让更多的小伙伴们爱上pandas。

系列文章说明：

> 系列名（系列文章序号）——此次系列文章具体解决的需求

**平台：**

- windows 10
- python 3.8
- pandas >=1.2.4

## / 数据需求

现有一组数据，包含类别列，日期列，以及其他需要进行差异值计算的数值列，如计算苹果在2022-01-02卖出的数量比2022-01-01卖出的数量多了多少。

![](https://gitee.com/kangliz/pic-drawing-bed/raw/master/picture/pandas_save/pandas_save_10_1.png)

## / 需求拆解

看到需要对每个类型进行分组求值，那么首先需要将各类型进行分类，然后对各个类型进行求值就能够完成需求。

## / 需求处理

使用for循环再对类型进行索引取值，再求出差异值这里不做描述，在pandas里有个函数`groupby`可以很有效的将每个类型分隔开，返回时将所有结果进行聚合，非常适合该需求

- 方法一

```python
# groupby.apply(lambda x: x.diff())
# 在聚合后的返回值是对类型，日期升序排序，所以在groupby之前先对data数据进行排序
# 这样在返回值添加到data后就不会造成数据错位

data.sort_values(['类型', '日期'], inplace=True)
data[['进货diff', '卖出diff']] = data.groupby(['类型']).apply(lambda x: x[['进货总量', '卖出总量']].diff()).values
```

![](https://gitee.com/kangliz/pic-drawing-bed/raw/master/picture/pandas_save/pandas_save_10_2.png)

可以看到每个类型的首日和其他日期计算的结果是正确的。

- 方法二

```python
# groupby.diff
# 对groupby后的结果直接进行索引要计算的列再调用diff方法

data.sort_values(['类型', '日期'], inplace=True)
data[['进货diff', '卖出diff']] = data.groupby(['类型'])[['进货总量', '卖出总量']].diff()
```

![](https://gitee.com/kangliz/pic-drawing-bed/raw/master/picture/pandas_save/pandas_save_10_3.png)

得出的结果与方法一是一样的。

- 方法三

```python
# groupby.transform # 返回与原始对象具有相同索引的数据帧
# 所以使用这种方法可以不用对原数据框进行排序再聚合

data[['进货diff', '卖出diff']] = data.groupby(['类型']).transform(lambda x: x.diff())[['进货总量', '卖出总量']]
```

![](https://gitee.com/kangliz/pic-drawing-bed/raw/master/picture/pandas_save/pandas_save_10_4.png)
