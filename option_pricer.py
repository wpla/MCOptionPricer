import numpy as np
import pandas as pd


class OptionPricer:
    """ Monte Carlo Option Pricer """

    def __init__(self):
        self.data = pd.DataFrame()
        self.risk_free_rate = 0

    def set_risk_free_rate(self, r):
        self.risk_free_rate = r

    def discount(self, value, time=1):
        return value / np.exp(self.risk_free_rate * time)

    def run_monte_carlo_simulations(self, init_asset_price, sigma, mu, simulations=1000, steps=100):
        dt = 1 / steps
        for n in range(simulations):
            asset_price = init_asset_price
            time = 0
            asset_prices = [asset_price]
            asset_time = [time]

            for i in range(steps):
                # Model of the asset price:
                #   dS = mu*S*dt + sigma*S*dX, X ~ N(0,dt)
                asset_price *= 1 + mu * dt + sigma * np.sqrt(dt) * np.random.normal()
                time += dt
                asset_prices.append(asset_price)
                asset_time.append(time)

            asset_history = pd.Series(asset_prices, asset_time)
            self.data[n] = asset_history

    def simulated_price(self, option, time_to_maturity=1):
        payoff_data = []
        for n in self.data.columns:
            payoff_data.append(option.payoff_from_series(self.data[n]))
        payoffs = pd.Series(payoff_data)
        return self.discount(payoffs.mean(), time_to_maturity)

    def black_scholes_price(self, option, sigma, r, time_to_maturity=1, D=0):
        payoff_data = []
        for n in self.data.columns:
            payoff_data.append(option.black_scholes_from_series(self.data[n], sigma, r, time_to_maturity, D))
        payoffs = pd.Series(payoff_data)
        return self.discount(payoffs.mean(), time_to_maturity)

    def black_scholes_price_2(self, option, sigma, r, time_to_maturity=1, D=0):
        payoff_data = []
        for n in self.data.columns:
            payoff_data.append(option.black_scholes_from_series_2(self.data[n], sigma, r, time_to_maturity, D))
        payoffs = pd.Series(payoff_data)
        return self.discount(payoffs.mean(), time_to_maturity)
