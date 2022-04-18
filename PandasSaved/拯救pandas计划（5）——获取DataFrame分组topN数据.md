# 拯救pandas计划（5）——获取DataFrame分组topN数据

最近发现周围的很多小伙伴们都不太乐意使用pandas，转而投向其他的数据操作库，身为一个数据工作者，基本上是张口pandas，闭口pandas了，故而写下此系列以让更多的小伙伴们爱上pandas。  

系列文章说明：

> 系列名（系列文章序号）——此次系列文章具体解决的需求  

**平台：**  

- windows 10
- python 3.8
- pandas >=1.2.4  

## / 数据需求

现有一组数据，需要根据`name`进行分组，以`date_col`顺序排序，获取每组数据的前N项数据。  
![](https://gitee.com/kangliz/pic-drawing-bed/raw/master/picture/pandas_save/pandas_save_5_1.png)

为考虑比较各方案间的耗时，此次数据采用数据类别多量小的数据集。  
![](https://gitee.com/kangliz/pic-drawing-bed/raw/master/picture/pandas_save/pandas_save_5_2.png)

## / 需求拆解

整个数据框的前几行或者后几行都有相应的方法可以调用，如`head()`、`tail()`，分组后的前几行，只需要把整个数据框应用到`groupby`上再对各个分组进行`head()`即可，而这里需要取得topN，则分组后不一定能够按顺序取得，故而需要对数据框进行排序。

## / 需求处理

### 方法一

正如需求拆解里提到过的，使用groupby来完成这部分任务，在取得topN之前是需要对整个数据集进行排序的，这可以先尝试下在groupby之前排序，还是之后排序是否会对整个任务执行时间有影响。  
**先排序，后分组**  

```python
df.sort_values(['name', 'date_col'], inplace=True)
df.groupby(['name']).head(1)
```

![](https://gitee.com/kangliz/pic-drawing-bed/raw/master/picture/pandas_save/pandas_save_5_3.png)  

**先分组，后排序**  
由于groupby后面不能直接跟sort_values，所以需要调用`apply`来对每个分组进行排序。
![](https://gitee.com/kangliz/pic-drawing-bed/raw/master/picture/pandas_save/pandas_save_5_4.png)

分组后排序用时：

```python
df.groupby(['name']).apply(lambda x: x.sort_values('date_col').head(1)).reset_index(drop=True)
```

![](https://gitee.com/kangliz/pic-drawing-bed/raw/master/picture/pandas_save/pandas_save_5_5.png)  
看到这运行时间差了一个数量级，可能会怀疑是不是sort_values的问题，都知道`pandas`调用内部函数时运行效率还算是过的去，怎么在这差了这么多，直接在groupby后面运行head()仅200ms，这会可以看看在apply里调用head()。  
![](https://gitee.com/kangliz/pic-drawing-bed/raw/master/picture/pandas_save/pandas_save_5_6.png)  
在上图可以看出拖慢运行时间的主要原因不是sort_values，而是apply，虽然apply的工作机制方便了对数据框内的数据进行各种各样的处理操作，但当存在一种内部函数可以满足需求时再选择使用apply就会稍显鸡肋。  
（手动水印：原创CSDN宿者朽命，https://blog.csdn.net/weixin_46281427?spm=1011.2124.3001.5343 ，公众号A11Dot派）  
简言之，在这种方式处理上，先排序再分组取topN是能够较快的得到目标数据。  

### 方法二

在[拯救pandas计划（4）——DataFrame分组条件查找值](https://blog.csdn.net/weixin_46281427/article/details/122504615)中有提到过使用`drop_duplicates()`，同样在这里分组取topN也可以一试，但有限制条件，其`drop_duplicates()`内的`keep`参数决定了，仅能保留首个或尾个或者不保留重复数据。因此当只取top1时，可以试用此种方法，在处理时间上也过得去。

```python
df.sort_values(['name', 'date_col'], inplace=True)
df.drop_duplicates(['name'])  # 默认保留首个
```

![](https://gitee.com/kangliz/pic-drawing-bed/raw/master/picture/pandas_save/pandas_save_5_7.png)

### 方法三

虽然说有内部函数直接能达成结果的优先使用内部函数，但在这里不妨想一想如何在不使用`groupby`的方式求得分组topN。（可以先思考一会儿再继续往下看）

阐述下我的想法，仅做抛砖引玉之用，既然是分组取topN，不就是一种变相的分组排序，取排序靠前的值。以这样的思路，先对组中的每个类型进行计数，再编号即可取得。

- 计数：   

除了groupby外对类型进行计数还有一个好的方法，`value_counts`，这里需要将`sort`参数设置为False，避免内部排序影响外部排序，在计数前依然是先对整个数据框进行排序。

```python
df.sort_values(['name', 'date_col'], inplace=True)
name_count = df.value_counts('name', sort=False)
```

- 编号：

而后对`name_count`进行编号，使用`lambda`调用`range(x)`。

```python
name_count.map(lambda x: range(x))
```

![](https://gitee.com/kangliz/pic-drawing-bed/raw/master/picture/pandas_save/pandas_save_5_8.png)  
从生成的结果看来，`Series`中的`values`是一个可迭代序列，这种结果不能直接对原始数据框设置编号，取出`values`，使用`np.hstack`以行方向组合,对每个分组编号组合成一个一维数组。

```python
import numpy as np

df.sort_values(['name', 'date_col'], inplace=True)
np.hstack(df.value_counts('name', sort=False).map(lambda x: range(x)).values)
```

![](https://gitee.com/kangliz/pic-drawing-bed/raw/master/picture/pandas_save/pandas_save_5_9.png)  
ps: `values`中的每个值都是一维数组

- 取值：

再对生成的值与想要提取的topN的N进行对比，进行布尔索引提取即可得到想要的topN数据。运行结果如下，时间上也能接受：   
![](https://gitee.com/kangliz/pic-drawing-bed/raw/master/picture/pandas_save/pandas_save_5_10.png)  
以下是将这段代码进行封装成函数：

```python
import numpy as np
import pandas as pd


def get_data_top(data: pd.DataFrame, group_cols: list, val_cols: list, ascending: bool = True, k: int = 1):
    """
    自定义获取数据框topN
    :param data: pd.DataFrame类型
    :param group_cols: list, 需要聚合的列名
    :param val_cols: list, 需要排序的列名
    :param ascending: 排序方式，默认`True`，顺序排序，接收bool或这个列表里全部为bool的列表
    :param k: 取前k项值
    :return: 返回topN数据框
    """
    # 为了能返回传入数据框的原index，将index保存至values中
    datac = data.reset_index().copy()
    index_colname = datac.columns[0]
    # 对原数据框进行排序
    datac.sort_values(group_cols + val_cols, ascending=ascending, inplace=True)
    # 主要代码：分组对组内进行编号
    rank0 = np.hstack(datac.value_counts(group_cols, sort=False).map(lambda x: range(x)).values)
    # 取topN值
    datac = datac[rank0 < k]
    # 取出原index重置为index值
    datac.index = datac[index_colname].values
    # 删除额外生成的index值的列
    del datac[index_colname]
    return datac
```
  
ps: 参数冒号后的类型仅做提示，输入其他类型亦能入参，但需要传入正确参数及类型才能正常输出。

## / 总结

文中使用三种方法来取得数据集中的前N项值，过程上略有不同，总的结果呈现也基本相同，在想法及做法上对个人都一种提升。在写这篇之前，我一直在询问我自己，这篇值不值得写下来，把方法三删了改，改了删，起初并没有使用`numpy.hstack`，而是直接使用`list`强转range，偶然一次运行时发现运行时间竟然比groupby.head短，当时还窃窃自喜，复盘发现原来是我的把.head()运用在apply中，在方法一也有提到过这样做的耗时。经过几番修改，最终采用`np.hstack`组合编号，效率上能勉强达到方法一水平。  

在书本中，在年长者口中，常常有一种声音提醒我们现在站在了人生的十字路口，需要仔细思考，斟酌，推断这样做会有怎样的结果，但现在还需要磨蹭啥呢，未来不是推断出的未来，是创造的未来，敢于去想，敢于去做！  

----

<p align="right">于二零二二年元月二十四日作</p>
