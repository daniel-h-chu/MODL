import Functions as Fx
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import os
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import scipy
from scipy.stats.stats import pearsonr
import warnings
from sklearn.metrics import r2_score
warnings.filterwarnings("ignore")

planned = pd.read_excel(Fx.include('EIA-NaturalGasPipelineProjects.xlsx'), header=1, sheet_name=[1,2])

planned[2]['Capacity'] = planned[2]['Additional Capacity (MMcf/d)']
pipelines = pd.concat([planned[1], planned[2]])
pipelines = pipelines.drop(index = 65)
pipelines = pipelines.drop(index = 596)
try:
    pipelines['Cost'] = pipelines['Cost (millions)'].astype(float)
except ValueError:
    pipelines['Cost'] = None

pipelines = pipelines.loc[:,['Capacity', 'Completed Date', 'Cost', 'Miles', 'Project Type']]
pipelines['Completed Date'] = pd.to_datetime(pipelines['Completed Date'])
pipelines = pipelines.sort_values('Completed Date')
pipelines_withoutdate = pipelines.dropna(subset = ['Completed Date', 'Cost'])
'''plt.plot(pipelines_withoutdate['Completed Date'] - pd.datetime(1970,1,1), pipelines_withoutdate['Cost'], 'o')
plt.semilogy()
plt.show()'''


pipelines_withoutdate['Number Date'] = (pipelines_withoutdate['Completed Date'] - pd.datetime(1970,1,1)).apply(lambda x: x.total_seconds())
X = np.array(pipelines_withoutdate['Number Date'] / 31557600)
Y = np.array(pipelines_withoutdate['Cost'])
X = np.reshape(X, (-1, 1))
reg = LinearRegression().fit(X, Y)
print('Score1: ' + str(reg.score(X, Y)))
print('Coef1: ' + str(reg.coef_))

pipelines_reg = pipelines.dropna(axis=0)
pipelines_reg = pipelines_reg.loc[(pipelines_reg!=0).any(1)]
'''max_exp = [0,0]
max_r = 0
for cost_exp in np.arange(-2,2,.22):
    #for cap_exp in np.arange(-1, -.3, .1):
    for mile_exp in np.arange(-2, 2, .22):
        print(cost_exp, mile_exp)
        pipelines_reg['Y'] = abs(pipelines_reg['Capacity'])**(-1*cost_exp) * abs(pipelines_reg['Cost'])**cost_exp
        pipelines_reg['X'] = abs(pipelines_reg['Miles'])**mile_exp
        pipelines_reg_temp = pipelines_reg.replace([np.inf, -np.inf], np.nan)
        pipelines_reg_temp = pipelines_reg_temp.dropna(subset=["X", "Y"], axis=0)
        X = np.array(pipelines_reg_temp['X'])
        Y = np.array(pipelines_reg_temp['Y'])
        r2s = 0
        for i in range(50):
            X_Train, X_Test, Y_Train, Y_Test = train_test_split(X, Y, test_size=.3, random_state=i+100)
            X_Train = np.reshape(X_Train, (-1, 1))
            X_Test = np.reshape(X_Test, (-1, 1))
            reg = LinearRegression().fit(X_Train, Y_Train)
            Y_Pred = reg.predict(X_Test)
            r2s += r2_score(Y_Test, Y_Pred)/50
        if r2s > max_r:
            max_exp = [cost_exp,  mile_exp]
            max_r = r2s
print(max_exp)
print(max_r)'''

pipelines_reg['Cost/Capacity'] = abs(pipelines_reg['Cost'])/abs(pipelines_reg['Capacity'])
pipelines_reg['Miles2'] = abs(pipelines_reg['Miles'])
Y3 = np.array(pipelines_reg['Cost/Capacity'])
X3 = np.array(pipelines_reg['Miles2'])
plt.plot(X3, Y3, 'o')
plt.show()
print(X3)
print(Y3)

plt.show()
intercept = []
coef = []
def geo_mean(iterable):
    a = np.array(iterable)
    return a.prod()**(1.0/len(a))



r2s = 0
for i in range(100):
    X3_Train, X3_Test, Y3_Train, Y3_Test = train_test_split(X3, Y3, test_size = .3, random_state = i+ 100)
    #plt.plot(X3, Y3, 'o')
    X3_Train = np.reshape(X3_Train, (-1, 1))
    X3_Test = np.reshape(X3_Test, (-1, 1))
    reg3 = LinearRegression().fit(X3_Train, Y3_Train)
    Y3_Prediction = reg3.predict(X3_Test)
    intercept.append(reg3.intercept_)
    coef.append(reg3.coef_)
    r2s += r2_score(Y3_Test, Y3_Prediction) / 100
print('Coef: ' + str(geo_mean(coef)))
print('Intercept: ' + str(geo_mean(intercept)))
print('Score: ' + str(r2s))

pipelines.to_csv('Test.csv')
file = os.path.join('Test.csv')
os.startfile(file)
