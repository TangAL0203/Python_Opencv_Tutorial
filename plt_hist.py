#-*-coding:utf-8-*-
import matplotlib.pyplot as plt
fig = plt.figure()
ax = fig.add_subplot(111)

Each_Attr_num = {'Fabric': 152875,
                 'Part': 113792,
                 'Shape': 132263,
                 'Style': 107292,
                 'Texture': 111405}

# hist只能统计一个范围的数据，划分为bins个区间，各个区间的统计量的直方图
X = [1.4,2.2,3,3.8,4.6]
xgroup_labels = ['Fabric', 'Part', 'Shape', 'Style', 'Texture'] #x轴刻度的标识
plt.xticks(X, xgroup_labels, fontsize=18,fontweight='bold') #默认字体大小为10
n, bins, patches = ax.hist([[1]*152875, [2]*113792, [3]*132263, [4]*107292, [5]*111405], bins=5) # bins 区间个数

print(bins)
plt.title('Num of Five Attrs', fontsize=20)
plt.xlabel('Attr name', fontsize=20)
plt.ylabel('Num', fontsize=20)
plt.show()
