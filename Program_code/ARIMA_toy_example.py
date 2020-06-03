from pandas import read_csv
from pandas import datetime
import matplotlib.pyplot as plt
from statsmodels.tsa.arima_model import ARIMA
series = read_csv('C:/Users/Zhiyan/Desktop/ATR301.csv', header=0)
X = series.values
size = int(len(X) * 0.66)
train, test = X[0:size], X[size:len(X)]
history = [x for x in train]
predictions = list()
for t in range(len(test)):
	model = ARIMA(history, order=(5,1,0))
	model_fit = model.fit(disp=0)
	output = model_fit.forecast()
	yhat = output[0]
	predictions.append(yhat)
	obs = test[t]
	history.append(obs)
	print('predicted=%f, expected=%f' % (yhat, obs))
predictions=list(train)+predictions
plt.plot(range(len(predictions)),predictions,label='predicted')
plt.plot(range(len(X)),X,label='actual')
plt.legend()
plt.savefig(r'C:/Users/zhiyan/desktop/ARIMA_case.png')
plt.show()
