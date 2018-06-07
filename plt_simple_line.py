# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np

"""
2D图折现图，带图例，加格点。 
"""

plt.rcParams['font.sans-serif']=['Arial']  #如果要显示中文字体，则在此处设为：SimHei
plt.rcParams['axes.unicode_minus']=False  #显示负号

Y = np.array([[[1],[2],[2],[1],[5]], 
             [[3],[5],[2],[4],[2]]])

X = np.array(range(1,6,1))

#label在图示(legend)中显示。若为数学公式，则最好在字符串前后添加"$"符号
#color：b:blue、g:green、r:red、c:cyan、m:magenta、y:yellow、k:black、w:white、、、
#线型：-  --   -.  :    ， 
#marker：.  ，   o   v    <    *    +    1
plt.figure(figsize=(5,5))
plt.grid(linestyle = "--")      #设置背景网格线为虚线
ax = plt.gca()

xgroup_labels = [str(i) for i in range(1,6,1)] #x轴刻度的标识
plt.xticks(X, xgroup_labels, fontsize=18,fontweight='bold') #默认字体大小为10

# 画折现图
plt.plot(X, Y[0],color="cyan",label="ALL",linewidth=2.5)
plt.plot(X, Y[1],color="blue",label="Shape",linewidth=2.5)


plt.title("Y Vs X",fontsize=20,fontweight='bold')    #默认字体大小为12
plt.xlabel("ylabel",fontsize=20,fontweight='bold')
plt.ylabel("xlabel",fontsize=20,fontweight='bold')

plt.legend()          #显示各曲线的图例
plt.legend(loc=4,numpoints=1)
leg = plt.gca().get_legend()
ltext = leg.get_texts()
plt.setp(ltext,fontsize=8,fontweight='bold') #设置图例字体的大小和粗细

plt.show()
