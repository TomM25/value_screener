import numpy as np
from datetime import date

from get_financial_report import get_financial_report


class Firm:
    def __init__(self, ticker, market='us', read_data_dir=None, write_data_dir='data'):
        self.ticker = ticker
        self.market = market
        self.read_data_dir = read_data_dir
        self.write_data_dir = write_data_dir

    def get_firm_reports(self):
        incomes = get_financial_report('income', self.ticker, self.market, self.read_data_dir, self.write_data_dir)
        balances = get_financial_report('balance', self.ticker, self.market, self.read_data_dir, self.write_data_dir)
        cash_flows = get_financial_report('cashflow', self.ticker, self.market, self.read_data_dir, self.write_data_dir)
        setattr(self, 'incomes', incomes)
        setattr(self, 'balances', balances)
        setattr(self, 'cash_flows', cash_flows)

    def get_last_revenue(self):
        latest_incomes_publish = \
        self.incomes[self.incomes['Publish Date'] == self.incomes['Publish Date'].max()]['Publish Date'].values[0]
        latest_revenue = self.incomes[self.incomes['Publish Date'] == latest_incomes_publish]['Revenue'].values[0]
        return latest_revenue

    def last_revenue_test(self):
        return True if self.get_last_revenue() > (350 * 10 ^ 6) else False

    def get_negative_profits_last_five(self):
        today = date.today()
        curr_year = today.year
        lowest_profit = min(self.incomes[self.incomes['Fiscal Year'] > (curr_year - 5)]['Net Income (Common)'].values)
        return True if lowest_profit < 0 else False





if __name__ == '__main__':
    a_firm = Firm('A', read_data_dir=r'data')
    a_firm.get_firm_reports()
    blah = a_firm.get_last_revenue()
    print("blah")