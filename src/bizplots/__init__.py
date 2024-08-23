from ._plots import plot_quantiles, plot_spaghetti
from ._containers import QuantileContainer, SpaghettiContainer
from ._handlers import HandlerQuantile, HandlerSpaghetti


handler_map = {
    QuantileContainer: HandlerQuantile(),
    SpaghettiContainer: HandlerSpaghetti(),
}

__all__ = ["plot_quantiles", "plot_spaghetti", "handler_map"]
