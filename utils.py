import math
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline, BSpline
import numpy as np
#from train import N_EPISODES



PLOT_INTERPOLATE = 10

# =====================================================================
def get_distance( p1, p2 ):
    return math.sqrt( (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 )


# =====================================================================
def truncate(number, decimals=0):
    """
    Returns a value truncated to a specific number of decimal places.
    """
    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer.")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more.")
    elif decimals == 0:
        return math.trunc(number)

    factor = 10.0 ** decimals
    return math.trunc(number * factor) / factor


# =====================================================================
def plotData( data, title, xlabel, ylabel, fig_name ):
    
    # Remove NaN and infinite values
    data = np.nan_to_num(data)

    n_episodes = len(data)
    x = np.arange( len( data ) )

    x_ = np.arange( int(n_episodes / PLOT_INTERPOLATE) if n_episodes > PLOT_INTERPOLATE else n_episodes)
    
    #define x as 200 equally spaced values between the min and max of original x 
 
    
    #define spline
    spl = make_interp_spline(x, data, k=3)
    y_smooth = spl(x_)
    #not sure smoothing thing works accurately, need one more check maybe
    
    #create smooth line chart 
    n = x_ * PLOT_INTERPOLATE if n_episodes > PLOT_INTERPOLATE else x_
    plt.plot( n, y_smooth)
    plt.title( title )
    plt.xlabel( xlabel )
    plt.ylabel( ylabel )
    plt.grid()
    plt.savefig( fig_name )
    plt.show()
    