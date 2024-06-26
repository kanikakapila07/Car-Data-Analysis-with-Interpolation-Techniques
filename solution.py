
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.interpolate import lagrange

#loading the dataset by its given url
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/auto-mpg/auto-mpg.data"
columns = ["MPG", "Cylinders", "Displacement", "Horsepower", "Weight", "Acceleration", "Model Year", "Origin", "Car Name"]
dataset = pd.read_csv(url, sep='\s+', names=columns)

#selecting weight and miles per gallon columns
Weight = dataset['Weight']
MPG = dataset['MPG']

#plotting scatter plot of dataset
plt.scatter(Weight, MPG,label='Cars', color='red')
plt.xlabel('Weight (lbs)')
plt.ylabel('Miles Per Gallon (MPG)')
plt.legend()
plt.title('Scatter Plot of Simulated Auto MPG Data \nMPG Vs Weight')
plt.grid(True)
plt.show()

#calculates polynomial interpolation using vandermonde matrix method
def vandermonde_interpolate_np(x, y, xx):
    Vander_matrix = np.vander(x, increasing=False)
    coefficients = np.linalg.solve(Vander_matrix, y)
    result = np.polyval(coefficients, xx)
    return result

#calculates lagrange interpolation
def lagrange_interpolate_scipy(x, y, xx):
    poly = lagrange(x, y)
    return poly(xx)

#calculates newton basis
def newton_basis(x, xx):
    n = len(x)
    m = len(xx)
    N_xx = np.ones((m, n))
    for i in range(1, n):
        N_xx[:, i] = N_xx[:, i-1] * (xx - x[i-1])
    return N_xx

#calculates divided differences
def divide_differences_coef(x, y):
    n = len(x)-1
    div_diff = np.zeros([n+1, n+1])
    #y is first column
    div_diff[:, 0] = y
    for j in range(1, n+1):
        for i in range(n-j+1):
            div_diff[i, j] = (div_diff[i+1, j-1] - div_diff[i, j-1]) / (x[i+j] - x[i])
    coef = div_diff[0, :]
    return coef

#calculates newton interpolation using newton basis and divided differences
def newton_interpolate(x, y, xx):
    N_xx = newton_basis(x, xx)
    c = divide_differences_coef(x, y)
    return np.dot(N_xx, c)

#n is degree
n = 15
x = np.linspace(min(Weight), max(Weight),n+1)
y = np.random.rand(n+1)
xx = np.linspace(min(Weight), max(Weight), 100)
vandermonde_Pn_xx = vandermonde_interpolate_np(x, y, xx)
lagrange_Pn_xx = lagrange_interpolate_scipy(x, y, xx)
newton_Pn_xx = newton_interpolate(x, y, xx)

#plotting three polynomial interpolation methods against orginal data points
plt.scatter(Weight, MPG, label='Original data points', color='red')
plt.plot(xx, vandermonde_Pn_xx,'*',label='Vandermonde Matrix Interpolation', color='orange')
plt.plot(xx, lagrange_Pn_xx,label='Lagrange Interpolation', color='limegreen', )
plt.plot(xx, newton_Pn_xx, '--',label='Newton Interpolation', color='yellow')
plt.xlabel('Weight (lbs)')
plt.ylabel('Miles Per Gallon (MPG)')
plt.title('Scatter Plot of Simulated Auto MPG Data using Interpolation \nMPG Vs Weight')
plt.legend()
plt.grid(True)
plt.show()
