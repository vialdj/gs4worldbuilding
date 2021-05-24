def marginal_atmosphere(cls):

    class MarginalAtmosphere:
        def __init__(self, parameters):
            self.parameters = cls(parameters)

    return MarginalAtmosphere
