@[ToC](拯救pandas计划（4）——DataFrame分组条件查找值)

最近发现周围的很多小伙伴们都不太乐意使用pandas，转而投向其他的数据操作库，身为一个数据工作者，基本上是张口pandas，闭口pandas了，故而写下此系列以让更多的小伙伴们爱上pandas。  

系列文章说明：

> 系列名（系列文章序号）——此次系列文章具体解决的需求  

**平台：**  

- windows 10
- python 3.8
- pandas >=1.2.4  

## / 数据需求

依据各个用户的判断标签，且按照【甲乙丙丁……】依次排序，取得每个用户优先级最高的数据，其他标签列保留。如下图所示：

![](https://gitee.com/kangliz/pic-drawing-bed/raw/master/picture/pandas_save/pandas_save_4_1.png)

## / 需求拆解

既然是对每个用户进行判断标签优先级的提取，则可以对每个用户进行一个分组，在组内进行数据查找，下面给出两种我的实现方法。  

## / 需求处理

### 方法一：

由于只有示例中只有一列其他标签，这里可以简单处理，如有不需要处理的列数较多，可以发挥想象是否能按照此方法进行提取。首先处理其他标签值，这里给它用列表包裹起来。

```python
df['其他标签'] = df['其他标签'].map(lambda x: [x])
```

![](https://gitee.com/kangliz/pic-drawing-bed/raw/master/picture/pandas_save/pandas_save_4_2.png)  

再按每用户每判断标签进行聚合，在上一步把其他标签处理成`list`类型，间接的方便了这里的聚合，使用`sum`对列表进行累加。

```python
df = df.groupby(['用户', '判断标签'], as_index=False)['其他标签'].sum()
```

![](https://gitee.com/kangliz/pic-drawing-bed/raw/master/picture/pandas_save/pandas_save_4_3.png)  

之后对判断标签进行排序，这里说明下，早期pandas包的`.sort_values`没有`key`参数，需要自行升级包才能使用，在没有key参数之前对列进行自定义排序是一件比较麻烦的事，需要生成类别序列在该列上，这里只需要将每种类型用字典的形式，规范化各类别的顺序，通过`key`参数，调用`map`函数即可简单且快速的自定义列排序。

```python
df.sort_values('判断标签', key=lambda x: x.map({'甲': 1, '乙': 2, '丙': 3, '丁': 4}), inplace=True)
```

![](https://gitee.com/kangliz/pic-drawing-bed/raw/master/picture/pandas_save/pandas_save_4_4.png)

可以注意到，每用户每判断类型只有一行，顺序升序，这里只取优先级较高的判断标签，可以使用去重函数，保留第一次出现的行即可

```python
df.drop_duplicates('用户', inplace=True)
```

![](https://gitee.com/kangliz/pic-drawing-bed/raw/master/picture/pandas_save/pandas_save_4_5.png)

现在离我们的目标还差一步之遥，唯一的区别就是其他标签是`list`类型，最后使用`explode`方法，单行生成多行的方式处理成目标形式。

```python
df.explode('其他标签')
```

![](https://gitee.com/kangliz/pic-drawing-bed/raw/master/picture/pandas_save/pandas_save_4_6.png)
大功告成！

### 方法二：

文章开头提到过，既然是分组取优先级最高的值，那么不妨直接用groupby分组各用户，再对组内进行优先值查找。

```python
def get_first_label(data):
    """判断并获取每一个分组内标签排序最上的值"""
    return data[data['判断标签'] == data.head(1)['判断标签'].values[0]]

# 可先对判断标签进行排序，再groupby分组
df.sort_values('判断标签', key=lambda x: x.map({'甲': 1, '乙': 2, '丙': 3, '丁': 4}), inplace=True)
df.groupby(['用户']).apply(get_first_label).reset_index(drop=True)
```

结果：
![](https://gitee.com/kangliz/pic-drawing-bed/raw/master/picture/pandas_save/pandas_save_4_7.png)

## / 总结

分组查找也是在数据处理中比较常见的需求了，这里也仅仅是提供两种自己的浅显之见，其方法二，虽然看似代码行数少，但在执行效率上相比方法一略有逊色，当数据量增大时，每次groupby.apply调用函数会比较吃力，而方法一虽也有groupby，但是调用的是内部函数，且处理比较简单，自然会快一点，而作为去重，drop_duplicates当然是一把好手，该怎么处理数据还是看需求量及心情如何。  

明日的太阳依旧升起，明天的我们也是大放光彩。  

--- 

<p align="right">于二零二二年元月十四作</p>
