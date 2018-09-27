from option_types import OptionTypes
import numpy as np
from scipy.stats import norm


class Option:
    """ Plain Vanilla Call or Put Option """

    def __init__(self, strike, option_type=OptionTypes.CALL):
        self.strike = strike
        self.option_type = option_type

    def payoff(self, asset_price):
        if self.option_type == OptionTypes.CALL:
            if asset_price > self.strike:
                return asset_price - self.strike
        return 0

    def payoff_from_series(self, series):
        asset_price = series.iloc[-1]
        return self.payoff(asset_price)

    def black_scholes(self, asset_price, sigma, r, time_to_maturity):
        if self.option_type == OptionTypes.CALL:
            d1 = (np.log(asset_price/self.strike) + (r + 1/2*sigma**2)*time_to_maturity)/(sigma*np.sqrt(time_to_maturity))
            d2 = (np.log(asset_price/self.strike) + (r - 1/2*sigma**2)*time_to_maturity)/(sigma*np.sqrt(time_to_maturity))
            return asset_price*norm.cdf(d1) - self.strike*np.exp(-r*time_to_maturity)*norm.cdf(d2)
        return 0
