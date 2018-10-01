import numpy as np
import pandas as pd


class OptionPricer:
    """ Monte Carlo Option Pricer """

    def __init__(self):
        self.data = pd.DataFrame()
        self.risk_free_rate = 0
        self.init_asset_price = 0
        self.sigma = 0
        self.mu = 0
        self.start_time = 0
        self.maturity = 1

    def set_risk_free_rate(self, r):
        self.risk_free_rate = r

    def set_init_asset_price(self, asset_price):
        self.init_asset_price = asset_price

    def set_sigma(self, sigma):
        self.sigma = sigma

    def set_mu(self, mu):
        self.mu = mu

    def set_start_time(self, start_time):
        self.start_time = start_time

    def set_maturity(self, maturity):
        self.maturity = maturity

    def discount(self, value, time=1):
        return value / np.exp(self.risk_free_rate * time)

    def run_monte_carlo_simulations(self, simulations=1000, steps=100):
        dt = (self.maturity - self.start_time) / steps
        for n in range(simulations):
            asset_price = self.init_asset_price
            time = self.start_time
            asset_prices = [asset_price]
            asset_time = [time]

            for i in range(steps):
                # Model of the asset price:
                #   dS = mu*S*dt + sigma*S*dX, X ~ N(0,dt)
                asset_price *= 1 + self.mu * dt + self.sigma * np.sqrt(dt) * np.random.normal()
                time += dt
                asset_prices.append(asset_price)
                asset_time.append(time)

            asset_history = pd.Series(asset_prices, asset_time)
            self.data[n] = asset_history

    def simulated_price_continuous_sampling(self, option, time_to_maturity=1):
        payoff_data = []
        for n in self.data.columns:
            payoff_data.append(option.payoff_from_series(self.data[n]))
        payoffs = pd.Series(payoff_data)
        return self.discount(payoffs.mean(), time_to_maturity)

    def sample_data(self, series, sample_distance):
        """ Samples data from series. The index of the series has to be numeric, but can be float as well.

        Example 1 (sample_distance <= delta Index:
            series: Values [0,   1,   2,   3,   4,   5,   6,   7,   8,   9, 1]
                    Index  [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
            sample_distance: 0.001
            Result:        [0,   1,   2,   3,   4,   5,   6,   7,   8,   9, 1]
            => In this case the result equals the original series, since the sample distances are
               smaller than the distance between the indexes

        Example 2 (sample_distance > delta Index:
            series: Values [0,   1,   2,   3,   4,   5,   6,   7,   8,   9, 1]
                    Index  [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
            sample_distance: 0.25
            Result:        [0,        2,             5,        7,           1]

            => In this case the series is reduced.
        """

        sample_pos = 0
        index = series.index
        index_pos = 0
        sampled_values = []
        sampled_index = []

        while index_pos < len(index) - 1:
            if sample_pos < index[index_pos]:
                sample_pos += sample_distance
            elif sample_pos >= index[index_pos + 1]:
                index_pos += 1
            elif sample_pos >= index[index_pos]:
                sampled_values.append(series[index[index_pos]])
                sampled_index.append(index[index_pos])
                sample_pos += sample_distance
                index_pos += 1
        sampled_values.append(series[index[-1]])
        sampled_index.append(index[-1])

        return pd.Series(sampled_values, sampled_index)

    def simulated_price_discrete_sampling(self, option, time_to_maturity=1, sample_distance=0.1):
        payoff_data = []
        for n in self.data.columns:
            sampled_data = self.sample_data(self.data[n], sample_distance)
            payoff_data.append(option.payoff_from_series(sampled_data))
        payoffs = pd.Series(payoff_data)
        return self.discount(payoffs.mean(), time_to_maturity)

