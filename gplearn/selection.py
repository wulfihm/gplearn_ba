"""Selection methods to choose programs from the population

The :mod:`gplearn.selection` module contains some selection method 
with  which to choose from the computer programs created by 
the :mod:`gplearn.genetic` module.
"""

# Author: Hans-Martin Wulfmeyer <wulfmeyer.me>
#
# License: BSD 3 clause

import numpy as np

__all__ = ['make_selection']


class _Selection(object):

    """A selection method to get suitable individuals from the population

        TODO: Description

    Parameters
    ----------
    function : callable
        TODO: Description
    """

    def __init__(self, function, **kwargs):
        self.function = function
        self.kwargs = kwargs

    def __call__(self, *args):
        return self.function(*args, **self.kwargs)


def make_selection(function, **kwargs):
    """Make a selection method

    This factory function creates a selection method object which takes the
    population of programs and selects suitable candiadtes for the evolution
    process.

    Parameters
    ----------
    function : callable
        TODO: description

    *args : TODO: datatype
        TODO: description

    """

    """
        TODO: some tests
        1. Test **kwargs contains all the default parameters needed by
            the provided function (or simply the same number of arguments)
        1. Test that function works with the **kwargs provided and returns
            an indivdual from the population
    """

    return _Selection(function, **kwargs)


def _tournament(random_state, parents, greater_is_better, tournament_size):
        """Find the fittest individual from a sub-population."""
        contenders = random_state.randint(0, len(parents), tournament_size)
        fitness = [parents[p].fitness_ for p in contenders]
        if greater_is_better:
            parent_index = contenders[np.argmax(fitness)]
        else:
            parent_index = contenders[np.argmin(fitness)]
        return parents[parent_index], parent_index


def _paretogp(random_state, paretofront):
        parent_index = random_state.randint(0, len(paretofront))
        return paretofront[parent_index], parent_index
        

def _eplex(random_state, parents, greater_is_better, X, y):
    survivors = parents
    cases = random_state.permutation(len(y))

    for case in cases:
        if len(survivors) == 1:
            break
        # execute only works with 2 dimensional arrays :/
        x = np.vstack((X[case], X[case]))
        errors = [p.execute(x)[0] - y[case] for p in survivors] # <= very performance heavy

        MAD = np.median(np.abs(errors - np.median(errors)))

        if greater_is_better:
            treshold = max(errors) - MAD
            survivors = [p for k, p in enumerate(survivors) if errors[k] >= treshold]
        else :
            treshold = min(errors) + MAD
            survivors = [p for k, p in enumerate(survivors) if errors[k] <= treshold]
                
    parent_index = parents.index(random_state.choice(survivors))
    return parents[parent_index], parent_index

_selection_map = {'tournament': _tournament,
                    'eplex': _eplex}