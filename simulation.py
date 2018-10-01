import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.stats import norm
import math
import os


class SimulationParameters:
    (CONTINUOUS_SAMPLING, DISCRETE_SAMPLING) = range(2)

    def __init__(self):
        self.runs = 100
        self.simulations = 100
        self.steps= 100
        self.sample_interval = None
        self.set_sampling_method(SimulationParameters.CONTINUOUS_SAMPLING)
        self.option = None
        self.option_name = None
        self.option_real_price = None
        self.start_time = 0
        self.maturity = 1
        self.time_to_maturity = 1
        self.plot_x_min = -2
        self.plot_x_max = 2

    def set_sampling_method(self, method):
        self.sampling_method = method
        self.sampling_name = "cont"
        if method == SimulationParameters.DISCRETE_SAMPLING:
            self.sampling_name = "disc"


class SimulationResult:
    def __init__(self):
        self.option_name = None
        self.sampling_method = None
        self.sampling_interval = None
        self.prices = None
        self.errors = None
        self.real_price = None
        self.price_mean = None
        self.errors_mean = None
        self.errors_stddev = None
        self.errors_variance = None


class Simulation:
    def __init__(self, option_pricer):
        self.option_pricer = option_pricer
        self.result = SimulationResult()

    def write_result_to_file(self, params):
        # Write data to csv file

        filename = params.option_name + ".csv"
        if not os.path.exists(filename):
            outfile = open(filename, "w")
            outfile.write(params.option_name + "\n\n")
            outfile.write("Runs;MC Simulations;Steps;Sampling;Sample_interval;Price (Mean);Real Price;"
                          "Error_Stddev;Error_Variance\n")
        else:
            outfile = open(filename, "a")

        outfile.write("%d;%d;%d;%s;%s;%.4f;%.4f;%.4f;%.4f\n" %
                      (params.runs,
                       params.simulations,
                       params.steps,
                       params.sampling_name,
                       "n/a" if params.sampling_name == "cont" else ("%.2f" % params.sample_interval),
                       self.result.price_mean,
                       params.option_real_price,
                       self.result.errors_stddev,
                       self.result.errors_variance))
        outfile.close()

    def write_plot(self, params):
        # Clear plot

        plt.clf()

        # Create plot

        n, bins, patches = plt.hist(self.result.errors, 20, density=True, facecolor='gray')
        x_max = (max([abs(b) for b in bins]))
        x_max = math.ceil(x_max * 10) / 10
        if x_max < 1:
            x_max = 1

        # Create data for normal distribution with mean = 0, and variance = error_variance

        norm_x = np.arange(-x_max, x_max, 0.01)
        norm_y = [norm.pdf(i, loc=0, scale=np.sqrt(self.result.errors_variance)) for i in norm_x]

        y_max = math.ceil(max(n) * 10) / 10
        plt.plot(norm_x, norm_y, color="black", linewidth=0.5)
        plt.xlabel('Error')
        plt.ylabel('Probability')
        plt.axis([-x_max, x_max, 0, y_max])
        plt.grid(False)

        # Save plot as PNG

        params_str = "-%d-%d-%s%s" % (params.runs,
                                      params.simulations,
                                      params.sampling_name,
                                      "" if params.sampling_method == SimulationParameters.CONTINUOUS_SAMPLING
                                         else ("-%.2f" % params.sample_interval))
        filename = params.option_name + params_str + ".png"
        plt.savefig(filename)

    def run(self, params):
        """ Run several calculations for Monte Carlo simulation and save histogram of errors in histogram."""

        errors = []
        prices = []
        print("Running simulations for " + params.option_name)
        for i in range(params.runs):
            print("%s - step %d/%d, N=%d" % (params.option_name, i, params.runs, params.simulations))
            self.option_pricer.run_monte_carlo_simulations(simulations=params.simulations, steps=params.steps)
            price = 0
            if params.sampling_method == SimulationParameters.CONTINUOUS_SAMPLING:
                price = self.option_pricer.simulated_price_continuous_sampling(params.option, params.time_to_maturity)
            elif params.sampling_method == SimulationParameters.DISCRETE_SAMPLING:
                price = self.option_pricer.simulated_price_discrete_sampling(params.option, params.time_to_maturity,
                                                                        params.sample_interval)
            prices.append(price)
            errors.append(price - params.option_real_price)

        # Calculate histogram and price mean and error parameters

        self.result.prices = pd.Series(prices)
        self.result.price_mean = self.result.prices.mean()
        self.result.errors = pd.Series(errors)
        self.result.errors_stddev = self.result.errors.std()
        self.result.errors_variance = self.result.errors.var()

        self.write_result_to_file(params)
        self.write_plot(params)

        return self.result.price_mean
