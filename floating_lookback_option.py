from option_types import OptionType
from numpy import log, exp, sqrt
from scipy.stats import norm


class FloatingLookbackOption:
    """ Floating Lookback Option """

    def __init__(self, option_type=OptionType.CALL):
        self.option_type = option_type

    def payoff(self, asset_price, min_asset_price, max_asset_price):
        if self.option_type == OptionType.CALL:
            return asset_price - min_asset_price
        elif self.option_type == OptionType.PUT:
            return max_asset_price - asset_price
        return 0

    def payoff_from_series(self, series):
        last_asset_price = series.iloc[-1]
        min_asset_price = series.min()
        max_asset_price = series.max()
        return self.payoff(last_asset_price, min_asset_price, max_asset_price)

    def black_scholes_price_2(self, asset_price, asset_min, asset_max, sigma, r, time_to_maturity=1, D=0):
        """ Calculates value of option according to Black-Scholes-Formula.
            Formula from PWOQF Vol 2, p. 450

        Arguments:
            asset_price: current asset price
            asset_min: minimum of asset price so far
            asset_max: maximum of asset price so far
            sigma: volatility of underlying asset in std-deviations of returns
            r: the risk-free interest rate
            time_to_maturity: time to maturity in years
            D: cumulative dividends of underlying asset payed until maturity of the option
        """

        t = time_to_maturity
        S = asset_price

        if self.option_type == OptionType.CALL:
            M = asset_min
            d1 = (log(S / M) + (r - D + 1 / 2 * sigma ** 2) * t) / (sigma * sqrt(t))
            d2 = d1 - (sigma * sqrt(t))

            return S * exp(-D * t) * norm.cdf(d1) - M * exp(-r * t) * norm.cdf(d2) + \
                S * exp(-r * t) * (sigma ** 2) / (2 * (r - D)) * \
                ((S / M) ** -(2 * (r - D) / (sigma ** 2)) *
                    norm.cdf(-d1 + (2 * (r - D) * sqrt(t)) / sigma) -
                    exp((r - D) * t) * norm.cdf(-d1))

        elif self.option_type == OptionType.PUT:
            M = asset_max
            d1 = (log(S / M) + (r - D + 1 / 2 * sigma ** 2) * t) / \
                 (sigma * sqrt(t))
            d2 = d1 - (sigma * sqrt(t))
            return M * exp(-r * t) * norm.cdf(-d2) - \
                S * exp(-D * t) * norm.cdf(-d1) + \
                S * exp(-r * t) * (sigma ** 2) / (2 * (r - D)) * \
                (-(S / M) ** -(2 * (r - D) / (sigma ** 2)) *
                    norm.cdf(d1 - (2 * (r - D) * sqrt(t)) / sigma) +
                    exp((r - D) * t) * norm.cdf(d1))
        return 0

    def black_scholes_price(self, asset_price, sigma, r, time_to_maturity=1, D=0):
        """ Calculates value of option according to Black-Scholes-Formula.
            Formula from Musiela, Rutkowski 2005: Martingale Methods in Financial Modelling, p. 238ff

        Arguments:
            asset_price: current asset price
            sigma: volatility of underlying asset in std-deviations of returns
            r: the risk-free interest rate
            time_to_maturity: time to maturity in years
            D: cumulative dividends of underlying asset payed until maturity of the option
        """

        r1 = (r + 1 / 2 * sigma ** 2)
        t = time_to_maturity
        S = asset_price
        d = r1 * sqrt(t) / sigma
        if self.option_type == OptionType.CALL:
            return S * (norm.cdf(d) - exp(-r * t) * norm.cdf(d - sigma * sqrt(t)) - sigma ** 2 / (2 * r) *
                        norm.cdf(-d) + exp(-r * t) * sigma ** 2 / (2 * r) * norm.cdf(d - sigma * sqrt(t)))

        elif self.option_type == OptionType.PUT:
            return S * (-norm.cdf(-d) + exp(-r * t) * norm.cdf(-d + sigma * sqrt(t)) + sigma ** 2 / (2 * r) *
                        norm.cdf(d) - exp(-r * t) * sigma ** 2 / (2 * r) * norm.cdf(-d + sigma * sqrt(t)))
        return 0

    def black_scholes_from_series(self, series, sigma, r, time_to_maturity=1, D=0):
        first_asset_price = series.iloc[0]
        return self.black_scholes_price(first_asset_price, sigma, r, time_to_maturity, D)

    def black_scholes_from_series_2(self, series, sigma, r, time_to_maturity=1, D=0):
        last_asset_price = series.iloc[0]
        return self.black_scholes_price_2(last_asset_price, last_asset_price, last_asset_price, sigma,
                                          r, time_to_maturity, D)
