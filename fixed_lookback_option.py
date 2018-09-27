from option_types import OptionType
import numpy as np
from scipy.stats import norm


class FixedLookbackOption:
    """ Fixed Lookback Option """

    def __init__(self, strike, option_type=OptionType.CALL):
        self.strike = strike
        self.option_type = option_type

    def payoff(self, max_asset_price):
        if self.option_type == OptionType.CALL:
            return max(max_asset_price - self.strike, 0)
        if self.option_type == OptionType.PUT:
            return max(self.strike - max_asset_price, 0)
        return 0

    def payoff_from_series(self, series):
        max_asset_price = series.max()
        return self.payoff(max_asset_price)

    def black_scholes(self, asset_price, asset_min, asset_max, sigma, r, time_to_maturity, D=0):
        """ Calculates value of option according to Black-Scholes-Formula.

        Arguments:
            asset_price: current asset price
            asset_min: minimum of asset price so far
            asset_max: maximum of asset price so far
            sigma: volatility of underlying asset in std-deviations of returns
            r: the risk-free interest rate
            time_to_maturity: time to maturity in years
            D: cumulative dividends pays until maturity of the option
        """

        if self.option_type == OptionType.CALL:
            if self.strike > asset_max:
                d1 = (np.log(asset_price / self.strike) + (r - D + 1 / 2 * sigma ** 2) * time_to_maturity) / \
                     (sigma * np.sqrt(time_to_maturity))
                d2 = d1 - (sigma * np.sqrt(time_to_maturity))
                return asset_price * np.exp(-D * time_to_maturity) * norm.cdf(d1) - \
                       self.strike * np.exp(-r * time_to_maturity) * norm.cdf(d2) + \
                       asset_price * np.exp(-r * time_to_maturity) * (sigma ** 2) / (2 * (r - D)) * \
                       (-(asset_price / self.strike) ** -(2 * (r - D) / sigma ** 2) *
                          norm.cdf(d1 - (2 * (r - D) * np.sqrt(time_to_maturity)) / sigma) +
                          np.exp((r - D) * time_to_maturity) * norm.cdf(d1))
            else:
                d1 = (np.log(asset_price / asset_max) + (r - D + 1 / 2 * sigma ** 2) * time_to_maturity) / \
                     (sigma * np.sqrt(time_to_maturity))
                d2 = d1 - (sigma * np.sqrt(time_to_maturity))
                return (asset_max - self.strike) * np.exp(-r * time_to_maturity) + \
                       asset_price * np.exp(-D * time_to_maturity) * norm.cdf(d1) - \
                       asset_max * np.exp(-r * time_to_maturity) * norm.cdf(d2) - \
                       asset_price * np.exp(-r * time_to_maturity) * (sigma ** 2) / (2 * (r - D)) * \
                       ((asset_price / asset_max) ** -(2 * (r - D) / sigma ** 2) *
                          norm.cdf(-d1 - (2 * (r - D) * np.sqrt(time_to_maturity)) / sigma) +
                          np.exp((r - D) * time_to_maturity) * norm.cdf(d1))

        elif self.option_type == OptionType.PUT:
            if self.strike < asset_min:
                d1 = (np.log(asset_price / self.strike) + (r - D + 1 / 2 * sigma ** 2) * time_to_maturity) / \
                     (sigma * np.sqrt(time_to_maturity))
                d2 = d1 - (sigma * np.sqrt(time_to_maturity))
                return self.strike * np.exp(-r * time_to_maturity) * norm.cdf(-d2) - \
                       asset_price * np.exp(-D * time_to_maturity) * norm.cdf(-d1) + \
                       asset_price * np.exp(-r * time_to_maturity) * (sigma ** 2) / (2 * (r - D)) * \
                       ((asset_price / self.strike) ** -(2 * (r - D) / sigma ** 2) *
                          norm.cdf(-d1 + (2 * (r - D) * np.sqrt(time_to_maturity)) / sigma) -
                          np.exp((r - D) * time_to_maturity) * norm.cdf(-d1))
            else:
                d1 = (np.log(asset_price / asset_min) + (r - D + 1 / 2 * sigma ** 2) * time_to_maturity) / \
                     (sigma * np.sqrt(time_to_maturity))
                d2 = d1 - (sigma * np.sqrt(time_to_maturity))
                return (self.strike - asset_min) * np.exp(-r * time_to_maturity) - \
                       asset_price * np.exp(-D * time_to_maturity) * norm.cdf(-d1) + \
                       asset_min * np.exp(-r * time_to_maturity) * norm.cdf(-d2) + \
                       asset_price * np.exp(-r * time_to_maturity) * (sigma ** 2) / (2 * (r - D)) * \
                       ((asset_price / asset_min) ** -(2 * (r - D) / sigma ** 2) *
                          norm.cdf(-d1 + (2 * (r - D) * np.sqrt(time_to_maturity)) / sigma) -
                          np.exp((r - D) * time_to_maturity) * norm.cdf(-d1))
        return 0

    def black_scholes_from_series(self, series, sigma, r, time_to_maturity, D=0):
        first_asset_price = series.iloc[0]
        min_asset_price = series.min()
        max_asset_price = series.max()
        return self.black_scholes(first_asset_price, min_asset_price, max_asset_price, sigma, r, time_to_maturity, D)
