import numpy as np
from scipy.stats import norm
from scipy.special import erf

def get_power_spectrum(time_series):
    """
    Applies window function and fourier transform to time_series data and returns power spectrum of FFT: ps[freq]=|FFT(x)|^2[freq]

    :param time_series: Numpy array containing the most recent ADC voltage difference measurements.
    """
    time_series_zero_mean = time_series-np.mean(time_series)
    time_series_fft = np.fft.fft(time_series_zero_mean)
    ps = np.abs(time_series_fft)**2 #Gets square of complex number
    return ps

def get_rms_voltage(ps, freq_min, freq_max, freq, time_series_len):
    """
    Gets the Root-Mean-Square (RMS) voltage of waves with frequency between freq_min and freq_max. Parseval's Theorem says:
    \sum_{i=0}^{N-1} x[i]^2 = \frac{1}{N} \sum_{i=-(N-1)}^{N-1} |FFT(x)[i]|^2
    Using this, the RMS voltage is (first formula is definition, second is implemented evaluation):
    \sqrt{ \frac{1}{N} \sum_{i=0}^{N-1} x[i]^2 } = \frac{1}{N} \sqrt{ \sum_{freq in range} |FFT(x)[freq]|^2}
    
    :param ps: FFT power spectrum of time_series, ps[freq] = |FFT(x)|^2[freq].
    :param freq_min: Number corresponding to minimum alpha wave frequency in Hz.
    :param freq_max: Number corresponding to maximum alpha wave frequency in Hz.
    :param freq: Numpy array of negative and positive FFT freq, fft.fftfreq of time_series
    :param time_series_len: Integer length of time_series
    """
    freq_abs = np.abs(freq) 
    ps_in_range = ps[(freq_abs <= freq_max) & (freq_abs >= freq_min)] #Gets power spectrum for freq in range [freq_min, freq_max]
    rms = (1/time_series_len) * np.sqrt(np.sum(ps_in_range))
    return rms

def gaussian_eval(relaxed, concentrated):
    """
    We approximate concentrated and relaxed brain wave data sets each as normal Gaussian distributions.
    The cross point of the two gaussians give the best V0 (threshold voltage which separates relazed and concentrated data) which minimizes over all error.
    The overlap area divided by 2 give the probability of wrong classification
    The ratio of overlap area left of V0 to right of V0 gives the percentage of wrong estimation being we guessed concentrated but is actually relaxed.
    
    :param data[0]: relaxed data time average
    :param data[1]: concentrated time average

    RETURN:
        V0: threshold voltage which separates relazed and concentrated data
        false_relaxed: probability of false relaxed classification
        false_concentrated: probability of false concentrated classification
"""
    # calculate the meanie and std to construct the gaussian normal distributions
    r_mean = np.mean(relaxed)
    c_mean = np.mean(concentrated)
    r_std = np.std(relaxed)
    c_std = np.std(concentrated)

    # Solve for cross point of the two normal distributions
    a = 1/(2*r_std**2) - 1/(2*c_std**2)
    b = c_mean/(c_std**2) - r_mean/(r_std**2)
    c = r_mean**2 /(2*r_std**2) - c_mean**2 / (2*c_std**2) - np.log(c_std/r_std)
    results = np.roots([a,b,c])

    # Select the cross point in the middle of the two mean values.
    intersection = []
    for i in range(len(results)):
        if results[i] < r_mean and results[i] > c_mean:
            intersection.append(results[i])
    V0 = intersection[0]

    # Calculate the overlap area using erf function
    r_z = (V0 - r_mean)/(r_std * math.sqrt(2))
    r_overlap = (1-abs(erf(r_z)))/2
    c_z = (V0 - c_mean)/(c_std* math.sqrt(2))
    c_overlap = (1-abs(erf(c_z)))/2

    # probability of false relaxed classification
    false_relaxed = c_overlap/2
    # probability of false concentrated classification
    false_concentrated = r_overlap/2
    
    return V0, false_relaxed, false_concentrated
