import numpy as np
import pandas as pd


class OptionPricer:
    """ Monte Carlo Option Pricer """

    def __init__(self, simulations=1000, steps=100):
        self.simulations = simulations
        self.steps = steps
        self.data = pd.DataFrame()

    def generate_data(self, init_asset_price, sigma, mu):
        dt = 1 / self.steps
        for n in range(self.simulations):
            asset_price = init_asset_price
            time = 0
            asset_prices = [asset_price]
            asset_time = [time]

            for i in range(self.steps):
                # Model of the asset price in a risk-free environment
                # dS = r*S*dt + sigma*S*dX^Q
                asset_price *= 1 + mu * dt + sigma * np.sqrt(dt) * np.random.normal()
                time += dt
                asset_prices.append(asset_price)
                asset_time.append(time)

            asset_history = pd.Series(asset_prices, asset_time)
            self.data[n] = asset_history

    def get_price(self, option):
        payoff_data = []
        for n in self.data.columns:
            payoff_data.append(option.payoff_from_series(self.data[n]))
        payoffs = pd.Series(payoff_data)
        return payoffs.mean()

