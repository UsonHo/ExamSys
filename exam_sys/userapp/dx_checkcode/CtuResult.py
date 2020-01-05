from . import RiskLevel

class CtuResult:
    def __init__(self, riskLevel, riskType):
        self.riskLevel = riskLevel
        self.riskType = riskType

    def hasRisk(self):
        return RiskLevel.REJECT == self.riskLevel or RiskLevel.REVIEW == self.riskLevel

    def getRiskLevel(self):
        return self.riskLevel
