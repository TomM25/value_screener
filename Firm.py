from get_financial_report import get_financial_report


class Firm:
    def __init__(self, ticker, market='us', read_data_dir=None, write_data_dir='data'):
        self.ticker = ticker
        self.market = market
        self.read_data_dir = read_data_dir
        self.write_data_dir = write_data_dir
        self.income = get_financial_report('income', ticker, market, read_data_dir, write_data_dir)
        self.balance = get_financial_report('balance', ticker, market, read_data_dir, write_data_dir)
        self.cash_flow = get_financial_report('cashflow', ticker, market, read_data_dir, write_data_dir)
        self.curr_share_price = get_financial_report('shareprices', ticker, market, read_data_dir, write_data_dir, variant='latest')

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

    def get_last_profits(self, years_back=5):
        return self.get_latest_annual_data(report_kind='income', column='Net Income (Common)', years_back=years_back)

    def positive_last_profits_test(self, years_back=5):
        # Was the profit constantly positive during the time period?
        # TODO ask Yotam if this is relevant
        lowest_profit = min(self.get_last_profits(years_back=years_back))
        return lowest_profit > 0

    def consistent_profits_growth_test(self, years_back=5):
        # Was the profit growth constantly positive during the time period?
        profits = self.get_last_profits(years_back=years_back)
        for index, profit in enumerate(profits[:-1]):
            if profits[index + 1] < profit:
                return False
        return True

    def get_profits_growth(self, years_back=4):
        # TODO verify computation with Yotam
        profits = self.get_last_profits(years_back=years_back)
        return ((profits[-1] + profits[-2])/(profits[-3] + profits[-4])) - 1

    def profits_growth_test(self, years_back=4, threshold=0.3):
        # Is the profit growth rate higher than the threshold
        return self.get_profits_growth(years_back=years_back) > threshold
