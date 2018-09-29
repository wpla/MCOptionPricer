from option_types import OptionType
from numpy import log, exp, sqrt
from scipy.stats import norm


class FixedLookbackOption:
    """ Fixed Lookback Option """

    def __init__(self, strike, option_type=OptionType.CALL):
        self.strike = strike
        self.option_type = option_type

    def payoff(self, min_asset_price, max_asset_price):
        if self.option_type == OptionType.CALL:
            return max(max_asset_price - self.strike, 0)
        elif self.option_type == OptionType.PUT:
            return max(self.strike - min_asset_price, 0)
        return 0

    def payoff_from_series(self, series):
        max_asset_price = series.max()
        min_asset_price = series.min()
        return self.payoff(min_asset_price, max_asset_price)

    def black_scholes_price(self, asset_price, asset_min, asset_max, sigma, r, time_to_maturity=1, D=0):
        """ Calculates value of option according to Black-Scholes-Formula.

        Arguments:
            asset_price: current asset price
            asset_min: minimum of asset price so far
            asset_max: maximum of asset price so far
            sigma: volatility of underlying asset in std-deviations of returns
            r: the risk-free interest rate
            time_to_maturity: time to maturity in years
            D: cumulative dividends of underlying asset payed until maturity of the option
        """

        S = asset_price
        E = self.strike
        t = time_to_maturity
        b = r - D

        if self.option_type == OptionType.CALL:
            M = asset_max
            if E > M:
                d1 = (log(S / E) + (r - D + 1 / 2 * (sigma ** 2)) * t) / \
                     (sigma * sqrt(t))
                d2 = d1 - sigma * sqrt(t)
                C = S * exp(-D * t) * norm.cdf(d1) - \
                    E * exp(-r * t) * norm.cdf(d2) + \
                    S * exp(-r * t) * (sigma ** 2) / (2 * b) * \
                    (-(S / E) ** -(2 * b / sigma ** 2) *
                     norm.cdf(d1 - (2 * b * sqrt(t)) / sigma) +
                     exp(b * t) * norm.cdf(d1))
                return C
            else:
                d1 = (log(S / M) + (r - D + 1 / 2 * (sigma ** 2)) * t) / \
                     (sigma * sqrt(t))
                d2 = d1 - sigma * sqrt(t)
                C = (M - E) * exp(-r * t) + \
                    S * exp(-D * t) * norm.cdf(d1) - \
                    M * exp(-r * t) * norm.cdf(d2) + \
                    S * exp(-r * t) * (sigma ** 2) / (2 * b) * \
                    (-(S / M) ** -(2 * b / sigma ** 2) *
                     norm.cdf(d1 - (2 * b * sqrt(t)) / sigma) +
                     exp(b * t) * norm.cdf(d1))
                return C

        elif self.option_type == OptionType.PUT:
            M = asset_min
            if E < M:
                d1 = (log(S / E) + (b + 1 / 2 * (sigma ** 2)) * t) / \
                     (sigma * sqrt(t))
                d2 = d1 - sigma * sqrt(t)
                P = E * exp(-r * t) * norm.cdf(-d2) - \
                    S * exp(-D * t) * norm.cdf(-d1) + \
                    S * exp(-r * t) * (sigma ** 2) / (2 * b) * \
                    ((S / E) ** -(2 * b / (sigma ** 2)) *
                     norm.cdf(-d1 + (2 * b * sqrt(t)) / sigma) -
                     exp(b * t) * norm.cdf(-d1))
                return 333
            else:
                d1 = (log(S / M) + (b + 1 / 2 * (sigma ** 2)) * t) / \
                     (sigma * sqrt(t))
                d2 = d1 - sigma * sqrt(t)
                P = (E - M) * exp(-r * t) - \
                    S * exp(-D * t) * norm.cdf(-d1) + \
                    M * exp(-r * t) * norm.cdf(-d2) + \
                    S * exp(-r * t) * (sigma ** 2) / (2 * b) * \
                    ((S / M) ** -(2 * b / (sigma ** 2)) *
                     norm.cdf(-d1 + (2 * b * sqrt(t)) / sigma) -
                     exp(b * t) * norm.cdf(-d1))
                return P
        return 0

