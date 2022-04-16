# 拯救pandas计划（7）——对含金额标志的字符串列转换为浮点类型数据

最近发现周围的很多小伙伴们都不太乐意使用pandas，转而投向其他的数据操作库，身为一个数据工作者，基本上是张口pandas，闭口pandas了，故而写下此系列以让更多的小伙伴们爱上pandas。

系列文章说明：

> 系列名（系列文章序号）——此次系列文章具体解决的需求

**平台：**

- windows 10
- python 3.8
- pandas >=1.2.4  

## / 数据需求

数据结构如下（`price`列不含`nan`及其他不规范类型的字符串），将`price`列的美元符号`$`和`,`去除掉并转换成浮点类型。

![](https://gitee.com/kangliz/pic-drawing-bed/raw/master/picture/pandas_save/pandas_save_7_1.png)

## / 需求拆解

看到这种数据清洗需求，内心应该是有很多种方法去解决的，这里着重提下在`pandas`里几种常用手段。

## / 需求处理

### 方法一

在使用`pandas`前，先温习下用python自带函数及re模块处理此类需求，简要地使用两种方式。

- 使用两个string.replace方法  

```python
# 使用两个string.replace方法
data['price'] = [float(i.replace('$', '').replace(',', '')) for i in data['price']]
```

![](https://gitee.com/kangliz/pic-drawing-bed/raw/master/picture/pandas_save/pandas_save_7_2.png)

- 使用re模块  

```python
# re
import re

data['price'] = [float(re.sub(r'[$,]', '', i)) for i in data['price']]
```

结果同上，不再贴图展示。

（手动水印：原创CSDN宿者朽命，https://blog.csdn.net/weixin_46281427?spm=1011.2124.3001.5343 ，公众号A11Dot派)

### 方法二

`方法一`是没有用到任何pandas函数及方法，使用在pandas里使用列表生成式赋值给`pd.DataFrame()`总感觉差了点什么，哦，是`.map`方法：

- map调用函数  

*.replace.replace*

```python
# 使用map，可以链式调用其他pandas方法，如astype

data['price'].map(lambda x: x.replace('$', '').replace(',', '')).astype(float)
```

*re*

```python
# 也可以在map里调用re模块

data['price'].map(lambda x: re.sub(r'[$,]', '', x)).astype(float)
```

- 使用split函数切分字符串

既然知道`$`在最前面，且只使用`,`做千分位，可以尝试split结合strip函数进行字符串拆分，再join拆分后列表的字符串。

```python
# join拆分后的字符串完成数据清洗

data['price'].map(lambda x: ''.join(x.lstrip('$').split(','))).astype(float)
```

- str.split代替split

细看`price`列是一个dtype = 'object'类别的列，这样也能使用pandas中的`.str.split`方法。

![](https://gitee.com/kangliz/pic-drawing-bed/raw/master/picture/pandas_save/pandas_save_7_3.png)

```python
# .str.strip.str.split代替strip.split

data['price'].str.strip('$').str.split(',').map(lambda x: ''.join(x)).astype(float)
```

- str.replace  

前面水了这么多该请出这次的主角了。前面写的多多少少有点繁琐，或者没pandas那味了，本来想用pandas简化代码或者更好理解，这倒好更麻烦了，使用`.str.replace`就会舒服不少。

```python
# .str.replace, 使用正则表达式，需要加上regex=True

data['price'].str.replace(r'[$,]', '', regex=True).astype(float)
```

## / 总结

数据的处理或许理解方式不同处理的过程不同，不用去为了做到而去更改自己的代码习惯，或者是自己的逻辑习惯，这里罗列了部分解决方法，看起来都是比较容易理解的，只是对于pandas模块有了专属的方法替代，本篇虽短，仅仅提及了解决本次需求可以用到的几种，希望能对正在处理这类数据的你带来一点帮助。  

春雪夜入白草地，只影闲游孤鸟随。  

---

<p align="right">于二零二二年二月十二日作</p>
