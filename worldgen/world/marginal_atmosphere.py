def marginal_atmosphere(cls):

    class MarginalAtmosphere(object):
        def __init__(self, parameters):
            self.parameters = cls(parameters)

    return MarginalAtmosphere


# marginal atmopsheres decorators
def chlorine_or_fluorine(cls):

    class ChlorineOrFluorine(marginal_atmosphere.MarginalAtmosphere):
        pass


def high_carbon_dioxide(cls):

    class HighCarbonDioxide(marginal_atmosphere.MarginalAtmosphere):
        pass


def high_oxygen(cls):

    class HighOxygen(marginal_atmosphere.MarginalAtmosphere):
        pass


def inert_gases(cls):

    class InertGases(marginal_atmosphere.MarginalAtmosphere):
        pass


def low_oxygen(cls):

    class LowOxygen(marginal_atmosphere.MarginalAtmosphere):
        pass


def nitrogen_compounds(cls):

    class NitrogenCompounds(marginal_atmosphere.MarginalAtmosphere):
        pass


def sulfur_compounds(cls):

    class SulfurCompounds(marginal_atmosphere.MarginalAtmosphere):
        pass


def organic_toxins(cls):

    class OrganicToxins(marginal_atmosphere.MarginalAtmosphere):
        pass


def pollutants(cls):

    class Pollutants(marginal_atmosphere.MarginalAtmosphere):
        pass
