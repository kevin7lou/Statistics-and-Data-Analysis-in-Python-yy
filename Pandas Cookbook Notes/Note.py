'''
快速检索：√ 表示未知的操作tricks；或低频的
'''
########### Note 1

# Jupyter 索引操作：
[目录下的标题名](#实际正文中的标题名)

pd.set_option('max_columns',8,'max_rows',10)
movie.get_dtype_counts()
Series.to_frame()

# 集合（字典）的运算：
&, |, +, -

# 选取列，用 df[''] 比df.column_name 可读性更分明；后者操作更便捷
 .quantile(.2)   等分
 .quantile([.2, .5, .7])

# 分布占比
director.value_counts(normalize=True)

# Series是否含缺失值
.hasnans	

# 链式方法，为了提升可读性，建议写成多行，若反斜杠换行比较麻烦，可以使用小括号包裹整个语句。
person.drive('store')\
      .buy('food')\
      .drive('home')\
      .prepare('food')\
      .cook('food')\
      .serve('food')\
      .eat('food')\
      .cleanup('dishes') 
# 链式也有缺点，比如debug很困难，难以追溯错在哪儿。
person1 = person.drive('store')
person2 = person1.buy('food')
person3 = person2.drive('home')
      
# 填充缺失值并转换数据类型：
data.fillna(0)\
    .astype(int)\
    .head()
    
# 缺失值统计：pandas将False／True 作0/1 计算
df.isnull()\
  .sum()    # 统计缺失值数量
df.isnull()\
  .mean()   # 统计缺失值占比


# 索引index操作
df.set_index('column_name',drop=True)
df.reset_index()  # Rangeindex

# 指定更改某个列名、行名
indexes_renamed = {'a':'b'} # a 改为b
columns_renamed = {'c': 'd'}
df.rename(index=indexes_renamed,
          columns=columns_renamed)
 
          
# 列的位置序号：
df.columns.get_loc('column_name')
df.insert() # 新增、插入某列



########### Chapter 2
#拿到一个数据集后，可能需要重新排“列”——离散、连续；含缺失、无缺失；数值、非数值；等等。
# 排列规则并无标准，比如：
# 1、区分一列是离散或连续  需要自己一个一个去看
# 2、在离散或连续列中，再细分组
# 3、 重要的组放前面，其中类别列放连续值列前面


# 选取多列——[[]]
# tuple 的逗号可省略：
#>>> tuple1 = 1,2,3,'a','b'
#>>> tuple2 = (1,2,3,'a','b')
#>>> tuple1 == tuple2
#     True

## .select_dtypes()
movie.get_type_counts()
movie.select_dtypes(include=['int'])
movie.select_dtypes(include=['number'])
movie.select_dtypes(include=['object'])

## .filter 只检查列名，不涉及具体的数据值
movie.filter(like='facebook',axis=0)
movie.filter(regex='\d', axis=0)



pd.option.display.max_rows = 10

movie.describe(percentiles=[.01, .3, .99])

movie.min(skipna=False)

# 参数axis=1，可以想象新增1列；axis=0,新增1行；
# 累计统计分析函数 可以减少for循环的使用
.cumsum(axis=1) #累加
.cumprob()
.cummin()
.cummax()

# 滚动计算（窗口计算）
 .rolling(w).sum() # 依次计算相邻w个元素的和
 .rolling(w).mean()
 .rolling(w).var()

 
pd.set_option('precision',n) # 显示时，保留小数位数
# 保留2位小数：地板除
df // 0.01 / 100

# 2个df是否一致，不能用==，因为NA无法比较，用df1.equals(df2)

################## Note 3

## 探索性数据分析EDA
数据可以分为连续型变量和类别型变量。连续型数据一定值数值型的，分类变量是离散型的。

###汇总统计：类别变量；转置操作；
df.describe(include=[np.object, pd.Categorical]).T  # 转置操作可以增强可读性，当列很多时

### Data Dictionaries很重要，合作必需。

## 改变数据类型，节省内存; 当列中含有一个string，pandas会强制该列为Object类行，其数值也会变成string
df[['col1','col2']].memory_usage(deep=True)        # 每列占用的内存;必须设置deep=True才能准确提取每个值的内存，尤其Object类型；
df['clo2'] = df['col2'].astype(np.int8)                 # 只有0/1 2个值的，可以转化为8-bit integer

### object -> categorical，当该列有比较低的基数(number of unique values)
df.select_dtypes(include=['object']).nunique()   # 查看唯一值的个数，< 1%可以考虑转换类型
                                                 #注：object类型不像其他数据类型，并不是列中的每个值都是同一类型；它像一个catchall，可能包罗各种类型。
df['col3'] = df['col3'].astype('category')

#注：Python3 采用Unicode编码，每个字符占4 bytes；Pandas 一列内存>100 bytes，则超出的每个字符占5 bytes
#注：如果某数值列含有缺失值，该列类型必是 float64; Integer 数据类型会自动变为 float，如果它有了缺失值，
#    也因此，无法 .astype(np.int8)——ValueError: Cannot convert non-finite value (NA or inf) to integer.
# RangeIndex 是占内存最小的数据类型，若变成Int64Index，内存需求放大巨多：
>>> df.index = pd.Int64Index(df.index)

## 选择A值top100的行，A值top100且B值button5 的行
df.nlargest(100,'A',keep=False)  # 但该参数可能有问题，可能未修复。
df.nlargest(100,'A').nsmallest(50,'B')

## 多级排列再筛选
df_sorted = df.sort_values(['A','B','C'],ascending=[False,True,False]).head()

# 累计更大值、累加、累乘
df['A'].cummax()
df['A'].cumsum()

########## Note 4
 ## 混用数值和labels进行切片，以前的版本可用.ix实现，现在的.iloc 或.loc 已无法实现：
 >>> df.loc[:5, 'A':'Z'] # 会报错
 >>> col_start = df.columns.get_loc('A')
 >>> col_end = df.columns.get_loc['Z'] + 1
 >>> df.iloc[:5, col_start:col_end] #先用.get_loc 将labels转换成integer，再用.iloc；
 >>> df.loc[:, 'A':'Z'][:5] # 虽然能用链式连用.loc .iloc 来实现，但非常不建议。简单的尚可。

## 加速计算：用.iat .at 代替 .iloc .loc 

 ## index 是字母，非数值的，排序后，能用.loc 按字母顺序切片，像查字典一样
>>> df = df.sort_index()
>>> df.loc['Ax': 'Az']
 # 可以用 df.index.is_monotonic_ 来检查是否顺排
 
 ########## Note 5
 # 方法运算.add, .sub 等比直接用+ - 的好处是，可以设置参数：
 a = pd.DataFrame(np.arange(20).reshape(4,5))
 b = pd.Series(np.arange(4))
 
 a.sub(b, 
       axis=0 # a - b 默认为axis=1
       fill_value= # 缺失值补齐
 
 
 (df['A'] > 100).mean()  # 计算 > 100 的值的占比 ，该方法错误。因为 >100的结果输出是True／False ，而A中本身含有会被当作False的NaN
 df['A'].dropna().gt(100).mean()   # 需要排除 Nan导致的False个数不准确
 
 ## 可以同时比较1个df中的2列：
 a = df[['A','B']].dropna()
(a['A'] > a['B']).mean()
 
 and: &
 or: |
 not: ~
 
 ## 多布尔条件筛选：条件另创建变量，再合并这些变量。代码更规范整洁
 criteria1 = df['A'] > 1
 criteria2 = df['B'] == 'abc'
 criteria3 = ((df['C'] < 100) | 
              (df['C'] > 200))
 
 criteria_final = criteria1 & criteria2 & criteria3
 criteria_final.head()
 df[criteria_final]
 
 cols = ['A','B','C']
 df.loc[criteria3, cols]
       
 criteria = df.nunique() == 2
 binary_cols = df.columns[criteria].tolist()
 
 ## Python中，非0整数、非空字符串、非空序列都可为布尔值True
 
 # 更快地检索：
 ## 按index检索 比布尔检索快3倍左右，但重置一列为index可能抵消。若不用重置index，可以考虑index检索。
 df[df['A'] == 'a']
 df2 = df.set_index('A')
 df2.loc['a']
 
 ## 当index唯一或顺排，index selection performance 大幅提升
 ## 原理：未排序且含有重复值时，pandas需要检验index的每个值以正确选择，排序后，pandas利用binary search 算法提高性能；
 ##      值唯一时，pandas通过hash table实现快速检索，每个索引坐标以近乎相同的耗时被查找，无论它的长度。
 df1
 df2 = df1.set_index('A')
 df2.index_is_monotonic     # 检查是否单调; is_unique 检查是否唯一
 df3 = df2.sort_index()     # index 排序
 
 %timeit df1[df1['A'] == 'z']
 %timeit df2.loc['z']
 %timeit df3.loc['z']
 
 ## 拼接多列，作为新索引
 df.index = df['Country'] + ', ' + df['city']
 df = df.sort_index()
 
 >>> %%timeit
 >>> crit1 = df['Country'] == 'China'
 >>> crit2 = df['City'] == 'Beijing'
 >>> df[crit1 & crit2]
 
 >>> %timeit df.loc['China, Beijing']    # 速度快1个量级
 
 ## √ 按百分位选择
 A = df['A'] # pd.Series
 df_summary = A.describe(percentiles=[.1, .9])
 upper_10 = A.loc['90%']  # 取得90%位的值
 lower_10 = A.loc['10%']  # 取得10%位的值
 criteria = (A > upper_10) | (A < lower_10)
 A_top_bottom_10 = A[criteria]
 
 A.plot(color='b', figsize=(12, 6)) # 折线图
 A_top_bottome_10.plot(marker='o', style=' ', ms=4, color='r') # √ 点图（不连线的折线图）；ms:marker_size; 在折线图的基础上，全出各折点
 
 xmin = criteria.index[0]
 xmax = criteria.index[-1]
 plt.hlines(y=[lower_10, upper_10], xmin=xmin, xmax=xmax, color='r')
 
 ## 一些相当于SQL where 的操作: 
   ## 主要是 .isin
      criteria = ~df.A.isin(df.A.value_counts().index[:5]) #排除top5
   ## 代码规范上：多个条件语句分别赋给多个变量名，再合成1个变量名：
      criteria_city = df['city'].isin(['Beijing', 'Shanghai', 'Hangzhou'])
      criteria_gender = df['gender'] == 'Female'
      criteria_age = (df['age'] >= 20) & (df['Age'] <= 40) # 或者 df.age.between(20,40)
      criteria_final = criteria_city & criteria_gender & criteria_age
      select_columns = ['city', 'gender', 'age']
      df.loc[criteria_final, select_columns]  # .loc[ , ]
   
   ## √ .query 当过滤条件很繁复时，Boolean Indexing 语法会很啰嗦。.query 方法可以精简代码及增强可读性，语法更像直白的英文表达。√
       # 注意：该方法仍在试验，也并不及布尔索引强大，不可用作production codes
      # 例： 
      employee = pd.read_csv('../data/employee.csv')
      depts = ['Houston Police Department-HPD', 'Houston Fire Department (HFD)']
      select_columns = ['UNIQUE_ID', 'DEPARTMENT', 'GENDER', 'BASE_SALARY']
      query_string = "DEPARTMENT not in @depts " \  # not in 和 @ 的使用  √
               "and GENDER == 'Female' " \      # 字符串值 用引号
               "and 80000 <= BASE_SALARY <= 120000"
        
      emp_filtered = employee.query(query_string)
      emp_filtered[select_columns].head()
       
  ## √ 变化率 pd.Sereise.pct_change()
     # 例：Amazon股价变化的分布
      amzn = pd.read_csv('../data/amzn_stock.csv', index_col='Date', parse_dates=['Date'])
      amzn_daily_return = amzn.Close.pct_change()
      aman_daily_return = amzn_daily_return.dropna()
      aman_daily_return.hist(bins=20)  # 画直方图
       # 每个observation的z-score，即距离均值 几个标准差：
      mea = amzn_daily_return.mean()
      st = amzn_daily_return.std()
      abs_z_score = amzn_daily_return.sub(mea).abs().div(st)
       # 分布返回1，2，3个标准差内的百分比（占比）√
      pcts = [abs_z_score.lt(i).mean() for i in range(1,4)] # .mean() 常用于比较运算后，计算(布尔值）的百分比，因为True=1,False=0
      print('{:.3f} fall within 1 standard deviation. '
            '{:.3f} fall within 2 standard deviation. '
            '{:.3f} fall within 3 standard deviation. '.foramt(*pcts)) # √ 格式化print ，扩展参数*
   ## √ .where 筛选符合条件的，同时保留不符合条件的值; 类比np.where。可用于异常值处理，去头掐尾找出大部分的非异常值，保留并replace异常值（而非删除）
       #例：
       movie = pd.read_csv('../data/movie.csv', index_col='movie_title')
       facebook_likes = movie['actor_1_facebook_likes'].dropna()
       facebook_likes.hist()                                             # 可看出分布很不均匀，基本全部数据分到一个bin里。
       criteria_high = facebook_likes < 20000                            # 筛选出 <20000 的
       criteria_high.mean()                                              # 占比90.8%（ True=1,False=0）
       facebook_likes.where(criteria_high).head()                        # √ where ，过滤出<20000的项；>=的，保留为Nan
       
       criteria_low = facebook_likes > 300
       facebook_likes_cap = facebook_likes.where(criteria_high, other=20000)\  # < 20000
                                   .where(criteria_low, 300)                   # and > 300 
       facebook_likes_cap.hist()                                         # 分布相对均匀了
       
    ## √ .clip 可用等价实现上面.where的效果，"裁剪、剪报、去头掐尾函数"
       facebook_likes_cap2 = facebook_likes.clip(lower=300, upper=20000)
       facebook_likes_cap2.equals(facebook_likes_cap)
       
    ## √ .mask 功能与where相反，顾名思义，用NaN 遮盖住不满足条件的数据，并不删除，前后的shape不变。
  
######### Note 6 面向index的操作
       # Indexes 支持集合操作，类似Python sets
       >>> df.columns   # 若加.values 返回ndarray，无以下集合操作
       Index(['a', 'b', 'c', 'd'], dtype='object')
       >>> columns = df.columns
       
       >>> c1 = columns[:3]
       >>> c1
       Index(['a', 'b', 'c'], dtype='object')
       
       >>> c2 = columns[2:]
       >>> c2
       Index(['c', 'd'], dtype='object')
       
       >>> c1.union(c2)                           # 并集
       Index(['a', 'b', 'c', 'd'], dtype='object')
       >>> c1 | c2
       Index(['a', 'b', 'c', 'd'], dtype='object')
       
       >>> c1.symmetric_difference(c2)             # 对称差分
       Index(['a', 'b', 'd'], dtype='object')
       >>> c1 ^ c2
       Index(['a', 'b', 'd'], dtype='object')
       >>> c1.difference(c2)             # 差集， in c1 and not in c2 
       
       # 检查某列是否含缺失值
       >>> df['A'].hasnans  
       False
       
       # 高亮显示缺失值部分
       df.style.highlight_null('yellow')# .style 只可用于小DataFrame，否认Jupyter 会崩溃。
       # 高亮显示最大值
       df.style.highlight_max(axis=) 
       
       # 将某列设为index，比如去重后索引乱序--.set_index()
       df = df.drop_duplicates(subset='column1')
       df = df.set_index('column1')
       
       # 将整列转换为数值类型  
       for col in cols:  # pd.to_numeric 只接受 list, tuple, 1-d array, or Series，不接受DataFrame。所以用for遍历，或用apply
           df[col]= pd.to_numeric(df[col],errors='coerce') # 参数使得非数值字符串转换为 Nan

######### Note 7 Grouping 
# 任何grouping 操作都有3部分组成：the grouping columns, aggregating columns, aggregating functions
#聚合，顾名思义，将多个值聚合为一个值
        
######### Note 7 Grouping 
df.groupby('A').B.mean()
df.groupby('A').B.agg('mean')
df.groupby('A').agg({'B':'mean'}) #√ 用传入字典，得到的是DataFrame，而非Series
df.groupby('A').agg({'B':'mean', 'C':'var', 'D':'idxmax'}) # √ 用agg能对多列采用多种不同的聚合方法（aggregation，或可用自定义函数）
       
# 可传入mean, min, max, median, sum, count, std, var, describe, size, nunique, idxmin, idxmax，包括一些np方法，如np.mean
# size 返回的是总行数数， count 则对非缺失值 计数

groupbyob = df.groupby('A')
dir(groupbyob) # 可用dir 探索DataFrameGroupby 对象
groupbyob.mean() # √ 若不加aggregating columns ，直接跟 aggregating method，则对'A'以外的所有列进行聚合。

# √ groupby之后，查看其中的某单个分组
groupbyob.head().head()     # 取每组的前5行组成一个DataFrame
groupbyob.nth([1,-1]).head() # 选取每组的第1行和最后1行（注意中间是逗号，选取的是指定行）
       
# 多列，多聚合函数同时操作
#例1:
>>> df.groupby(['A','B'])['C','D'].agg(['sum', 'mean']) # C,D 列 都做sum, mean 操作
     C            D
    sum mean    sum mean
A B      
a 1  20   55
  2  2    23
  3  44   64
       
# √ groupby后 ,通过多级index的元组进行切片     .loc[[('a',1),('b',1)]] 
       
 
# 例2:
>>>group_cols = ['A','B']   # 可以将操作的三个部分生成3个变量，增加可读性
>>>agg_dict = {'C': ['sum', 'mean', 'size'], # map specific agg_cols to specific agg_funs
               'D': ['mean', 'var']}         
>>>df.groupby(group_cols) \
     .agg(agg_dict)
    
# grouping 之后，删除（合并）多级（列）索引
# 例3:
>>>airline_info = flights.groupby(['AIRLINE', 'WEEKDAY'])\
                         .agg({'DIST':['sum', 'mean'], 
                               'ARR_DELAY':['min', 'max']}) \
                         .astype(int)     # √ 转换为整数
>>>level0 = airline_info.columns.get_level_values(0)   # √ 提取各级列索引
>>>level0
Index(['DIST', 'DIST', 'ARR_DELAY', 'ARR_DELAY'], dtype='object')
>>>level1 = airline_info.columns.get_level_values(1)
>>>level1
Index(['sum', 'mean', 'min', 'max'], dtype='object')
       
>>>airline_info.columns = level0 + '_' + level1  # √ 多级列索引合并
       
                DIST_sum	|DIST_mean	|ARR_DELAY_min	|ARR_DELAY_max
AIRLINE|	WEEKDAY				
AA	       1	      1455386	   1139	       -60	         551
          2	      1358256   	1107	       -52	         725
     
>>>airline_info.reset_index()    # √ 将多级索引压缩为 just a single level。通常保留会更直观。

# 例4: 
flights.groupby(['AIRLINE'], as_index=False)['DIST'].agg('mean').round(0) # √ group_cols 不作index；结果保留有效位数
      
# grouping 之后进行filter √ 低频
  # 类似标记每一行True or False 来进行筛选，我们也可以标记grouping之后的每个gruop，过滤掉为False的groups
grouped = college.groupby('STABBR')  # 首先 .groupby 再使用 .filter
grouped.ngroups  # 查看有多少个不同的group，类似df.nunique()
       
.filter 接收 自定义函数，传入的是 DataFrame，该函数必须返回 True or False。

注意：.groupby 之后调用.filter 完全不同于DataFrame.fitler
       
#√ groupby 有4个method 接受functions 来对其每段group进行运算操作。分别是agg, filter, transform, apply。
前3个都要求 functions返回特定的output:
       1. agg 必须返回一个scalar value
       2. filter 必须返回True or False
       3. transform 必须返回一列 Series
apply 最灵活，可替代agg 和transform;接受的函数可返回 a scaler, a Series, a DataFrame of any shape. #√ 低频
自定义函数均可搭配scipy、numpy 做科学计算，如几何平均数、调和平均数
       
# √ 低频。 grouping 之后 的.transform ，同一列，基于每组的所有数进行操作，接受自定义函数。比如算各组4个数，算基于各组（而不是整列）均值的z_score。
# 类似Series.map，只不过直接跟在grouopby 之后，更方便 
       
# √ 但是，上面的操作代价很高，这里仅有6w行，若数量更多，方法 .apply(,axis=1) 是Pandas中性能最差的操作之一。
Pandas 内部循环遍历每一行，没有采用任何numpy的加速措施。尽可能 avoid using apply with axis=1
   
#其它：
s = pd.Series([1, 1, 1, 0, 1, 1, 1, 0])
s.cumsum()
s.diff() # 当前值减去前一个值
s.where(lambda x: x<0)  # 不满足的 用nan填充
       
##################### My practices
 
 # 思想：Pandas 与Numpy的重要区别是，Pandas有索引，通过索引可以操作DataFrame的值。Numpy中不存在索引，所以所有操作必须通过维度来控制，相对复杂。
 #      Pandas通过索引，将对一组数据的使用，简化为对索引的使用。比如差集、交集、并集。算术运算根据行、列索引（补齐后）运算
       
# 直接读取zip、gz等压缩文件，而非先解压
df = pd.read_csv('filename.tar.gz', compression='gzip')
       
# 新增一行：
df.loc['行名']= 

# 查最大（小）值的索引——元素在列表中的索引（位置）
t = [1,2,3,4,5]
t.index(max(t))

s = pd.Series(t)
s.idxmax()  # √
s.idxmin()

# 例：查找每row中的最大值
  df.indmax(axis=1) # 进一步可用 .value_counts(normalize=True)
  

       
       
df['col'].argmax()

# 一列Series 或 index是否有单调性，即排过序，包括字母：
s.is_monotonic_decreasing or s.is_monotonic_increasing
 
 # Series 的.get操作
 s.get('f',100) # 若索引中没有'f'，则新增f，对应的值为100
       
 # 相关性分析，适用于Series, DataFrame
       .cor()  # 计算协方差矩阵
       .corr() # 计算相关系数矩阵，参数有Pearson、Spearman、Kendall等
   corr=df.corr()  # 计算变量（列）两两之间的（皮尔逊相关系数）
   threshold=corr[corr > 0.7].sum() -1  # 过滤相关系数 > 0.7的
   corv=threshold[threshold > 0.7]
   train[corv.index].corr()
 
# 文本处理
       .str.
  # 正则 √
       .apply(lambda x: len(re.findall('@.*雪', x))
    def find(x):
        pattern = re.compile(r'())
        results = pattern.search(x)
        if '雪碧' in results.groupdict()['name']
            return 1
        else:
            return 0
    df[x].apply(find)
                             
# 日期生成
index = pd.date_range('10/1/1999',periods=1100) # periods 是天数
                             
# np.where
df['C'] = np.where(df['A'] > df['B'], 'a','b')

# 文件太大，分块读取，分块遍历及运算
pd.read_csv( ,chunksize=100) # 每个chunk多少行，而不是分成多少个chunk
                             
# loc 布尔值检索、筛选 √
df.loc[[False, True]]
       
       
