import numpy as np
from option_pricer import OptionPricer
from binary_option import BinaryOption
from fixed_lookback_option import FixedLookbackOption
from floating_lookback_option import FloatingLookbackOption
from asian_option import AsianOption
from option import Option


def discount(value, r, time=1):
    return value / np.exp(r * time)


if __name__ == "__main__":
    risk_free_interest_rate = 0.05

    option_pricer = OptionPricer(simulations=10000, steps=100)
    option_pricer.generate_data(init_asset_price=100, sigma=0.2, mu=risk_free_interest_rate)

    option = Option(strike=120)
    payoff = option_pricer.get_price(option)
    discounted_payoff = discount(payoff, risk_free_interest_rate)
    print("Plain Vanilla Call Option: %.2f" % (discounted_payoff, ))
    print("Plain Vanilla Call Option (Black Scholes): %.2f" % (option.black_scholes(100, 0.2, risk_free_interest_rate, 1), ))

    binary_option = BinaryOption(strike=120, payoff=150)
    payoff = option_pricer.get_price(binary_option)
    discounted_payoff = discount(payoff, risk_free_interest_rate)
    print("Binary Call Option: %.2f" % (discounted_payoff, ))

    fixed_lookback_option = FixedLookbackOption(strike=120)
    payoff = option_pricer.get_price(fixed_lookback_option)
    discounted_payoff = discount(payoff, risk_free_interest_rate)
    print("Fixed Lookback Call Option: %.2f" % (discounted_payoff, ))

    floating_lookback_option = FloatingLookbackOption()
    payoff = option_pricer.get_price(floating_lookback_option)
    discounted_payoff = discount(payoff, risk_free_interest_rate)
    print("Fixed Lookback Call Option: %.2f" % (discounted_payoff, ))

    asian_option = AsianOption(strike=120)
    payoff = option_pricer.get_price(asian_option)
    discounted_payoff = discount(payoff, risk_free_interest_rate)
    print("Asian Call Option: %.2f" % (discounted_payoff, ))


