import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimSun']
plt.rcParams['axes.unicode_minus'] = False

from matplotlib import rcParams

plt.rc('font', family='Times New Roman')
plt.rc('font', size=11)
# rcParams['mathtext.default'] = 'regular'
rcParams.update({'mathtext.fontset': 'stix'})   # 和上面二选一

plt.figure(figsize=(8, 5.5))

# 示例数据
data = pd.read_csv('C:/Users/fan/Desktop/data.csv')

for i in range(1, 13):
    plt.plot(data.iloc[:, 0], data.iloc[:, i], label=data.columns[i])
plt.title('$\mathrm{Nature}$系列期刊“含水率”', fontproperties='simsun')
plt.ylabel('“含水率”$\mathrm{(\%)}$', fontproperties='simsun')
plt.legend(ncol=1)

plt.figtext(0.08, 0.05, '数据来源：$\mathrm{Nature}$官网, 统计截止时间：$2024$年$12$月$29$日\n“含水率”定义：指发表在$Nature$系列期刊上, 水文学($Hydrology$)领域的文章占比', fontproperties='simsun')

plt.tight_layout(rect=[0, 0.1, 1, 1])
plt.show()
# plt.savefig('C:/Users/fan/Desktop/nature文章分析-绘图.png', dpi=300, bbox_inches='tight', pad_inches=0.02)
