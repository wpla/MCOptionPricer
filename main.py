import numpy as np
from option_pricer import OptionPricer
from binary_option import BinaryOption
from fixed_lookback_option import FixedLookbackOption
from floating_lookback_option import FloatingLookbackOption
from asian_option import AsianOption
from barrier_option import BarrierOption
from option import Option
from option_types import OptionType


if __name__ == "__main__":

    # Monte Carlo parameters
    simulations = 100000
    steps = 100

    # Market parameters
    risk_free_interest_rate = 0.05

    # Asset parameters
    asset_price = 100
    sigma = 0.2

    # Option parameters
    time_to_maturity = 1
    strike = 120
    binary_payoff = 100
    barrier = 140

    option_pricer = OptionPricer()
    option_pricer.set_risk_free_rate(risk_free_interest_rate)
    option_pricer.run_monte_carlo_simulations(asset_price, sigma, mu=risk_free_interest_rate,
                                              simulations=simulations, steps=steps)

    # Plain Vanilla Call Option
    call_option = Option(strike)
    simulated_price = option_pricer.simulated_price(call_option, time_to_maturity)
    black_scholes_price = call_option.black_scholes_price(asset_price, sigma, risk_free_interest_rate,
                                                          time_to_maturity)
    print("Plain Vanilla Call Option (Monte Carlo): %.2f" % (simulated_price,))
    print("Plain Vanilla Call Option (Black Scholes): %.4f" % (black_scholes_price, ))

    # Plain Vanilla Put Option
    put_option = Option(strike, option_type=OptionType.PUT)
    simulated_price = option_pricer.simulated_price(put_option, time_to_maturity)
    black_scholes_price = put_option.black_scholes_price(asset_price, sigma, risk_free_interest_rate,
                                                         time_to_maturity)
    print("Plain Vanilla Put Option (Monte Carlo): %.2f" % (simulated_price,))
    print("Plain Vanilla Put Option (Black Scholes): %.4f" % (black_scholes_price, ))

    # Floating Lookback Call Option
    floating_lookback_call_option = FloatingLookbackOption()
    simulated_price = option_pricer.simulated_price(floating_lookback_call_option, time_to_maturity)
    black_scholes_price = option_pricer.black_scholes_price(floating_lookback_call_option,
                                                            sigma, risk_free_interest_rate, time_to_maturity)
    black_scholes_price_2 = option_pricer.black_scholes_price_2(floating_lookback_call_option,
                                                                sigma, risk_free_interest_rate, time_to_maturity)
    print("Floating Lookback Call Option (Monte Carlo): %.2f" % (simulated_price,))
    print("Floating Lookback Call Option (Black Scholes): %.4f" % (black_scholes_price, ))
    print("Floating Lookback Call Option (Black Scholes 2): %.4f" % (black_scholes_price_2, ))

    # Floating Lookback Put Option
    floating_lookback_put_option = FloatingLookbackOption(option_type=OptionType.PUT)
    simulated_price = option_pricer.simulated_price(floating_lookback_put_option, time_to_maturity)
    black_scholes_price = option_pricer.black_scholes_price(floating_lookback_put_option,
                                                            sigma, risk_free_interest_rate, time_to_maturity)
    black_scholes_price_2 = option_pricer.black_scholes_price_2(floating_lookback_put_option,
                                                                sigma, risk_free_interest_rate, time_to_maturity)
    print("Floating Lookback Put Option (Monte Carlo): %.2f" % (simulated_price,))
    print("Floating Lookback Put Option (Black Scholes): %.4f" % (black_scholes_price, ))
    print("Floating Lookback Put Option (Black Scholes 2): %.4f" % (black_scholes_price_2, ))

    # Fixed Lookback Call Option
    fixed_lookback_call_option = FixedLookbackOption(strike)
    simulated_price = option_pricer.simulated_price(fixed_lookback_call_option, time_to_maturity)
    black_scholes_price = option_pricer.black_scholes_price(fixed_lookback_call_option,
                                                            sigma, risk_free_interest_rate, time_to_maturity)
    print("Fixed Lookback Call Option (Monte Carlo): %.2f" % (simulated_price,))
    print("Fixed Lookback Call Option (Black Scholes): %.4f" % (black_scholes_price, ))

    # Fixed Lookback Put Option
    fixed_lookback_put_option = FixedLookbackOption(strike, option_type=OptionType.PUT)
    simulated_price = option_pricer.simulated_price(fixed_lookback_put_option, time_to_maturity)
    black_scholes_price = option_pricer.black_scholes_price(fixed_lookback_put_option,
                                                            sigma, risk_free_interest_rate, time_to_maturity)
    print("Fixed Lookback Put Option (Monte Carlo): %.2f" % (simulated_price,))
    print("Fixed Lookback Put Option (Black Scholes): %.4f" % (black_scholes_price, ))

    # Binary Call Option
    binary_call_option = BinaryOption(strike, payoff=binary_payoff)
    simulated_price = option_pricer.simulated_price(binary_call_option, time_to_maturity)
    black_scholes_price = binary_call_option.black_scholes_price(asset_price, sigma, risk_free_interest_rate,
                                                                 time_to_maturity)
    print("Binary Call Option (Monte Carlo): %.2f" % (simulated_price,))
    print("Binary Call Option (Black Scholes): %.4f" % (black_scholes_price, ))

    # Binary Put Option
    binary_put_option = BinaryOption(strike, payoff=binary_payoff, option_type=OptionType.PUT)
    simulated_price = option_pricer.simulated_price(binary_put_option, time_to_maturity)
    black_scholes_price = binary_put_option.black_scholes_price(asset_price, sigma, risk_free_interest_rate,
                                                                time_to_maturity)
    print("Binary Put Option (Monte Carlo): %.2f" % (simulated_price,))
    print("Binary Put Option (Black Scholes): %.4f" % (black_scholes_price, ))

    # Barrier Call Option
    barrier_call_option = BarrierOption(strike, barrier,
                                        option_type=OptionType.CALL,
                                        barrier_type=BarrierOption.KNOCK_OUT,
                                        barrier_level=BarrierOption.UP)
    print("Barrier Call Option (Monte Carlo): %.2f" %
          (option_pricer.simulated_price(barrier_call_option, time_to_maturity),))

    # Asian Call Option
    asian_call_option = AsianOption(strike)
    print("Asian Call Option (Monte Carlo): %.2f" %
          (option_pricer.simulated_price(asian_call_option, time_to_maturity),))

    # Asian Put Option
    asian_put_option = AsianOption(strike, option_type=OptionType.PUT)
    print("Asian Put Option (Monte Carlo): %.2f" %
          (option_pricer.simulated_price(asian_put_option),))

