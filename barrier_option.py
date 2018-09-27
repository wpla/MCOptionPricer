from option_types import OptionType


class BarrierOption:
    """ Barrier Option """

    (KNOCK_IN, KNOCK_OUT) = range(2)
    (UP, DOWN) = range(2)

    def __init__(self, strike, barrier, option_type=OptionType.CALL, barrier_type=KNOCK_OUT, barrier_level=UP):
        self.strike = strike
        self.barrier = barrier
        self.option_type = option_type
        self.barrier_type = barrier_type
        self.barrier_level = barrier_level

    def calc_payoff(self, asset_price):
        if self.option_type == OptionType.CALL:
            return max(asset_price - self.strike, 0)
        elif self.option_type == OptionType.PUT:
            return max(self.strike - asset_price, 0)
        return 0

    def payoff(self, asset_price, max_asset_price, min_asset_price):
        if self.barrier_type == self.KNOCK_OUT:
            if self.barrier_level == self.UP:
                if max_asset_price < self.barrier:
                    return self.calc_payoff(asset_price)
            elif self.barrier_level == self.DOWN:
                if min_asset_price > self.barrier:
                    return self.calc_payoff(asset_price)
        elif self.barrier_type == self.KNOCK_IN:
            if self.barrier_level == self.UP:
                if max_asset_price > self.barrier:
                    return self.calc_payoff(asset_price)
            elif self.barrier_level == self.DOWN:
                if min_asset_price < self.barrier:
                    return self.calc_payoff(asset_price)
        return 0

    def payoff_from_series(self, series):
        asset_price = series.iloc[-1]
        max_asset_price = series.max()
        min_asset_price = series.min()
        return self.payoff(max_asset_price, min_asset_price)

