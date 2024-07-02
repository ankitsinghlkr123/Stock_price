from django.shortcuts import render
from datetime import date

import yfinance as yf
import numpy as np
import pandas as pd
import seaborn as sns
import random 
import matplotlib.pyplot as plt
import pandas_datareader as data
from scipy.stats import norm
from scipy.stats import skewnorm
from plotly import graph_objs as go
def home(request):
    return render(request,'predict/index.html')


def eval(request):
    if request.method == 'POST':
        desired_ticker = request.POST.get('ticker')    
        start='2022-12-23'
        end='2023-1-25'
        df = yf.download(desired_ticker, start, end)
        price = df['Close']
        historical_returns = price.pct_change()
        historical_returns = historical_returns.dropna()
        lower_bound = norm.ppf(0.25)
        upper_bound = norm.ppf(0.70)
        mean = historical_returns.mean()
        stdev = historical_returns.std()
        np.random.seed()
        n = np.random.normal(size=(10, 30))
        rows = n.shape[0]
        cols = n.shape[1]
        for i in range(0, rows):
            for j in range(0, cols):
                if n[i][j] > upper_bound:
                    n[i][j] = upper_bound
                elif n[i][j] < lower_bound:
                    n[i][j] = lower_bound
                else:
                    n[i][j] = n[i][j]
                n[i][j] = (stdev * (n[i][j])) + mean
        p = np.zeros([rows, cols + 1])
        if(price.size!=0):
            for i in range(0, rows):
                p[i][0] = price[-1]
        for i in range(1, cols + 1):
            for j in range(0, rows):
                p[j][i] = (p[j][i - 1]) * (1 + n[j][i - 1])
        x = np.arange(0, cols + 1)
        fig, ax = plt.subplots(nrows=1, ncols=1)
        for d in range(0, rows):
            ax.plot(x, p[d])
            ax.set_xlabel('days')
            ax.set_ylabel('stock price')
                    
        import base64
        import io
        from io import BytesIO
        
        buffer = io.BytesIO()
        plt.gcf().canvas.print_png(buffer)
        plt_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
        plt.close(fig)
        
        return render(request, 'predict/result.html', {'image_data': plt_data})
    return render(request, 'predict/index.html')