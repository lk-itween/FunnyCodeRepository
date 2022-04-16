# 拯救pandas计划（6）——多级分组并将次级条件转换为列名  

最近发现周围的很多小伙伴们都不太乐意使用pandas，转而投向其他的数据操作库，身为一个数据工作者，基本上是张口pandas，闭口pandas了，故而写下此系列以让更多的小伙伴们爱上pandas。

系列文章说明：

> 系列名（系列文章序号）——此次系列文章具体解决的需求

**平台：**

- windows 10
- python 3.8
- pandas >=1.2.4

## / 数据需求

需要将下列数据进行格式转换，对左图选中的两列作为条件进行分组并计数，之后再将第二列作为列名使结果成为新的数据框。  

```python
import pandas as pd

data = {"Name": ["Jack","Jack","Jason", "Jason","Rose","Rose"],
         "Course": ["Chinese","Chinese","Chinese","Russian","English","English"],
        "Date": ["20220112","20220113","20220112","20220114","20220112","20220113"]}
df = pd.DataFrame(data)
```
![](https://gitee.com/kangliz/pic-drawing-bed/raw/master/picture/pandas_save/pandas_save_6_1.png)  

## / 需求拆解

转换图中有需要将行转成列名，不由得想到使用`unstack`进行转换，`unstack`中传入参数为索引，只需要将被转换的列提至索引处就能完成。而对元素计数，使用`value_counts`或者`groupby`后再`count`都能进行计数并将对应列设置成索引。  

## / 需求处理

### 方法一

可以根据上述需求拆解中的方法进行数据处理，使用value_counts后再进行行转列操作。  

在value_counts中可以直接传入目标数据框的列名，这样就不用先索引提取所需列再进行操作了，结果是一个有多级索引的Series对象。  
![](https://gitee.com/kangliz/pic-drawing-bed/raw/master/picture/pandas_save/pandas_save_6_2.png)  
对结果中的`Course`索引做行转列操作，即使用`unstack`方法。原`Course` 列的列名为`Course`再转换后，其同样也还是作为该列的一个name属性值，如下图`df.columns`  
![](https://gitee.com/kangliz/pic-drawing-bed/raw/master/picture/pandas_save/pandas_save_6_3.png)

这一步完成后已经跟结果很接近了，其不同点就是`Name`列还是为索引并不是`values`属性值，这里可以先进行reset_index， 再重新设置columns，抑或最后两步步骤调换顺序也能生成结果样式。  
![](https://gitee.com/kangliz/pic-drawing-bed/raw/master/picture/pandas_save/pandas_save_6_4.png)

```python
df = df.value_counts(['Name', 'Course']).unstack('Course')
df.columns = df.columns.values
df.reset_index(inplace=True)
```

### 方法二

处理逻辑与方法一类似，使用`groupby`进行聚合计数再做行转列操作，最后重置索引更新列名。与一不同点在于需要对聚合后的具体列进行提取计数。  
![](https://gitee.com/kangliz/pic-drawing-bed/raw/master/picture/pandas_save/pandas_save_6_9.png)  
得出的结果和方法一一致，方便数据处理，将可链式调用的步骤结合，相同语句作用也不再赘述。    

（手动水印：原创CSDN宿者朽命，https://blog.csdn.net/weixin_46281427?spm=1011.2124.3001.5343 ，公众号A11Dot派)  
![](https://gitee.com/kangliz/pic-drawing-bed/raw/master/picture/pandas_save/pandas_save_6_5.png)

```python
df = df.groupby(['Name', 'Course'])['Course'].count().unstack('Course').reset_index()
df.columns = df.columns.values
```

### 方法三

列与列之间的数据求和计数，在`pandas`中也有一种类似于excel中的`数据透视表`，`交叉表`的操作，因数据透视表（pivot_table）在一次处理结果中会生成多层索引，其多层索引降级可以去[拯救pandas计划（1）——将一维数组转换为二维数组](https://blog.csdn.net/weixin_46281427/article/details/122344350)方法中找到处理方法。

- **pivot_table（数据透视表）:**  

```python
pd.pivot_table(df, index=['Name'], columns=['Course'], aggfunc='count')
```

![](https://gitee.com/kangliz/pic-drawing-bed/raw/master/picture/pandas_save/pandas_save_6_6.png)

- **crosstab（交叉表）:**    

包含的参数与`pivot_table`相差不大，但能更好的解决两列数据作笛卡尔变换的问题  
![](https://gitee.com/kangliz/pic-drawing-bed/raw/master/picture/pandas_save/pandas_save_6_7.png)  
只需要按照各参数的含义将所需处理的对象依次补充即可输出目标数据集，这个需要将`dropna`设置为`False`才能满足当前要求，否则会将`NaN`处理成 0。  
![](https://gitee.com/kangliz/pic-drawing-bed/raw/master/picture/pandas_save/pandas_save_6_8.png)  
接下的步骤想必都已经知道了，重置索引及更新列名。

```python
df = pd.crosstab(df['Name'], df['Course'], values=df['Course'], dropna=False, aggfunc='count')
df.columns = df.columns.values
df.reset_index(inplace=True)
```

## / 总结

本篇也是对`pandas`中一个小小的例子进行讲解，在众多方法都能解决同一个问题时，希望都能仔细斟酌，挑选一个更适合自己的方法才显得尤为重要，有些方法可能更符合当前所想的逻辑，而有些跳出了你思想的圈子，寻找到一种更直达结果的处理方式。  

话说雨过天晴，太阳更加的明亮。此时所处黑暗，阴冷，是让黎明的到来更有希望，万物都将会复苏。  

---

<p align="right">于二零二二年一月二十七日作</p>
