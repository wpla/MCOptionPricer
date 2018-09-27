from option_types import OptionTypes


class AsianOption:
    """ Asian Option """

    def __init__(self, strike, option_type = OptionTypes.CALL):
        self.strike = strike
        self.option_type = option_type

    def payoff(self, avg_asset_price):
        if self.option_type == OptionTypes.CALL:
            if avg_asset_price > self.strike:
                return avg_asset_price - self.strike
        return 0

    def payoff_from_series(self, series):
        avg_asset_price = series.mean()
        return self.payoff(avg_asset_price)
