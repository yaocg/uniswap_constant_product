from decimal import Decimal
from typing import Union
from optparse import OptionParser

def simulateTrade(token0_reserve:int, token1_reserve:int, token0_amount_in:Union[int,None]=None, token1_amount_in:Union[int,None]=None)->(int,int,int,int):
    """
    return reserve0, reserve1, amountIn0/amountOut0, amountOut1/amountIn1
    """
    # uint amountInWithFee = amountIn.mul(997);
    # uint numerator = amountInWithFee.mul(reserveOut);
    # uint denominator = reserveIn.mul(1000).add(amountInWithFee);
    # amountOut = numerator / denominator;
    if token0_amount_in:
        amountIn = token0_amount_in
        reserveIn = token0_reserve
        reserveOut = token1_reserve
    elif token1_amount_in:
        amountIn = token1_amount_in
        reserveIn = token1_reserve
        reserveOut = token0_reserve
    else:
        return token0_reserve, token1_reserve, token0_amount_in, token1_amount_in

    amountInWithFee = Decimal(amountIn*997)
    numerator = amountInWithFee*reserveOut
    denominator = (reserveIn*1000) + amountInWithFee
    amountOut = int(numerator / denominator)

    reserveIn += amountIn
    reserveOut -= amountOut

    if token0_amount_in:
        return reserveIn, reserveOut, amountIn, amountOut
    else:
        return reserveOut, reserveIn, amountOut, amountIn


if __name__ == "__main__":

    default_t0r = 0
    default_t1r = 0
    default_t0i = 0
    default_t1i = 0

    usage = "usage: python3 main.py [options] arg"
    parser = OptionParser(usage=usage,description="command descibe")
    parser.add_option("--t0r", dest="token0_reserve",   default=default_t0r, help=f"token0 reserve(>0), default:{default_t0r}")
    parser.add_option("--t1r", dest="token1_reserve",   default=default_t1r, help=f"token1 reserve(>0), default:{default_t1r}")
    parser.add_option("--t0i", dest="token0_in",        default=default_t0i, help=f"token0 amount in(>0/=0), default:{default_t0r}")
    parser.add_option("--t1i", dest="token1_in",        default=default_t1i, help=f"token1 amount in(=0/>0), default:{default_t1r}")

    (options, args) = parser.parse_args()
    token0_reserve = int(options.token0_reserve)
    token1_reserve = int(options.token1_reserve)
    token0_in = int(options.token0_in)
    token1_in = int(options.token1_in)
    if token0_reserve and token1_reserve and (token0_in or token1_in):
        token0_reserve_out, token1_reserve_out, token0_amount_out, token1_amount_out = simulateTrade(
                token0_reserve=token0_reserve,
                token1_reserve=token1_reserve,
                token0_amount_in=token0_in,
                token1_amount_in=token1_in)
        print("token0_reserve_out:", token0_reserve_out)
        print("token1_reserve_out:", token1_reserve_out)
        print("token0_amount_out:", token0_amount_out)
        print("token1_amount_out:", token1_amount_out)
    else:
        parser.print_help()

