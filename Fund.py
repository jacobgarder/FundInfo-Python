from TAA import TAA


class Fund:

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.NAV = TAA.getNAV(id)
        self.MA6 = TAA.getMA(id, 120)
        self.MA10 = TAA.getMA(id, 200)
        self.oneMonth = TAA.getChangePercent(id, "month")
        self.threeMonths = TAA.getChangePercent(id, "three_months")
        self.sixMonths = TAA.getChangePercent(id, "six_months")
        self.oneYear = TAA.getChangePercent(id, "year")
        self.average = (self.oneMonth + self.threeMonths +
                        self.sixMonths + self.oneYear) / 4

    def getMA6Indicator(self):
        return (self.NAV - self.MA6) / self.MA6 * 100.0

    def getMA10Indicator(self):
        return (self.NAV - self.MA10) / self.MA10 * 100.0

    def getAverageReturns(self):
        return (self.average)

    def getFormattedHeader():
        return '{:>10}{:>32}{:>10}{:>10}{:>10}{:>10}{:>10}{:>10}{:>10}{:>10}'.format(
            "Id", "Name", "Current", "MA6 %", "MA10 %", "1 month", "3 months", "6 months", "1 year", "1/3/6/12")

    def getFormattedData(self):
        return '{:>10}{:>32}{:>10.2f}{:>10.2f}{:>10.2f}{:>10.2f}{:>10.2f}{:>10.2f}{:>10.2f}{:>10.2f}'.format(
            self.id, self.name[:30], self.NAV, self.getMA6Indicator(), self.getMA10Indicator(), self.oneMonth, 
            self.threeMonths, self.sixMonths, self.oneYear, self.average)
