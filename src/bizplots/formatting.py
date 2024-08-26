import math

from matplotlib.ticker import Formatter


def _formatted_len(s: float, decimals: int = 2, sign: str = "-"):
    """
    Figure out the length of the string representation of s
    that includes commas, decimal point, decimals, and sign (if any)
    """
    fmt = "g" if decimals is None else f".{decimals:d}f"
    formatted_s = f"{s:{sign},{fmt}}"
    return len(formatted_s)


def _human_readable(x):
    suffixes = ("", "k", "m", "bn", "tn", "qn")
    value = abs(x)
    if value < 1000:
        return x, ""

    index = int(math.log10(value) // 3)
    suffix = suffixes[index]
    divisor = 10 ** (index * 3)
    result = x / divisor
    return result, suffix


def as_currency(
    x: float,
    symbol: str = "$",
    decimals: int = 2,
    sign: str = " ",
    human_readable: bool = True,
):
    """
    Format the number `x` as a currency.

    Args:
        x:
            The numerical value of the currency
        symbol:
            The currency symbol (e.g. $, £, etc.). Single characters only.
        decimals:
            How many digits to include after the decimal point
        sign:
            How to sign the value, options are:
                '+': uses a sign for both positive and negative values
                '-': uses a sign for negative values only
                ' ': sign negative numbers and leave a blank space if positive.
                    This is the default.
        human_readable:
            Whether or not to display the value in human-readable format where we use
            suffixes 'k', 'm', 'bn', 'tn' to simplify large numbers.

    Returns:
        A string representing the currency
    """
    assert len(symbol) == 1
    assert sign in ["-", "+", " "]
    if human_readable:
        x, suffix = _human_readable(x)
    else:
        suffix = ""

    length = _formatted_len(x, decimals, sign)
    fmt = "g" if decimals is None else f".{decimals:d}f"
    return f"{x:{symbol}={sign}{length + 1},{fmt}}{suffix}"


class CurrencyFormatter(Formatter):
    def __init__(self, symbol="$", decimals=None, human_readable=True):
        self.decimals = decimals
        self.symbol = symbol
        self.human_readable = human_readable

    def __call__(self, x, pos=None):
        return self.as_currency(x)

    def as_currency(self, x):
        result = as_currency(
            x,
            decimals=self.decimals,
            symbol=self.symbol,
            human_readable=self.human_readable,
        )
        return self.fix_minus(result)
