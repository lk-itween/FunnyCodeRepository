@[TOC](拯救pandas计划（2）——交换两列中不同的数据)

最近发现周围的很多小伙伴们都不太乐意使用pandas，转而投向其他的数据操作库，身为一个数据工作者，基本上是张口pandas，闭口pandas了，故而写下此系列以让更多的小伙伴们爱上pandas。  

系列文章说明：
> 系列名（系列文章序号）——此次系列文章具体解决的需求  

**平台：**  
- windows 10
- python 3.8
- pandas 1.2.4

## 数据需求  
这次简单的讲一讲一个小小的数据处理，如何将下图红框部分与蓝框部分数据进行交换。
![pic1](https://img-blog.csdnimg.cn/img_convert/6acd02f3f4232efcdc43025b98bc5106.png) 
## 需求拆解  
只是将两列的所有数据进行交换那还比较好处理，直接更改各自的列名就行了，现在是交换部分值，思路将一列值拿出来，用另一列进行填充，我们也不用别的方法，上pandas！  

##  构建数据
![pic2](https://img-blog.csdnimg.cn/img_convert/78480ad39fe6fecfc8badb5b6c176088.png)
## 需求处理  
### 方法一
随便找一列作为mask列，将不符合条件的索引变成True，就能通过布尔取值拿出想要的值。
```python
# map调用函数为自定义条件函数，在这里仅为示例
# 学历列包含数值型，需强转为str再进行自定义条件筛选
mask = df['学历'].astype(str).map(lambda x: '经验不限' in x or '年' in x or x.isdigit())

# 通过布尔提取交换两列数据
df.loc[mask, '经验'], df.loc[mask, '学历'] = df.loc[mask, '学历'], df.loc[mask, '经验']
```
![pic3](https://img-blog.csdnimg.cn/d5648c2ec4c34934bd001bd4bb15769e.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5a6_6ICF5py95ZG9,size_12,color_FFFFFF,t_70,g_se,x_16)
### 方法二
提到数据的索引交换就不得不把numpy也一起搬出来了。通过.values方法得到narray数组，再根据numpy的索引提取赋值给当前数据框。
```python
# mask已在上一步获得
df.loc[mask, ['学历', '经验']] = df.loc[mask, ['学历', '经验']].values[:,[1,0]]
```
可以看到也是可以成功交换的。  
 ![pic4](https://img-blog.csdnimg.cn/img_convert/de6cfb1622b95173c4d51ef3fd1e4226.png)
**ps:** 是不能直接将两列进行交换的
```python
df.loc[mask, ['经验', '学历']] = df.loc[mask, ['学历', '经验']]
```
 这行代码运行完会发现无事发生，其原理有点不太明白，可能是视图不能直接赋值吧。。。  

## 总结  
数据的获取难免会碰到与自己想法不一致的，在这里也是因为数据不在它本来所在的列中，需要进行数据的提取并重新赋值，而在python中直接使用两列进行交换即可，也得益于pandas的数据整合方法非常强大，节省时间来做其他更有意义的事。  

冬日的夜晚，星星也还在频频的眨眼，静谧的，祥和的，今晚也一定会有个好梦吧。  

---
<p align='right'>于二零二二年元月十二日作</p>
