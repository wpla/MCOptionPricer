from option_pricer import OptionPricer
from binary_option import BinaryOption
from fixed_lookback_option import FixedLookbackOption
from floating_lookback_option import FloatingLookbackOption
from option import Option
from option_types import OptionType
from simulation import *
from optparse import OptionParser

if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("-r", "--rate", dest="r", type="float",
                      help="Risk-free interest rate (Default: 0.05)", default=0.05)
    parser.add_option("-a", "--asset", dest="asset", type="float",
                      help="Initial asset price (Default: 100)", default=100)
    parser.add_option("-s", "--sigma", dest="sigma", type="float",
                      help="Sigma (Default: 0.2)", default=0.2)
    parser.add_option("-t", "--time_to_maturity", dest="t", type="float",
                      help="Time to maturity in years (Default: 1)", default=1)
    parser.add_option("-k", "--strike", dest="strike", type="float",
                      help="Strike of option (Default: 120)", default=120)
    parser.add_option("-p", "--binary_payoff", dest="binary_payoff", type="float",
                      help="Payoff of binary option (Default: 100)", default=100)
    parser.add_option("--runs", dest="runs", type="int",
                      help="Simulations runs (Default: 100)", default=50)
    parser.add_option("--sim", dest="simulations", type="string",
                      help="List of number of Monte Carlo Simulations during each run"
                           " (Default: 100,1000,1000)", default="100,1000,10000")
    parser.add_option("--steps", dest="steps", type="int",
                      help="Number of price movements within each MC simulation (Default: 100)", default=100)
    parser.add_option("-o", "--option_types", dest="option_codes", type="string",
                      help="Option types. Possible values: "
                        "CO = call options, "
                        "PO = put options, "
                        "FLCO = floating lookback call options, "
                        "FLPO = floating lookback put options, "
                        "XLCO = fixed strike lookback call options, "
                        "XLPO = fixed strike lookback put options, "
                        "BCO = binary call options, "
                        "BPO = binary put options, "
                        "A list can be give (e.g. -o CO,PO,XLPO) "
                        "(Default: CO,PO,FLCO,FLPO,XLCO,BCO,BPO)",
                      default="CO,PO,FLCO,FLPO,XLCO,XLPO,BCO,BPO")

    (opts, args) = parser.parse_args()

    # Market parameters
    risk_free_interest_rate = opts.r

    # Asset parameters
    asset_price = opts.asset
    sigma = opts.sigma

    # Option parameters
    time_to_maturity = opts.t
    strike = opts.strike
    binary_payoff = opts.binary_payoff

    # Simulation parameters
    params = SimulationParameters()
    params.runs = opts.runs # Number of simulation runs each running a MC pricing
    params.steps = opts.steps  # Number of asset price movements for each simulation
    params.time_to_maturity = time_to_maturity
    # (x_min, x_max) = [int(x) for x in opts.plot_range_x.split(",")]
    # params.plot_x_min = x_min
    # params.plot_x_max = x_max
    sims = opts.simulations
    list_of_simulations = [int(x) for x in sims.split(",")]

    # Create option pricer
    option_pricer = OptionPricer()
    option_pricer.set_risk_free_rate(risk_free_interest_rate)
    option_pricer.set_init_asset_price(asset_price)
    option_pricer.set_mu(risk_free_interest_rate)
    option_pricer.set_sigma(sigma)

    simulation = Simulation(option_pricer)

    option_shortcuts = {
        "CO": ("Plain Vanilla Call Option", Option(strike)),
        "PO": ("Plain Vanilla Put Option", Option(strike, option_type=OptionType.PUT)),
        "FLCO": ("Floating Lookback Call Option", FloatingLookbackOption()),
        "FLPO": ("Floating Lookback Put Option", FloatingLookbackOption(option_type=OptionType.PUT)),
        "XLCO": ("Fixed Lookback Call Option", FixedLookbackOption(strike)),
        "XLPO": ("Fixed Lookback Put Option", FixedLookbackOption(strike, option_type=OptionType.PUT)),
        "BCO": ("Binary Call Option", BinaryOption(strike, payoff=binary_payoff)),
        "BPO": ("Binary Put Option", BinaryOption(strike, payoff=binary_payoff, option_type=OptionType.PUT))
    }

    option_codes = opts.option_codes
    option_codes = option_codes.split(",")

    for option_code in option_codes:
        (name, option) = option_shortcuts[option_code]
        params.option = option
        params.option_name = name

        # Calculate Black Scholes price
        if "Fixed" in name:
            # Only for fixed lookback options
            params.option_real_price = params.option.black_scholes_price(asset_price,
                                                                         asset_price,  # asset_min
                                                                         asset_price,  # asset_max
                                                                         sigma,
                                                                         risk_free_interest_rate,
                                                                         time_to_maturity)
        else:
            params.option_real_price = params.option.black_scholes_price(asset_price,
                                                                         sigma,
                                                                         risk_free_interest_rate,
                                                                         time_to_maturity)

        for s in list_of_simulations:
            print("Running simulation for " + name)
            params.simulations = s # Number of MC simulations

            # Simulate continuous sampling
            params.set_sampling_method(SimulationParameters.CONTINUOUS_SAMPLING)
            cont_price = simulation.run(params)

            # Simulate discrete sampling
            params.set_sampling_method(SimulationParameters.DISCRETE_SAMPLING)
            params.sample_interval = 0.1
            disc_price = simulation.run(params)

            # Output results to console
            print(params.option_name + " (MC Cont. Sampling): %.2f" % cont_price)
            print(params.option_name + " (MC Disc. Sampling@%.2f): %.2f" % (params.sample_interval,
                                                                            disc_price))
            print(params.option_name + " (Black Scholes): %.4f" % (params.option_real_price, ))


