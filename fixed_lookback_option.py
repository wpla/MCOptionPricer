from option_types import OptionTypes


class FixedLookbackOption:
    """ Fixed Lookback Option """

    def __init__(self, strike, option_type=OptionTypes.CALL):
        self.strike = strike
        self.option_type = option_type

    def payoff(self, max_asset_price):
        if self.option_type == OptionTypes.CALL:
            if max_asset_price > self.strike:
                return max_asset_price - self.strike
        return 0

    def payoff_from_series(self, series):
        max_asset_price = series.max()
        return self.payoff(max_asset_price)
