"""
The :mod:`sklearn.cluster` module gathers popular unsupervised clustering
algorithms.
"""
import numpy as np

def __stat_intervals(stat, alpha=0.05):
    boundaries = np.percentile(stat, [100 * alpha / 2, 100 * (1 - alpha / 2)])
    return boundaries    

def __get_bootstrap_samples(array, n_samples,seed=None):
    if type(array)!=np.ndarray:
        array=np.array(array)
    if seed:np.random.seed(seed)

    indices = np.random.randint(0, len(array), (n_samples, len(array)))
    samples = array[indices]
    return samples

def __print_conf_int(alpha,text,boundaries):
    print("{:.0%} confidence interval {}:[{:.2f},{:.2f}]".format(1-alpha,text,boundaries[0],boundaries[1]))


def bootstrap_confint(array,n_samples,function=np.mean,alpha=0.05,seed=None,print_text=True,text=''):
    """Function for calculation confidence interval using bootstrap.
    Args:
        array: input data (numpy array or list)
        function: function, applied to each bootsrapped sample
        n_samples: numbder of generated bootstrap samples
        aplpha:confidence level
        seed: random seed
        print_text: enable/disable printing message  with conf interval
        text:extra text added to message

    """
    scores =list(map(function, __get_bootstrap_samples(array, n_samples,seed)))
    boundaries=__stat_intervals(scores, alpha)

    if print_text:__print_conf_int(alpha,text,boundaries)  
    return boundaries


def bootstrap_delta_confint(array1,array2,n_samples,function=np.mean,alpha=0.05,seed=None,print_text=True,text=''):
    """Function for calculation confidence interval for difference on two samples(array1-array2) using bootstrap.
    Args:
        array1: input data (numpy array or list)
        function: function, applied to each bootsrapped sample
        n_samples: numbder of generated bootstrap samples
        aplpha:confidence level
        seed: random seed
        print_text: enable/disable printing message  with conf interval
        text:extra text added to message

    """
    scores1 =map(function, __get_bootstrap_samples(array1, n_samples,seed))
    scores2 =map(function, __get_bootstrap_samples(array2, n_samples,seed))
    delta_median_scores = list(map(lambda x: x[1] - x[0], zip(scores1, scores2)))
    boundaries=__stat_intervals(delta_median_scores, alpha)

    if print_text:__print_conf_int(alpha,text,boundaries)
    return boundaries
