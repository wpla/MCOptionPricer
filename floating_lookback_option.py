from option_types import OptionTypes


class FloatingLookbackOption:
    """ Floating Lookback Option """

    def __init__(self, option_type=OptionTypes.CALL):
        self.option_type = option_type

    def payoff(self, asset_price, min_asset_price):
        if self.option_type == OptionTypes.CALL:
            return max(asset_price - min_asset_price, 0)
        elif self.option_type == OptionTypes.PUT:
            return max(min_asset_price - asset_price, 0)
        return 0

    def payoff_from_series(self, series):
        last_asset_price = series.iloc[-1]
        min_asset_price = series.min()
        return self.payoff(last_asset_price, min_asset_price)
