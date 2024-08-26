from . import formatting
from ._plots import plot_quantiles, plot_spaghetti, plot_ribbons
from ._containers import QuantileContainer, SpaghettiContainer, RibbonsContainer
from ._handlers import HandlerQuantile, HandlerSpaghetti, HandlerRibbons


handler_map = {
    QuantileContainer: HandlerQuantile(),
    SpaghettiContainer: HandlerSpaghetti(),
    RibbonsContainer: HandlerRibbons(),
}

__all__ = [
    "plot_quantiles",
    "plot_spaghetti",
    "plot_ribbons",
    "handler_map",
    "formatting",
]
