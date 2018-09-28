from option_types import OptionType
import numpy as np
from scipy.stats import norm


class BinaryOption:
    """ Binary Option """

    def __init__(self, strike, payoff, option_type=OptionType.CALL):
        self.strike = strike
        self.payoff_value = payoff
        self.option_type = option_type

    def payoff(self, asset_price):
        if self.option_type == OptionType.CALL:
            if asset_price > self.strike:
                return self.payoff_value
        elif self.option_type == OptionType.PUT:
            if asset_price < self.strike:
                return self.payoff_value
        return 0

    def payoff_from_series(self, series):
        last_asset_price = series.iloc[-1]
        return self.payoff(last_asset_price)

    def black_scholes_price(self, asset_price, sigma, r, time_to_maturity=1, D=0):
        """ Calculates value of option according to Black-Scholes-Formula.

        Arguments:
            asset_price: current asset price
            sigma: volatility of underlying asset in std-deviations of returns
            r: the risk-free interest rate
            time_to_maturity: time to maturity in years
            D: cumulative dividends of underlying asset payed until maturity of the option
        """

        d2 = (np.log(asset_price / self.strike) + (r - D - 1 / 2 * sigma ** 2) * time_to_maturity) / \
                (sigma * np.sqrt(time_to_maturity))
        if self.option_type == OptionType.CALL:
            return np.exp(-r*time_to_maturity)*norm.cdf(d2)*self.payoff_value
        elif self.option_type == OptionType.PUT:
            return np.exp(-r*time_to_maturity)*(1-norm.cdf(d2))*self.payoff_value
        return 0
