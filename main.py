import numpy as np
import matplotlib.pyplot as plt
from statsmodels.stats.diagnostic 
import acorr_ljungbox
np.random.seed(123)
white_noise=np.random.standard_normal(size=100)# 不再指定boxpierce参数，近返回QLB统计量检验结果
# 同时设置lags参数为一个列表，相应只返回对应延迟阶数的检验结果
res = acorr_ljungbox(white_noise, lags=[6,12,24], return_df=True)
print(res)