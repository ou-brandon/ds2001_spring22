## Capital Asset Pricing Model (CAPM)
### Strength Training with Functions, Numpy

### Brandon Ou (bro9tn)
### Dr. Youmi Suk
### University of Virginia
### DS 2001: Programming for Data Science
### 21 March 2022
---
### Objectives: 
- Use numpy and functions to compute a stock's CAPM beta
- Perform sensitivity analysis to understand how the data points impact the beta estimate

### Background


In finance, CAPM is a single-factor regression model used for explaining and predicting excess stock returns. There are better, more accurate models, but it has its uses. For example, the *market beta* is a useful output.


Here is the formula for calculating the expected excess return:

\begin{aligned} &E[R_i] - R_f  = \beta_i ( E[R_m] - R_f ) \\ \\ &\textbf{where:} \\ &ER_i = \text{expected return of stock i} \\ &R_f = \text{risk-free rate} \\ &\beta_i = \text{beta of the stock} \\ &ER_m - R_f = \text{market risk premium} \\ \end{aligned} 

#### Review the instructions below to complete the requested tasks.

#### TOTAL POINTS: 10
---  

# load modules
import numpy as np
import pandas as pd

# risk-free Treasury rate
R_f = 0.0175 / 252
# read in the market data
data = pd.read_csv('capm_market_data.csv')
Look at some records  
SPY is an ETF for the S&P 500 (the "stock market")  
AAPL is Apple  
The values are closing prices, adjusted for splits and dividends
data.head()
Drop the date column
df = data.drop(['date'], axis=1)
df.head()

Compute daily returns (percentage changes in price) for SPY, AAPL  
Be sure to drop the first row of NaN  
Hint: pandas has functions to easily do this
pct_chg = df.pct_change().dropna()
#### 1. (1 PT) Print the first 5 rows of returns
pct_chg.head(5)
Save AAPL, SPY returns into separate numpy arrays  
#### 2. (1 PT) Print the first five values from the SPY numpy array, and the AAPL numpy array
spy = pct_chg['spy_adj_close']
spy.head(5)
aapl = pct_chg['aapl_adj_close']
aapl.head(5)
##### Compute the excess returns of AAPL, SPY by simply subtracting the constant *R_f* from the returns.
##### Specifically, for the numpy array containing AAPL returns, subtract *R_f* from each of the returns. Repeat for SPY returns.

NOTE:  
AAPL - *R_f* = excess return of Apple stock  
SPY - *R_f* = excess return of stock market

excess_spy = spy - R_f
excess_aapl = aapl - R_f
#### 3. (1 PT) Print the LAST five excess returns from both AAPL, SPY numpy arrays

print(excess_spy[-5:])
print(excess_aapl[-5:])
#### 4. (1 PT) Make a scatterplot with SPY excess returns on x-axis, AAPL excess returns on y-axis####
Matplotlib documentation: https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.scatter.html
import matplotlib.pyplot as plt
x = excess_spy
y = excess_aapl
plt.scatter(x, y)
#### 5. (3 PTS) Use Linear Algebra (matrices) to Compute the Regression Coefficient Estimate, \\(\hat\beta_i\\)

Hint 1: Here is the matrix formula where *x′* denotes transpose of *x*.

\begin{aligned} \hat\beta_i=(x′x)^{−1}x′y \end{aligned} 

Hint 2: consider numpy functions for matrix multiplication, transpose, and inverse. Be sure to review what these operations do, and how they work, if you're a bit rusty.
inv_xprime_x = 1/(x.transpose().dot(x))
beta_est = inv_xprime_x * x.transpose().dot(y)
print(beta_est)
You should have found that the beta estimate is greater than one.  
This means that the risk of AAPL stock, given the data, and according to this particular (flawed) model,  
is higher relative to the risk of the S&P 500.


#### Measuring Beta Sensitivity to Dropping Observations (Jackknifing)
Let's understand how sensitive the beta is to each data point.   
We want to drop each data point (one at a time), compute \\(\hat\beta_i\\) using our formula from above, and save each measurement.

#### 6. (3 PTS) Write a function called `beta_sensitivity()` with these specs:

- take numpy arrays x and y as inputs
- output a list of tuples. each tuple contains (observation row dropped, beta estimate)

Hint: **np.delete(x, i).reshape(-1,1)** will delete observation i from array x, and make it a column vector
# '''
def beta_sensitivity(x, y):
    res = []
    x = x.to_numpy().reshape(-1, 1)
    y = y.to_numpy().reshape(-1, 1)
    for i in range(0, len(x)):
        temp_x = x[i]
        temp_y = y[i]
        x = np.delete(x, i)
        y = np.delete(y, i)
        temp_beta_est = (1/(x.transpose().dot(x))) * x.transpose().dot(y)
        res.append((i, temp_beta_est))
        x = np.insert(x, i, temp_x)
        y = np.insert(y, i, temp_y)
    return res
# '''


'''
def beta_sensitivity(x, y):
    res = []
    x = x.to_numpy().reshape(-1, 1)
    y = y.to_numpy().reshape(-1, 1)
    for i in range(0, len(x) - 1):
        temp_x = x[0]
        temp_y = y[0]
        x = np.delete(x, 0)
        y = np.delete(y, 0)
        temp_beta_est = (1/(x.transpose().dot(x))) * x.transpose().dot(y)
        res.append((i, temp_beta_est))
        # x = np.insert(x, i, temp_x)
        # y = np.insert(y, i, temp_y)
    return res
'''
#### Call `beta_sensitivity()` and print the first five tuples of output.
print(beta_sensitivity(x, y)[:5])