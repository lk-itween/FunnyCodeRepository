# 拯救pandas计划（10）——对类别列分类计算数值列上下行差异值

最近发现周围的很多小伙伴们都不太乐意使用pandas，转而投向其他的数据操作库，身为一个数据工作者，基本上是张口pandas，闭口pandas了，故而写下此系列以让更多的小伙伴们爱上pandas。

系列文章说明：

> 系列名（系列文章序号）——此次系列文章具体解决的需求

**平台：**

- windows 10
- python 3.8
- pandas >=1.2.4

## / 数据需求

现有一组数据，包含类别列，日期列，以及其他需要进行差异值计算的数值列，如计算苹果在**2022-01-02**卖出的数量比**2022-01-01**卖出的数量多了多少。

![](https://gitee.com/kangliz/pic-drawing-bed/raw/master/picture/pandas_save/pandas_save_10_1.png)

## / 需求拆解

需要对每个类型进行分组求值，那么首先需要将各类型进行分类，然后再对各个类型进行求值就能够完成需求。

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

- 方法四

除上述简单明了的方法之外，还写了一个另类的求值方法。

```python
import numpy as np
import pandas as pd

def get_data_diff(data: pd.DataFrame, group_cols: list, val_cols: list, diff_cols: list, ascending: bool = True):
    """
    自定义获取数据框的diff
    :param data: pd.DataFrame类型
    :param group_cols: list, 需要聚合的列名
    :param val_cols: list, 需要排序的列名
    :param diff_cols: list, 需要计算diff的列名
    :param ascending: 排序方式，默认`True`，顺序排序，接收bool或这个列表里全部为bool的列表
    :return: 返回含diff的数据框
    """
    # 为了能返回传入数据框的原index，将index保存至values中
    datac = data.reset_index().copy()
    index_colname = datac.columns[0]
    # 对原数据框进行排序
    datac.sort_values(group_cols + val_cols, ascending=ascending, inplace=True)
    # 求diff
    datac[[f'{i}_diff' for i in diff_cols]] = datac[diff_cols].diff()
    # 主要代码：分组对组内进行编号
    rank0 = np.hstack(datac.value_counts(group_cols, sort=False).map(lambda x: range(x)).values)
    # 将每个类别的首个值用np.nan代替
    datac.loc[rank0 == 0, [f'{i}_diff' for i in diff_cols]] = np.nan
    # 取出原index重置为index值
    datac.index = datac[index_colname].values
    # 删除额外生成的index值的列
    del datac[index_colname]
    return datac

get_data_diff(df, ['类型'], ['日期'], ['进货总量', '卖出总量'])
```

使用这个自拟的函数也可以达成目标。

（手动水印：原创CSDN宿者朽命，https://blog.csdn.net/weixin_46281427?spm=1011.2124.3001.5343 ，公众号A11Dot派)

## / 总结

依赖pandas对行之间进行差异值计算(`diff`)也是非常方便的，如果需要分类计算只需要在diff前调用groupby方法就能完成需求，在之前的几篇中有提到过groupby后面接apply，若apply调用的是自定义函数，如匿名函数，会使计算时间延长，为了能较快的得出结果，可尽量使用已定义好的方法。

久旱逢甘露，滴水当涌泉。

---

<p align="right">于二零二二年三月三十日作</p>
