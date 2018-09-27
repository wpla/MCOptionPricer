import numpy as np
from option_pricer import OptionPricer
from binary_option import BinaryOption
from fixed_lookback_option import FixedLookbackOption
from floating_lookback_option import FloatingLookbackOption
from asian_option import AsianOption
from barrier_option import BarrierOption
from option import Option
from option_types import OptionType


def discount(value, r, time=1):
    return value / np.exp(r * time)


if __name__ == "__main__":
    risk_free_interest_rate = 0.05

    asset_price = 100
    sigma = 0.2
    time_to_maturity = 1
    strike = 120
    binary_payoff = 100

    option_pricer = OptionPricer(simulations=100000, steps=100)
    option_pricer.generate_data(asset_price, sigma, mu=risk_free_interest_rate)

    call_option = Option(strike)
    payoff = option_pricer.get_price(call_option)
    discounted_payoff = discount(payoff, risk_free_interest_rate)
    print("Plain Vanilla Call Option (Monte Carlo): %.2f" % (discounted_payoff, ))
    print("Plain Vanilla Call Option (Black Scholes): %.2f" %
          (call_option.black_scholes(asset_price, sigma, risk_free_interest_rate, time_to_maturity),))

    put_option = Option(strike, option_type=OptionType.PUT)
    payoff = option_pricer.get_price(put_option)
    discounted_payoff = discount(payoff, risk_free_interest_rate)
    print("Plain Vanilla Put Option (Monte Carlo): %.2f" % (discounted_payoff, ))
    print("Plain Vanilla Put Option (Black Scholes): %.2f" %
          (put_option.black_scholes(asset_price, sigma, risk_free_interest_rate, time_to_maturity),))

    binary_call_option = BinaryOption(strike, payoff=binary_payoff)
    payoff = option_pricer.get_price(binary_call_option)
    discounted_payoff = discount(payoff, risk_free_interest_rate)
    print("Binary Call Option (Monte Carlo): %.2f" % (discounted_payoff, ))
    print("Binary Call Option (Black Scholes): %.2f" %
          (binary_call_option.black_scholes(asset_price, sigma, risk_free_interest_rate, time_to_maturity), ))

    binary_put_option = BinaryOption(strike, payoff=binary_payoff, option_type=OptionType.PUT)
    payoff = option_pricer.get_price(binary_put_option)
    discounted_payoff = discount(payoff, risk_free_interest_rate)
    print("Binary Put Option (Monte Carlo): %.2f" % (discounted_payoff, ))
    print("Binary Put Option (Black Scholes): %.2f" %
          (binary_put_option.black_scholes(asset_price, sigma, risk_free_interest_rate, time_to_maturity), ))

    fixed_lookback_call_option = FixedLookbackOption(strike)
    payoff = option_pricer.get_price(fixed_lookback_call_option)
    discounted_payoff = discount(payoff, risk_free_interest_rate)
    print("Fixed Lookback Call Option (Monte Carlo): %.2f" % (discounted_payoff, ))
    print("Fixed Lookback Call Option (Black Scholes): %.2f" %
          (option_pricer.black_scholes(fixed_lookback_call_option,
                                       sigma, risk_free_interest_rate, time_to_maturity), ))

    fixed_lookback_put_option = FixedLookbackOption(strike, option_type=OptionType.PUT)
    payoff = option_pricer.get_price(fixed_lookback_put_option)
    discounted_payoff = discount(payoff, risk_free_interest_rate)
    print("Fixed Lookback Put Option (Monte Carlo): %.2f" % (discounted_payoff, ))
    print("Fixed Lookback Put Option (Black Scholes): %.2f" %
          (option_pricer.black_scholes(fixed_lookback_put_option,
                                       sigma, risk_free_interest_rate, time_to_maturity), ))

    floating_lookback_call_option = FloatingLookbackOption()
    payoff = option_pricer.get_price(floating_lookback_call_option)
    discounted_payoff = discount(payoff, risk_free_interest_rate)
    print("Floating Lookback Call Option (Monte Carlo): %.2f" % (discounted_payoff, ))
    print("Floating Lookback Call Option (Black Scholes): %.2f" %
          (option_pricer.black_scholes(floating_lookback_call_option,
                                       sigma, risk_free_interest_rate, time_to_maturity), ))

    floating_lookback_put_option = FloatingLookbackOption(option_type=OptionType.PUT)
    payoff = option_pricer.get_price(floating_lookback_put_option)
    discounted_payoff = discount(payoff, risk_free_interest_rate)
    print("Floating Lookback Put Option (Monte Carlo): %.2f" % (discounted_payoff, ))
    print("Floating Lookback Put Option (Black Scholes): %.2f" %
          (option_pricer.black_scholes(floating_lookback_put_option,
                                       sigma, risk_free_interest_rate, time_to_maturity), ))

    asian_call_option = AsianOption(strike)
    payoff = option_pricer.get_price(asian_call_option)
    discounted_payoff = discount(payoff, risk_free_interest_rate)
    print("Asian Call Option (Monte Carlo): %.2f" % (discounted_payoff, ))


