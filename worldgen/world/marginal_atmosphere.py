def marginal_atmosphere(cls):
    marginal_distribution = {
                             chlorine_or_fluorine: 0.01852,
                             high_carbon_dioxide: 0.07408,
                             high_oxygen: 0.06944,
                             inert_gases: 0.21296,
                             low_oxygen: 0.25,
                             nitrogen_compounds: 0.21296,
                             sulfur_compounds: 0.06944,
                             organic_toxins: 0.07408,
                             pollutants: 0.01852
                            }

    class MarginalAtmosphere(object):
        def __init__(self, instance):
            self = instance

        @property
        def marginal(self):
            """the marginal modifier"""
            return (type(self)._marginal)

    return MarginalAtmosphere


# marginal atmopsheres decorators
def chlorine_or_fluorine(cls):

    class ChlorineOrFluorine(marginal_atmosphere.MarginalAtmosphere):
        _marginal = "ChlorineOrFluorine"


def high_carbon_dioxide(cls):

    class HighCarbonDioxide(marginal_atmosphere.MarginalAtmosphere):
        _marginal = "HighCarbonDioxide"


def high_oxygen(cls):

    class HighOxygen(marginal_atmosphere.MarginalAtmosphere):
        _marginal = "HighOxygen"


def inert_gases(cls):

    class InertGases(marginal_atmosphere.MarginalAtmosphere):
        _marginal = "InertGases"


def low_oxygen(cls):

    class LowOxygen(marginal_atmosphere.MarginalAtmosphere):
        _marginal = "LowOxygen"


def nitrogen_compounds(cls):

    class NitrogenCompounds(marginal_atmosphere.MarginalAtmosphere):
        _marginal = "NitrogenCompounds"


def sulfur_compounds(cls):

    class SulfurCompounds(marginal_atmosphere.MarginalAtmosphere):
        _marginal = "SulfurCompounds"


def organic_toxins(cls):

    class OrganicToxins(marginal_atmosphere.MarginalAtmosphere):
        _marginal = "OrganicToxins"


def pollutants(cls):

    class Pollutants(marginal_atmosphere.MarginalAtmosphere):
        _marginal = "Pollutants"
