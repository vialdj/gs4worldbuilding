from scipy.stats import truncnorm

"""generates a random number using a normal distribution within boundaries"""
def truncated_normal(loc, scale, low, up):
    return truncnorm((low - loc) / scale,
                     (up - loc) / scale,
                     loc=loc, scale=scale).rvs()
