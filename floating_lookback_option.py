from option_types import OptionTypes


class FloatingLookbackOption:
    """ Floating Lookback Option """

    def __init__(self, option_type=OptionTypes.CALL):
        self.option_type = option_type

    def payoff(self, asset_price, min_asset_price):
        if self.option_type == OptionTypes.CALL:
            return asset_price - min_asset_price
        return 0

    def payoff_from_series(self, series):
        last_asset_price = series.iloc[-1]
        min_asset_price = series.min()
        return self.payoff(last_asset_price, min_asset_price)
