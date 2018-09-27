from option_types import OptionTypes


class FixedLookbackOption:
    """ Fixed Lookback Option """

    def __init__(self, strike, option_type=OptionTypes.CALL):
        self.strike = strike
        self.option_type = option_type

    def payoff(self, max_asset_price):
        if self.option_type == OptionTypes.CALL:
            return max(max_asset_price - self.strike, 0)
        if self.option_type == OptionTypes.PUT:
            return max(self.strike - max_asset_price, 0)
        return 0

    def payoff_from_series(self, series):
        max_asset_price = series.max()
        return self.payoff(max_asset_price)
