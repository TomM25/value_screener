from get_financial_report import get_financial_report
from config import display


class Firm:
    def __init__(self, ticker: str, market: str='us', read_data_dir=None, write_data_dir='data'):
        self.ticker = ticker
        self.market = market
        self.read_data_dir = read_data_dir
        self.write_data_dir = write_data_dir
        self.income = get_financial_report('income', ticker, market, read_data_dir, write_data_dir)
        self.balance = get_financial_report('balance', ticker, market, read_data_dir, write_data_dir)
        self.cash_flow = get_financial_report('cashflow', ticker, market, read_data_dir, write_data_dir)
        self.curr_share_data = get_financial_report('shareprices', ticker, market, read_data_dir, write_data_dir, variant='latest')

    def get_latest_report_year(self, report_kind: str):
        if report_kind not in ['income', 'balance', 'cash_flow']:
            raise ValueError(f"A report named {report_kind} does not exist")
        report = getattr(self, report_kind)
        return report[report['Fiscal Year'] == report['Fiscal Year'].max()]['Fiscal Year'].values[0]

    def get_latest_annual_data(self, report_kind: str, column: str, years_back: int):
        latest_year = self.get_latest_report_year(report_kind)
        earliest_year = latest_year - years_back
        report = getattr(self, report_kind)
        return report[report['Fiscal Year'] > earliest_year][column].values

    def get_last_revenue(self):
        return self.get_latest_annual_data(report_kind='income', column='Revenue', years_back=1)

    def last_revenue_test(self):
        return self.get_last_revenue() > (350 * 10 ^ 6)

    def get_last_profits(self, years_back: int=5):
        return self.get_latest_annual_data(report_kind='income', column='Net Income (Common)', years_back=years_back)

    def positive_last_profits_test(self, years_back: int=5):
        # Was the profit constantly positive during the time period?
        # TODO ask Yotam if this is relevant
        lowest_profit = min(self.get_last_profits(years_back=years_back))
        return lowest_profit > 0

    def consistent_profits_growth_test(self, years_back: int=5):
        # Was the profit growth constantly positive during the time period?
        profits = self.get_last_profits(years_back=years_back)
        for index, profit in enumerate(profits[:-1]):
            if profits[index + 1] < profit:
                return False
        return True

    def get_profits_growth(self, years_back: int=4):
        # TODO verify computation with Yotam
        profits = self.get_last_profits(years_back=years_back)
        return ((profits[-1] + profits[-2])/(profits[-3] + profits[-4])) - 1

    def profits_growth_test(self, years_back: int=4, threshold: float=0.3):
        # Is the profit growth rate higher than the threshold
        if not self.consistent_profits_growth_test(years_back=5):
            return False
        return self.get_profits_growth(years_back=years_back) > threshold

    def get_eps(self):
        shares_num = self.curr_share_data['Shares Outstanding'].values[0]
        profit = self.get_last_profits(years_back=1)[0]
        return profit / shares_num

    def get_earnings_multiplier(self):
        curr_price = self.curr_share_data['Close']
        return curr_price / self.get_eps()

    def earnings_multiplier_test(self, threshold: float=15.0):
        # Is the multiplier lower than a defined threshold
        if not isinstance(threshold, int) or isinstance(threshold, float):
            return ValueError(f"Threshold arg must be numeric. The argument that was passed is {threshold}")
        return self.get_earnings_multiplier() < threshold

    def get_current_ratio(self):
        current_assets = \
            self.get_latest_annual_data(report_kind='balance', column='Total Current Assets', years_back=1)[0]
        current_liabilities = \
            self.get_latest_annual_data(report_kind='balance', column='Total Current Liabilities', years_back=1)[0]
        return current_assets / current_liabilities

    def current_ratio_test(self, threshold: float=2):
        # Is the current ratio higher than a defined threshold
        return self.get_current_ratio() > threshold

    def get_equity_multiplier(self):
        total_assets = self.get_latest_annual_data(report_kind='balance', column='Total Assets', years_back=1)[0]
        total_liabilities = self.get_latest_annual_data(report_kind='balance', column='Total Assets', years_back=1)[0]
        shareholders_equity = total_assets - total_liabilities
        return total_assets / shareholders_equity

    def equity_earnings_test(self, threshold: float=22.0):
        # Is the product of the earnings multiplier and the equity multiplier lower than a defined threshold
        return (self.get_earnings_multiplier() * self.get_equity_multiplier()) < threshold

    def get_working_capital(self):
        current_assets = self.get_latest_annual_data(report_kind='balance', column='Total Current Assets', years_back=1)[0]
        current_liabilities  = self.get_latest_annual_data(report_kind='balance', column='Total Current Liabilities', years_back=1)[0]
        return current_assets - current_liabilities

    def get_long_term_liabilities(self):
        return self.get_latest_annual_data(report_kind='balance', column='Total Noncurrent Liabilities', years_back=1)[0]

    def working_capital_long_term_liabilities_test(self):
        # Is the working capital higher than the long term liabilities?
        return self.get_working_capital() > self.get_long_term_liabilities()

    # def generate_firm_report(self):
    #     df_list = list()
    #     for investor in display.keys():
    #         for test in investor_tests:
    #             for display_func in test['display_functions']:
    #                 firm_func = getattr(self, display_func)
    #             test_dict = {'Test_description': test['description']}


# if __name__ == '__main__':
#     apple = Firm(ticker='AAPL', read_data_dir='data')
#     # curr_ratio = apple.get_current_ratio()
#     test = apple.working_capital_long_term_liabilities_test()
#     print("blah")
