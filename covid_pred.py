from statsmodels.tsa.ar_model import AutoReg
from random import random

# contrived dataset
# data = [8390, 8251, 10414, 15064, 12394, 14021, 13176, 10501, 12064, 15358, 18974, 18427, 19337, 16696, 16728, 17028, 27007, 24111, 22972, 23024, 19673, 22403, 23794, 30699, 42229, 40622, 42655, 35930, 33751, 36487]
# fit model

def predict_next(data):
    model = AutoReg(data, lags=1)
    model_fit = model.fit()
    # make prediction
    yhat = model_fit.predict(len(data), len(data))
    print(yhat)
    return yhat