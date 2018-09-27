import numpy as np
import pandas as pd


class OptionPricer:
    """ Monte Carlo Option Pricer """

    def __init__(self):
        self.data = pd.DataFrame()

    def generate_data(self, init_asset_price, sigma, mu, simulations=100000, steps=100):
        dt = 1 / steps
        for n in range(simulations):
            asset_price = init_asset_price
            time = 0
            asset_prices = [asset_price]
            asset_time = [time]

            for i in range(steps):
                # Model of the asset price
                # dS = mu*S*dt + sigma*S*dX, X ~ N(0,dt)
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

    def black_scholes(self, option, sigma, r, time_to_maturity, D=0):
        payoff_data = []
        for n in self.data.columns:
            payoff_data.append(option.black_scholes_from_series(self.data[n], sigma, r, time_to_maturity, D))
        payoffs = pd.Series(payoff_data)
        return payoffs.mean()

