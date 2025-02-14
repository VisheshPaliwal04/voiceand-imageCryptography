import time
import matplotlib.pyplot as plt
import numpy as np

class Benchmark:
    # benchmark.py
    @staticmethod
    def time_operation(func, *args):
        start = time.time()
        result = func(*args)
        return time.time() - start, result  # This returns a tuple of (time, result)

    @staticmethod
    def plot_performance(sizes, times, title):
        plt.figure()
        plt.plot(sizes, times)
        plt.title(title)
        plt.xlabel("Image Size (pixels)")
        plt.ylabel("Time (seconds)")
        plt.grid(True)
        plt.show()

    @staticmethod
    def calculate_entropy(data):
        hist = np.histogram(data, bins=256)[0]
        prob = hist / hist.sum()
        return -np.sum(prob * np.log2(prob + 1e-10))