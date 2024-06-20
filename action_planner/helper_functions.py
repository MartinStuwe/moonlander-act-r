import numpy as np
import scipy.stats as sts


def mkdir_p(mypath):
    """Creates a directory. equivalent to using mkdir -p on the command line"""
    # shamelessly copied from:
    # "https://stackoverflow.com/questions/11373610/save-matplotlib-file-to-a-directory/31809973#31809973"

    from errno import EEXIST
    from os import makedirs, path

    try:
        makedirs(mypath)
    except OSError as exc:  # Python >2.5
        if exc.errno == EEXIST and path.isdir(mypath):
            pass
        else:
            raise


class CustomError(Exception):
    pass


def load_parameters_dict(file="none", parameters=None):
    if parameters is None:
        parameters = {}
    with open(file) as fh:
        for line in fh:
            name, value = line.strip().split()
            parameters[name] = float(value)

    # the following parameters mustbe included and set in partable
    known_pars = {"CCLThreshold", "SoCBoost", "convolutionGranularity", "persistenceTimeWindow"}
    if known_pars <= parameters.keys():
        return parameters
    else:
        raise CustomError("Something wrong with parameters in parameter file")


def likelihood_function(space, mu, sigma):
    """
    :param space: range of axis for which pdf is generated
    :param mu: true step size of  spaceship
    :param sigma: visual acuity

    Obtaining probability density which is returned normalized
    """
    
    likelihood_out = sts.norm.pdf(space, loc=mu, scale=sigma)
    return likelihood_out/likelihood_out.sum()


def normalized_posterior(prior, likelihood):
    """
    integrate prior and likelihood into posterior which is returned normalized
    """
    posterior = prior * likelihood
    normalized_posterior = posterior / posterior.sum()
    return normalized_posterior


def bound(low, high, value):
    return max(low, min(high, value))


# dict for mapping granularity to mean activation
convolutionGranularity_activation_dict = {
    72: 0.12,
    42: 0.08,
    30: 0.03,
    20: 0.02,
    12: 0.005
}

HL_SoC_convolutionGranularity_dict = {
    1: 12,
    0.9: 12,
    0.8: 20,
    0.7: 20,
    0.6: 30,
    0.5: 30,
    0.4: 42,
    0.3: 42,
    0.2: 72,
    0.1: 72,
    0.0: 72
}
