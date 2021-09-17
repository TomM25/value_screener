import numpy as np
import pandas as pd

from get_financial_report import get_financial_report
from config import display, investor_threshold


class Firm:
    """
    Represents a publicly traded firm. This class reads the firm's last annual financial
    statements (income statement, balance sheet and cashflow statement) and some basic
    data about the firm's stock value from Simfin's API. Using this data, it allows the
    calculation of financial metrics and relations, to help decide whether the firm's
    stock should be bought, sold, or held. To summarize the calculations, it allows
    generating a conclusive report.
    The metrics and relations in the report are all based on benchmarks that were defined
    by famous investors: Benjamin Graham, Warren Buffet, Peter Lynch and James P
    O'shaughnessy.
    Methods that start with the word 'get' are used to calculate a ratio or a metric.
    Methods that end with the word 'test' are used to check if the stock is attractive
    according to a specific benchmark, and return a boolean value.

    Attributes
    ----------
    ticker: str
        The firm's ticker
    market: str
        The market where the firm is traded
    read_data_dir: str (default=None)
        A path from which the data will be read. Use this argument in case that you already read the data from Simfin's
        API, and have it locally stored.
    write_data_dir: str (default='data')
        A path to a directory where the data from Simfin's API will be written to once downloaded.

    Methods
    ---------
    generate_firm_report()
        Generates a report with financial ratios and metrics for the firm, including buy/
        sell/hold recommendations according to famous investors' benchmarks.


    """
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
        report.sort_values(by='Fiscal Year', ascending=False, inplace=True)
        values = report[report['Fiscal Year'] > earliest_year][column].values
        values = np.nan_to_num(values, nan=0)
        if len(values) == 1:
            return values[0]
        else:
            return values

    def get_last_revenues(self, years_back: int=1):
        return self.get_latest_annual_data(report_kind='income', column='Revenue', years_back=years_back)

    def last_revenue_test(self):
        return bool(self.get_last_revenues() > (350 * 10 ^ 6))

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
            if (profit < 0) or (profits[index + 1] > profit):
                return False
        return True

    def get_4_years_profits_growth(self):
        # TODO verify computation with Yotam
        profits = self.get_last_profits(years_back=5)
        return ((profits[0] + profits[-1])/(profits[-2] + profits[-3])) - 1

    def get_profits_growth_array(self, years_back: int=5):
        growth_list = list()
        profits = self.get_last_profits(years_back=years_back)
        for index, profit in enumerate(profits[:-1]):
            ratio = (profits[index] / profits[index + 1])
            percentage = ratio - 1 if ratio > 0 else ratio + 1
            growth_list.append(percentage)
        return np.array(growth_list)

    def get_avg_profit_growth(self, years_back=5):
        growth_array = self.get_profits_growth_array(years_back=years_back)
        return np.mean(growth_array)

    def profits_growth_test(self, threshold: float=0.3):
        # Is the profit growth rate higher than the threshold
        if not self.consistent_profits_growth_test(years_back=5):
            return False
        return self.get_4_years_profits_growth() > threshold

    def get_eps(self):
        shares_num = self.curr_share_data['Shares Outstanding'].values[0]
        profit = self.get_last_profits(years_back=1)
        return profit / shares_num

    def get_current_stock_price(self):
        return self.curr_share_data['Close'].values[0]

    def get_earnings_multiplier(self):
        return self.get_current_stock_price() / self.get_eps()

    def earnings_multiplier_test(self, threshold: float=15.0):
        # Is the multiplier lower than a defined threshold
        if not (isinstance(threshold, int) or isinstance(threshold, float)):
            return ValueError(f"Threshold arg must be numeric. The argument that was passed is {threshold}")
        return self.get_earnings_multiplier() < threshold

    def get_current_ratio(self):
        current_assets = \
            self.get_latest_annual_data(report_kind='balance', column='Total Current Assets', years_back=1)
        current_liabilities = \
            self.get_latest_annual_data(report_kind='balance', column='Total Current Liabilities', years_back=1)
        return current_assets / current_liabilities

    def current_ratio_test(self, threshold: float=2):
        # Is the current ratio higher than a defined threshold
        return self.get_current_ratio() > threshold

    def get_shareholders_equity(self, years_back: int=1):
        total_assets = self.get_latest_annual_data(report_kind='balance', column='Total Assets', years_back=years_back)
        total_liabilities = \
        self.get_latest_annual_data(report_kind='balance', column='Total Liabilities', years_back=years_back)
        return total_assets - total_liabilities

    def get_equity_multiplier(self):
        total_assets = self.get_latest_annual_data(report_kind='balance', column='Total Assets', years_back=1)
        shareholders_equity = self.get_shareholders_equity(years_back=1)
        return total_assets / shareholders_equity

    def equity_earnings_test(self, threshold: float=22.0):
        # Is the product of the earnings multiplier and the equity multiplier lower than a defined threshold
        return (self.get_earnings_multiplier() * self.get_equity_multiplier()) < threshold

    def get_working_capital(self, years_back: int=1):
        current_assets = self.get_latest_annual_data(report_kind='balance', column='Total Current Assets', years_back=years_back)
        current_liabilities = self.get_latest_annual_data(report_kind='balance', column='Total Current Liabilities', years_back=years_back)
        return current_assets - current_liabilities

    def get_delta_working_capital(self):
        working_capital = self.get_working_capital(years_back=2)
        return working_capital[0] - working_capital[1]

    def get_long_term_liabilities(self):
        return self.get_latest_annual_data(report_kind='balance', column='Total Noncurrent Liabilities', years_back=1)

    def working_capital_long_term_liabilities_test(self):
        # Is the working capital higher than the long term liabilities?
        return bool(self.get_working_capital() > self.get_long_term_liabilities())

    def get_tax_rate(self):
        pre_tax_income = self.get_latest_annual_data(report_kind='income', column='Pretax Income (Loss)', years_back=1)
        income_tax_expense = self.get_latest_annual_data(report_kind='income', column='Income Tax (Expense) Benefit, Net',
                                                         years_back=1)
        return ((-1) * income_tax_expense) / pre_tax_income

    def get_nopat(self):
        tax_rate = self.get_tax_rate()
        operating_income = self.get_latest_annual_data(report_kind='income', column='Operating Income (Loss)',
                                                         years_back=1)
        return operating_income * (1-tax_rate)

    def get_capex(self):
        depreciation_amortization = \
        self.get_latest_annual_data(report_kind='income', column='Depreciation & Amortization',
                                    years_back=1)
        PPE = self.get_latest_annual_data(report_kind='balance', column='Property, Plant & Equipment, Net',
                                          years_back=2)
        return PPE[0] - PPE[1] + depreciation_amortization

    def get_fcff(self):
        nopat = self.get_nopat()
        depreciation_amortization = self.get_latest_annual_data(report_kind='income', column='Depreciation & Amortization',
                                                                years_back=1)
        capex = self.get_capex()
        delta_working_capital = self.get_delta_working_capital()
        return nopat + depreciation_amortization - capex - delta_working_capital

    def positive_fcff_test(self):
        return self.get_fcff() > 0

    def get_roa(self):
        net_income = self.get_latest_annual_data(report_kind='income', column='Net Income', years_back=1)
        total_assets = self.get_latest_annual_data(report_kind='balance', column='Total Assets', years_back=1)
        return net_income / total_assets

    def roa_test(self, threshold: int=0.12):
        return self.get_roa() > threshold

    def get_average_roe(self, years_back: int=5):
        net_income = self.get_latest_annual_data(report_kind='income', column='Net Income', years_back=years_back)
        shareholders_equity = self.get_shareholders_equity(years_back=years_back)
        roe_array = net_income / shareholders_equity
        return np.mean(roe_array)

    def roe_5_years_test(self, threshold: int=0.15):
        return self.get_average_roe() > threshold

    def get_net_income_5_years(self):
        net_income = self.get_latest_annual_data(report_kind='income', column='Net Income', years_back=5)
        return np.sum(net_income)

    def net_income_long_liabilities_test(self):
        net_income_sum = self.get_net_income_5_years()
        long_term_liabilities = self.get_long_term_liabilities()
        return net_income_sum > long_term_liabilities

    def get_last_year_net_income_growth(self):
        net_income = self.get_latest_annual_data(report_kind='income', column='Net Income', years_back=2)
        return net_income[0] - net_income[1]

    def get_retained_earnings(self, years_back: int=1):
        return self.get_latest_annual_data(report_kind='balance', column='Retained Earnings', years_back=years_back)

    def get_profits_growth_to_surplus(self):
        return self.get_last_year_net_income_growth() / self.get_retained_earnings()

    def profits_growth_to_surplus_test(self, threshold: float=0.12):
        return self.get_profits_growth_to_surplus() > threshold

    def get_pe_ratio(self):
        return self.get_current_stock_price() / self.get_eps()

    def get_peg_ratio(self):
        return self.get_pe_ratio() / self.get_avg_profit_growth()

    def peg_ratio_test(self, threshold: float=1.0):
        return self.get_peg_ratio() < threshold

    def get_net_debt(self):
        short_term_debt = self.get_latest_annual_data(report_kind='balance', column='Short Term Debt', years_back=1)
        long_term_debt = self.get_latest_annual_data(report_kind='balance', column='Long Term Debt', years_back=1)
        cash_and_equivalents = self.get_latest_annual_data(report_kind='balance',
                                                           column='Cash, Cash Equivalents & Short Term Investments',
                                                           years_back=1)
        return short_term_debt + long_term_debt - cash_and_equivalents

    def get_debt_equity_ratio(self):
        return self.get_net_debt() / self.get_shareholders_equity()

    def debt_equity_ratio_test(self, threshold: float=0.8):
        return self.get_debt_equity_ratio() < threshold

    def get_last_profits_growth_rate(self):
        return self.get_profits_growth_array()[0]

    def lynch_profits_growth_test(self, years_back: int=5):
        avg_profits_growth = self.get_avg_profit_growth(years_back=years_back)
        last_profits_growth = self.get_last_profits_growth_rate()
        if avg_profits_growth > 0.2 and last_profits_growth > 0.2:
            return True
        elif avg_profits_growth > 0.1 and last_profits_growth > 0.1:
            if last_profits_growth > avg_profits_growth:
                return True
            else:
                return False
        else:
            return False

    def get_last_inventories(self, years_back: int=2):
        return self.get_latest_annual_data(report_kind='balance', column='Inventories', years_back=years_back)

    def get_inventories_revenue_ratio(self, years_back: int=2):
        revenues = self.get_last_revenues(years_back=years_back)
        inventories = self.get_last_inventories(years_back=years_back)
        return inventories / revenues

    def get_inventories_revenue_growth(self):
        ratio_array = self.get_inventories_revenue_ratio(years_back=2)
        return (ratio_array[0] / ratio_array[1]) - 1

    def inventories_revenue_growth_test(self, threshold: float=0.05):
        growth_rate = self.get_inventories_revenue_growth()
        return growth_rate < threshold

    def get_two_years_profits(self):
        return self.get_last_profits(years_back=2)

    def positive_last_two_profits_test(self):
        return np.min(self.get_two_years_profits()) > 0

    def lynch_profit_revenue_test(self, years_back: int=5):
        avg_profits_growth = self.get_avg_profit_growth(years_back=years_back)
        revenue = self.get_last_revenues(years_back=1)
        if avg_profits_growth > 0.2:
            return revenue > (1000 * 10 ^ 6)
        elif avg_profits_growth > 0:
            return revenue > (1900 * 10 ^ 6)
        else:
            return False

    def get_market_cap(self):
        stock_price = self.get_current_stock_price()
        stocks_num = self.curr_share_data['Shares Outstanding'].values[0]
        return stock_price * stocks_num

    def market_cap_test(self, threshold: int=150000000):
        return self.get_market_cap() > threshold

    def get_market_cap_revenue(self):
        return self.get_market_cap() / self.get_last_revenues()

    def market_cap_revenue_test(self, threshold: float=1.5):
        return self.get_market_cap_revenue() < threshold

    def get_market_cap_revenue_entire_market(self):
        # TODO ask Yotam where to find this data and replace the constant
        return 2.28

    def market_cap_revenue_market_comparison_test(self):
        return self.get_market_cap_revenue() < self.get_market_cap_revenue_entire_market()

    @staticmethod
    def check_investor_threshold(value, investor: str):
        if value > investor_threshold[investor]['buy']:
            return 'buy'
        elif value > investor_threshold[investor]['hold']:
            return 'hold'
        else:
            return 'sell'

    def summarize_investor_test(self, df: pd.DataFrame):
        investor_pass_count = df.groupby('investor')['test_passed'].sum().rename('investor_test_pass_rate')
        for investor in df['investor'].unique():
            investor_test_num = len(df[df['investor'] == investor])
            investor_pass_count.at[investor] /= investor_test_num
        df = pd.merge(left=df, right=investor_pass_count, how='left', left_on='investor', right_on='investor')
        df['investor_recommendation'] = df.apply(
            lambda row: self.check_investor_threshold(row['investor_test_pass_rate'], row['investor']), axis=1)
        return df

    def generate_firm_report(self) -> pd.DataFrame:
        '''
        Generate a conclusive report about the firm, including the display of
        financial metrics and relations, based on Benchmarks that were defined
        by famous investors.

        Returns
        ---------
            report (pd.DataFrame): A conclusive report about the firm
        '''
        df_list = list()
        for investor in display.keys():
            for test in display[investor]:
                test_dict = dict()
                desc_dict = dict()
                test_func_name = '_'.join(test.split()) + '_test'
                test_func = getattr(self, test_func_name)
                test_passed = test_func()
                test_dict.update({'investor': investor, 'test_name': test, 'description': display[investor][test]['description'],
                                  'test_passed': test_passed})
                for idx, display_func in enumerate(display[investor][test]['display_functions']):
                    test_disp_func = getattr(self, display_func)
                    disp_func_val = test_disp_func()
                    if isinstance(disp_func_val, np.ndarray):
                        disp_func_val = list(disp_func_val)
                    desc_dict.update({display[investor][test]['display_functions_desc'][idx]: disp_func_val})
                test_dict.update({'related_values': desc_dict})
                df_list.append(test_dict)
        summary_df = pd.DataFrame(df_list)
        summary_df = self.summarize_investor_test(summary_df)
        return summary_df


if __name__ == '__main__':
    apple = Firm(ticker='AAPL') #, read_data_dir='data'
    # curr_ratio = apple.get_current_ratio()
    test = apple.generate_firm_report()
    print("blah")
