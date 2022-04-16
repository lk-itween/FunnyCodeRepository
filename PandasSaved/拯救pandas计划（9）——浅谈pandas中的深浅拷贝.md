@[ToC](拯救pandas计划（9）——浅谈pandas中的深浅拷贝)

最近发现周围的很多小伙伴们都不太乐意使用pandas，转而投向其他的数据操作库，身为一个数据工作者，基本上是张口pandas，闭口pandas了，故而写下此系列以让更多的小伙伴们爱上pandas。

系列文章说明：

> 系列名（系列文章序号）——此次系列文章具体解决的需求

**平台：**

- windows 10
- python 3.8
- pandas >=1.2.4

## / 数据需求

有时在修改pandas对象中不想改变原数据框会使用.copy()给原数据框做一份拷贝，但数据内容中包含可变对象时，使用却不会按本意进行，官方也在函数中给出说明，这里一起了解下pandas中的深浅复制。

## / .copy(deep=True)

函数详解文档：

```markdown
Signature: df.copy(deep: 'bool_t' = True) -> 'FrameOrSeries'
Docstring:
Make a copy of this object's indices and data.

When ``deep=True`` (default), a new object will be created with a
copy of the calling object's data and indices. Modifications to
the data or indices of the copy will not be reflected in the
original object (see notes below).

When ``deep=False``, a new object will be created without copying
the calling object's data or index (only references to the data
and index are copied). Any changes to the data of the original
will be reflected in the shallow copy (and vice versa).

Parameters
----------
deep : bool, default True
    Make a deep copy, including a copy of the data and the indices.
    With ``deep=False`` neither the indices nor the data are copied.

Returns
-------
copy : Series or DataFrame
    Object type matches caller.

Notes
-----
When ``deep=True``, data is copied but actual Python objects
will not be copied recursively, only the reference to the object.
This is in contrast to `copy.deepcopy` in the Standard Library,
which recursively copies object data (see examples below).

While ``Index`` objects are copied when ``deep=True``, the underlying
numpy array is not copied for performance reasons. Since ``Index`` is
immutable, the underlying data can be safely shared and a copy
is not needed.
```

在该函数文档中可以看出，默认为深复制(deep=True)，会创建一个与原数据框不同的数据对象，在副本中修改数据均不会使原数据发生修改，在下面的`Notes`部分提到，如果数据内容是可变对象依然会改变原数据框内容，原因是pandas的深复制仅是引用python对象使用，也有部分减少性能的消耗，如`Index`不可变对象可以安全无误的复制到新对象中，不同于`copy.deepcopy`会递归复制python对象，所以使用`pandas.copy`复制pandas对象，如果数据内容包含可变对象，仍然是不安全的，修改其内的数据会使原数据发生改变。

（手动水印：原创CSDN宿者朽命，https://blog.csdn.net/weixin_46281427?spm=1011.2124.3001.5343，公众号A11Dot派)

## / 函数使用

- 数据:

```python
import pandas as pd

data = {'A': [1, 2, 3],
 'B': [['厉害', '真棒'], ['值得鼓励', '继续加油'], ['相信未来--勇闯天涯']],
 'C': [{'key': '试一试', 'value': 'try'}, {'key': '看一看', 'value': 'look'}, {'key': '拍一拍', 'value': 'tickle'}]}
df = pd.DataFrame(data)
df_shallow = df.copy(deep=False) # 浅复制
df_copy = df.copy() # 深复制
```

![](https://gitee.com/kangliz/pic-drawing-bed/raw/master/picture/wuxiu/pandas_9_2.png)

生成df，包含3列数据，A列为数值型，不可变对象， B和C都是可变对象。

![](https://gitee.com/kangliz/pic-drawing-bed/raw/master/picture/wuxiu/pandas_9_1.png)

查看深浅复制对象，都与原对象不同，说明完成拷贝。

- 修改df中的A列数据

```python
df.loc[0, 'A'] = 50
```

![](https://gitee.com/kangliz/pic-drawing-bed/raw/master/picture/wuxiu/pandas_9_3.png)

**df_shallow**会跟着df的改变而发生改变，而**df_copy**不会发生变化，也证实了`df.copy(deep=False)`是浅层复制，新建了一个与**df**数据内容及索引相同的但对象不同的数据框。

- 修改B列数据

```python
df.loc[0, 'B'][0] = 'lihai'
```

![](https://gitee.com/kangliz/pic-drawing-bed/raw/master/picture/wuxiu/pandas_9_4.png)

在B列修改过程中所有复制出来的数据框都发生了变化，正如`Notes`所说，是对对象的引用，是直接修改引用到的数据，那么在数据框显示部分看到B列的内容发生变化，原始数据内容是否也已经改变，打印data：

![](https://gitee.com/kangliz/pic-drawing-bed/raw/master/picture/wuxiu/pandas_9_5.png)

data中的B所对应的值也已经发生改变，那么有什么方法可以仅改变深复制后的数据对象，又不改变原始数据，这里需要借助copy模块，C列的数据层次与B列一样，下面修改C列数据。

- 修改C列数据

```python
from copy import copy, deepcopy

def value_upper(dic):
    """将传入的dic使用深浅拷贝复制给另一个新的对象"""
    dic = copy(dic)  # 如果层级大于一层，请考虑使用deepcopy
    dic['value'] = dic['value'].upper()
    # 返回修改后的字典对象
    return dic

df_copy['C'].apply(value_upper)  # 未实际改变df_copy['C']
```

![](https://gitee.com/kangliz/pic-drawing-bed/raw/master/picture/wuxiu/pandas_9_6.png)

熟悉pandas的会明白这样仅让df_copy中的C列参与了函数执行，没有实际改变C列数据，但如果没有第5行中的copy操作，即使没有return语句也会使df_copy发生改变，原因见修改B列数据部分。如果需要改变C列数据将运行后的结果赋值给C列，由于C列被重新赋值也就不存在修改df_copy中C列数据会影响到df或df_shallow乃至data中的C列数据。

```python
df_copy['C'] = df_copy['C'].apply(value_upper) 
```

![](https://gitee.com/kangliz/pic-drawing-bed/raw/master/picture/wuxiu/pandas_9_7.png)

可以看到仅df_copy['C']发生了变化。

## / 总结

偶尔修改pandas对象中的数据时会被提醒所修改的数据视图会影响原数据框，可以考虑使用`df.copy`方法避免修改，而当数据中含有可变对象，且只修改其中的一部分内容，却不会产生这样的警告，而这样的结果又不能被接受时，可以查看下函数文档，`pandas`中的copy与python对象的复制在使用上有部分不同，例如`deepcopy`是会对python进行递归操作，而`pandas.copy`仅将数据引用及索引进行复制。如果你问我`deepcopy(df)`是否可以避免上述情况发生，很遗憾的告诉你不行，对该篇有任何疑问欢迎联系作者，简述你的见解。

当你难以分辨两者之间是否有某种关联时，最好的办法是改变其中一个的特征。

---

<p align="right">于二〇二二年三月二十日作</p>
