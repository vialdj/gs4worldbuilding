from . import Atmosphere


class MarginalAtmosphere(Atmosphere):
    def __init__(self, atmosphere):
        self = atmosphere

    @property
    def marginal(self):
        """the marginal modifier"""
        return (type(self)._marginal)


class ChlorineOrFluorine(MarginalAtmosphere):
    _toxicity = Atmosphere.Toxicity.HIGH
    _marginal = "ChlorineOrFluorine"


class HighCarbonDioxide(MarginalAtmosphere):
    _marginal = "HighCarbonDioxide"


class HighOxygen(MarginalAtmosphere):
    _marginal = "HighOxygen"


class InertGases(MarginalAtmosphere):
    _marginal = "InertGases"


class LowOxygen(MarginalAtmosphere):
    _marginal = "LowOxygen"


class NitrogenCompounds(MarginalAtmosphere):
    _toxicity = Atmosphere.Toxicity.MILD
    _marginal = "NitrogenCompounds"


class SulfurCompounds(MarginalAtmosphere):
    _toxicity = Atmosphere.Toxicity.MILD
    _marginal = "SulfurCompounds"


class OrganicToxins(MarginalAtmosphere):
    _toxicity = Atmosphere.Toxicity.MILD
    _marginal = "OrganicToxins"


class Pollutants(MarginalAtmosphere):
    _toxicity = Atmosphere.Toxicity.MILD
    _marginal = "Pollutants"


marginal_distribution = {
    ChlorineOrFluorine: 0.01852,
    HighCarbonDioxide: 0.07408,
    HighOxygen: 0.06944,
    InertGases: 0.21296,
    LowOxygen: 0.25,
    NitrogenCompounds: 0.21296,
    SulfurCompounds: 0.06944,
    OrganicToxins: 0.07408,
    Pollutants: 0.01852
}
