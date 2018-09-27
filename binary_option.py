from option_types import OptionTypes


class BinaryOption:
    """ Binary Option """

    def __init__(self, strike, payoff, option_type=OptionTypes.CALL):
        self.strike = strike
        self.payoff_value = payoff
        self.option_type = option_type

    def payoff(self, asset_price):
        if self.option_type == OptionTypes.CALL:
            if asset_price >= self.strike:
                return self.payoff_value
        return 0

    def payoff_from_series(self, series):
        last_asset_price = series.iloc[-1]
        return self.payoff(last_asset_price)