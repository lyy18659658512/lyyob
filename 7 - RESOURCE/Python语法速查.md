> [!example]- 字符串语法
>
> ```python
> "str".title()                             # 单词首字母改为大写
> "str".upper()                             # 单词全大写
> "str".lower()                             # 单词全小写
> "\n"                                      # 换行符
> "\t"                                      # 制表符
> "str".rstrip()                            # 删除字符串右端多余的空白
> "str".lstrip()                            # 删除字符串左端多余的空白
> "str".strip()                             # 删除字符串两端多余的空白
> "str".removeprefix('前缀')                # 删除字符串前缀
> "str".removesuffix('后缀')                # 删除字符串后缀
> f'字符串{变量}'                            # f-string 格式化
> ```

> [!example]- 列表语法
>
> ```python
> list[0] / list[-1]                        # 返回列表第一个、最后一个元素
> list[n]=x                                 # 修改列表任意位置的元素
> list.append('元素')                       # 列表末尾添加元素
> list.insert(n,'元素')                     # 列表任意位置插入元素
> del list[n]                               # 删除列表任意位置的元素，删除后无法访问
> list.pop()                                # 删除列表末尾的元素，可以访问
> list.pop(n)                               # 删除列表任意位置的元素，可以访问
> list.remove('元素')                       # 删除列表指定元素，已知想删除元素的值，不知道位置，可以访问（只会删除第一个指定的元素）
> list.sort()                               # 列表按特定顺序显示列表元素，永久改变列表中的排列顺序，sort()表示按字母顺序，sort（reverse=Ture）表示按字母相反顺序
> sorted(list)                              # 列表按特定的顺序显示元素，保留列表中的排列顺序,sorted(list) 表示按字母顺序，sorted(list,reverse=Ture) 表示按字母相反顺序
> list.reverse()                            # 反转列表元素的排列顺序，永久改变列表中的排列顺序
> len(list)                                 # 确定列表的长度，返回数值
> for value in list :                       # 循环遍历列表，将元素赋值给变量value
> for value in range(1,5) :                # 循环数字1-4，赋值给变量value
> list(range(1,6))                          # 创建数值列表[1,2,3,4,5]
> list(range(2,11,2))                       # 创建数值列表，从2开始，不断加2，直到达到或超过终值11，[2,4,6,8,10]
> [关于变量的表达式 for 变量 in range(1,11)]  # 列表推导式
> list[0:3]，list[:4],list[-3:]             # 列表切片，处理列表部分元素
> list[:]                                   # 复制生成列表，此列表与原列表无关联，如果没有[:]会生成一个相关联的列表
> (元素1, 元素2, 元素3)                     # 元组，同列表一样索引访问，元素不可修改，但可以重新定义元组，即给表示元组的变量赋值
> ```

> [!example]- IF 语句
>
> ```python
> if 表达式:                                 # 判断表达式的值为 True或False来决定是否执行if语句中的代码
> if 表达式:  else:                          # 条件未通过执行else后面的代码
> if 表达式:  elif 表达式:  else:            # 依次检查每个条件，条件满足后执行紧跟在它后面的代码，跳过余下的条件测试
> 判断是否相等用 ==，是否不等用 !=
> 判断多个条件表达式用and或or相连
> if 元素 in list:                           # 判断元素是否在列表中，是否不在列表中用 not in
> ```
>
> 注意事项：
> - 可以有多个elif,可以省略else代码块
> - 在每个条件为TURE时都需执行其后的代码时，需要用多个不包含elif和else代码块的if语句，而不能用if -elif-else

> [!example]- 字典
>
> ```python
> {'key_1':value_1,'key_2':value_2}         # 字典 ，一系列键值对
> dict['key']                                # 访问字典，返回字典中某个键关联的值
> dict['key']=value                          # 添加键值对，会保留定义时的顺序，也可以用来修改字典中的值
> del dict['key']                            # 删除键值对
> dict.get('key',value)                      # 访问字典中的值，如果不存在则返回value，如果没有value，则返回值None
> for k,v in dict.items():                   # 遍历字典，依次将每个键值对分别赋值给变量k和v
> for k in dict.keys():                      # 遍历字典中的所有键，依次将它们赋值给变量k,可省略.key()
> for v in dict.values():                    # 遍历字典中的所有值，一次将它们赋值给变量v
> set(dict.values())                         # 提取列表中不同的元素，生成一个没有重复元素的列表
> ```
>
> 注：`key()`并非只用于遍历，使用的同时会返回一个列表，其中包含字典中所有的键，即可用`dict.keys()`表示一个列表

> [!example]- 用户输入 & while 循环
>
> ```python
> input()                                    # 用户输出解读为字符串
> int(x)                                     # 将输入的字符串转化为数值
> 10 % 3                                     # 求模运算符号，将两个数相除返回余数，可根据返回值判断奇数、偶数、是否整除
> x += value                                 # A=A + value的简写
> while 表达式:                              # 循环不断运行，直到指定条件不满足退出循环
> while 标志:                                # 循环不断运行，直到标志=False退出循环
> while 列表:                                # 循环不断运行，直到列表为空退出循环
> break                                      # 循环不断运行，直到遇到break语句退出循环，break语句也可用来退出遍历循环For
> continue                                   # 忽略余下的代码，返回循环开头
> ```
