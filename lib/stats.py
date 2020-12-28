import numpy as np
import pandas as pd
from scipy.stats import norm


def compute_prop_ci(prop, n, alpha=.05):
    """Compute confidence interval (CI) for proportion.

    :param prop: float, DatFrame or np.array of proportions [0;1]
    :param n: sample size (int, DatFrame or np.array of int)
    :param float alpha: risk [0;1]

    :returns: Tuple[lower CI, upper CI, matplotlib.pyplot.bar yerr np.array]
    """

    z_score = norm.ppf(1 - alpha / 2)
    std_error = np.sqrt(prop * ((1 - prop) / n))

    lci = prop - z_score * std_error
    uci = prop + z_score * std_error

    if isinstance(prop, pd.DataFrame):
        lci = lci.fillna(0)
        uci = uci.fillna(0)

    yerr = None
    if isinstance(prop, np.ndarray) or isinstance(prop, pd.DataFrame):
        yerr = np.array([lci, uci])
        yerr = np.array([
            -(yerr[0] - prop.values).T,
            (yerr[1] - prop.values).T,
        ])

    return lci, uci, yerr
