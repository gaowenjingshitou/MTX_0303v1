import pandas as pd
import  os
import re
files_右膝关节T1增强=os.listdir("C:\\Users\\Beth\\Downloads\\MTX\\MRI处理数据\\右膝关节T1增强")
# print(len(files))
Pat_Names_右膝关节T1增强=[]
for item in files_右膝关节T1增强:
    pattern = re.compile('[^\u4e00-\u9fa50-9]')  # 中文的编码范围是：\u4e00到\u9fa5
    zh =pattern.split(item)
    Chinese=zh[0]
    Pat_Names_右膝关节T1增强.append(Chinese)
print("右膝关节T1增强人数=",len(set(Pat_Names_右膝关节T1增强)))  #55

Pat_Names_右膝关节T1增强=pd.DataFrame(set(Pat_Names_右膝关节T1增强), columns=["Pat_Name"])
print(Pat_Names_右膝关节T1增强)

files_左膝关节T1增强=os.listdir("C:\\Users\\Beth\\Downloads\\MTX\\MRI处理数据\\左膝关节T1增强")
# print(len(files))
Pat_Names_左膝关节T1增强=[]
for item in files_左膝关节T1增强:
    pattern = re.compile('[^\u4e00-\u9fa50-9]')  # 中文的编码范围是：\u4e00到\u9fa5
    zh =pattern.split(item)
    Chinese=zh[0]
    Pat_Names_左膝关节T1增强.append(Chinese)
print("左膝关节T1增强=",len(set(Pat_Names_左膝关节T1增强)))  #41



Intersection=list(set(Pat_Names_左膝关节T1增强).intersection(set(Pat_Names_右膝关节T1增强["Pat_Name"])))
print("左右膝关节交集人数",len(Intersection))