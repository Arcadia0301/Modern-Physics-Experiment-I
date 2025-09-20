import numpy as np

# 输入的四个文件名
files = ["No1_Pos170mm_Vac.txt", "No2_Pos170mm_Vac.txt", "No3_Pos170mm_Vac.txt", "No4_Pos170mm_Vac.txt"]

# 读取第一个文件
data = np.loadtxt(files[0], dtype=int)
col1 = data[:, 0]       # 第一列
col2_sum = data[:, 1]   # 第二列（初始化总和）

# 依次读取后面的文件并加上第二列
for fname in files[1:]:
    data = np.loadtxt(fname, dtype=int)
    col2_sum += data[:, 1]

# 合并成新的二维数组
result = np.column_stack((col1, col2_sum))

# 保存到新文件，整数格式
np.savetxt("Merged_Pos170mm_Vac.txt", result, fmt="%d", delimiter="\t")
