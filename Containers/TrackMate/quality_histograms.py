import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
from skimage.filters import threshold_otsu, threshold_yen, threshold_triangle, threshold_niblack, threshold_li

file_path = '/gscratch/cheme/nlsschim/pytrackmate/pytrackmate/Containers/TrackMate/output/agarose/'
file_list = os.listdir(file_path)

file_list = [f for f in file_list if os.path.isfile(os.path.join(file_path, f))]
file_list = [f for f in file_list if 'spot' in f and '.csv' in f]
print(file_list)


import numpy as np

def get_n_bins(values, min_bin_number=5, max_bin_number=50):
    """
    Returns the optimal number of bins for a histogram using the 
    Freedman-Diaconis rule: bin_width = 2 * IQR / n^(1/3).
    
    Parameters:
    - values: List or NumPy array of data points.
    - min_bin_number: Minimum number of bins.
    - max_bin_number: Maximum number of bins.
    
    Returns:
    - n_bins: Optimal number of bins.
    """
    size = len(values)
    
    # Compute the interquartile range (IQR)
    q1, q3 = np.percentile(values, [25, 75])
    iqr = q3 - q1
    
    # Compute bin width using Freedman-Diaconis rule
    bin_width = 2 * iqr * size**(-1/3)
    
    # Compute number of bins
    data_range = np.ptp(values)  # Equivalent to range[0] in Java
    n_bins = int(np.ceil(data_range / bin_width)) if bin_width > 0 else min_bin_number
    
    # Ensure bins are within bounds
    n_bins = max(min_bin_number, min(n_bins, max_bin_number))
    
    return n_bins

import numpy as np

def otsu_threshold(data):
    return otsu_threshold_with_bins(data, get_n_bins(data))

def otsu_threshold_with_bins(data, n_bins):
    hist, bin_edges = np.histogram(data, bins=n_bins)
    threshold_index = otsu_threshold_index(hist, len(data))
    bin_width = (bin_edges[1] - bin_edges[0])
    return bin_edges[0] + bin_width * threshold_index

def otsu_threshold_index(hist, n_points):
    total = n_points

    sum_total = np.sum(np.arange(len(hist)) * hist)

    sum_b = 0
    w_b = 0
    w_f = 0

    var_max = 0
    threshold = 0

    for t in range(len(hist)):
        w_b += hist[t]  # Weight Background
        if w_b == 0:
            continue

        w_f = total - w_b  # Weight Foreground
        if w_f == 0:
            break

        sum_b += t * hist[t]

        m_b = sum_b / w_b  # Mean Background
        m_f = (sum_total - sum_b) / w_f  # Mean Foreground

        # Calculate Between Class Variance
        var_between = w_b * w_f * (m_b - m_f) ** 2

        # Check if new maximum found
        if var_between > var_max:
            var_max = var_between
            threshold = t

    return threshold

def li_threshold(data, tol=1e-6, max_iter=100):
    """
    Compute the threshold using Li's iterative method.

    Parameters:
        data (numpy array): Input data (grayscale intensity values).
        tol (float): Convergence tolerance.
        max_iter (int): Maximum iterations allowed.

    Returns:
        float: Optimal threshold value.
    """
    data = np.asarray(data)
    hist, bin_edges = np.histogram(data, bins=256, density=True)  # Get histogram

    # Initialize threshold to the mean
    T = np.mean(data)

    for _ in range(max_iter):
        # Divide into background and foreground
        background = data[data < T]
        foreground = data[data >= T]

        if len(background) == 0 or len(foreground) == 0:
            break  # Stop if one class is empty

        # Compute means
        mu_b = np.mean(background)
        mu_f = np.mean(foreground)

        # Update threshold using Li's formula
        T_new = (mu_b - mu_f) / (np.log(mu_b) - np.log(mu_f))

        # Check convergence
        if abs(T - T_new) < tol:
            break

        T = T_new  # Update threshold

    return T




for file in file_list:
    df = pd.read_csv(file_path + file)
    print(df.shape)
    
    # Create a new figure for each histogram
    plt.figure()
    
    # Create histogram
    try:
        n_bins = get_n_bins(df['QUALITY'])  # Number of bins
        hist, bin_edges = np.histogram(df['QUALITY'], bins=n_bins)

        #otsu_auto_thresh = otsu_threshold(df['QUALITY'])
        #li_auto_thresh = li_threshold(df['QUALITY'])

        otsu_auto_thresh = threshold_otsu(hist=hist, nbins=n_bins)
        print(otsu_auto_thresh)
        #li_auto_thresh = threshold_li(hist)

        # Apply log transformation (equivalent to Math.log(1 + value))
        log_hist = np.log1p(hist)  # log(1 + hist)

        # Plot the histogram with log-transformed values
        plt.bar(bin_edges[:-1], log_hist, width=np.diff(bin_edges), edgecolor="black", align="edge")
        plt.axvline(x=otsu_auto_thresh, color='red', linestyle='--', label='Otsu')
        #plt.axvline(x=li_auto_thresh, color='green', label='Li')
        plt.legend()

        
        # Save the figure and then close it to free memory
        plt.savefig(file_path + file[:-4] + '.png')
        plt.close()
    
    except Exception as e:
        # Log or print the error details
        print(f"An error occurred: {e}")
