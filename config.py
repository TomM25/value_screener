# region display
display = {
    'Benjamin Graham': {
        'last revenue': {
            'description': 'Sales revenue > 350M',
            'display_functions': ['get_last_revenues'],
            'display_functions_desc': ['Last revenue']
        },
        'profits growth': {
            'description': '30% profits growth and not negative in the last 5 years',
            'display_functions': ['get_last_profits', 'get_4_years_profits_growth'],
            'display_functions_desc': ['5 last profits', 'Profits growth last four years']
        },
        'earnings_multiplier': {
            'description': 'Earnings multiplier lower than 15',
            'display_functions': ['get_earnings_multiplier'],
            'display_functions_desc': ['Earnings Multiplier']
        },
        'current_ratio': {
            'description': 'Current ratio higher than 2',
            'display_functions': ['get_current_ratio'],
            'display_functions_desc': ['Current ratio']
        },
        'equity_earnings': {
            'description': 'Equity multiplier times earnings multiplier lower than 22',
            'display_functions': ['get_equity_multiplier', 'get_earnings_multiplier'],
            'display_functions_desc': ['Equity multiplier', 'Earnings multiplier']
        },
        'working_capital_long_term_liabilities': {
            'description': 'Working capital higher than long term liabilities',
            'display_functions': ['get_long_term_liabilities', 'get_working_capital'],
            'display_functions_desc': ['Long term liabilities', 'Working capital']
        }
    },
    'Warren Buffet': {
        'consistent_profits_growth': {
            'description': 'EPS is constantly growing in the last 5 years, and is not negative',
            'display_functions': ['get_last_profits'],
            'display_functions_desc': ['Last 5 years common profit']
        },
        'net_income_long_liabilities': {
            'description': 'Cumulative total net income of last 5 years higher than long term liabilities',
            'display_functions': ['get_net_income_5_years', 'get_long_term_liabilities'],
            'display_functions_desc': ['Cumulative net income of 5 years', 'Long term liabilities']
        },
        'roa': {
            'description': 'ROA higher than 12%',
            'display_functions': ['get_roa'],
            'display_functions_desc': ['ROA']
        },
        'roe_5_years': {
            'description': 'ROE of last 5 years higher than 15%',
            'display_functions': ['get_average_roe'],
            'display_functions_desc': ['Average ROE of last 5 years']
        },
        'positive_fcff': {
            'description': 'Free cash flow is positive',
            'display_functions': ['get_fcff'],
            'display_functions_desc': ['FCFF']
        },
        'profits_growth_to_surplus': {
            'description': "last year's profits growth over retained earnings",
            'display_functions': ['get_last_year_net_income_growth', 'get_retained_earnings'],
            'display_functions_desc': ["Last year's net income growth", "Retained earnings"]
        }
    },
    'Peter Lynch': {
        'peg_ratio': {
            'description': 'PEG ratio lower than 1',
            'display_functions': ['get_peg_ratio'],
            'display_functions_desc': ['PEG ratio']
        },
        'debt_equity_ratio': {
            'description': 'Debt to equity ratio lower than 0.8',
            'display_functions': ['get_debt_equity_ratio', 'get_shareholders_equity', 'get_net_debt'],
            'display_functions_desc': ['Debt to equity ratio', 'Shareholders equity', 'Net debt']
        },
        'lynch_profits_growth': {
            'description': "If both the average growth (5 years) and the last growth are over 0.2 - pass. If they're both over"
                           "0.1, pass only if last year's growth is higher than the average growth. Else - fail.",
            'display_functions': ['get_avg_profit_growth', 'get_last_profits_growth_rate'],
            'display_functions_desc': ['Average profits growth rate of the last 5 years',
                                       "last year's profits growth rate"]
        },
        'inventories_revenue_growth': {
            'description': 'Growth of inventories to revenue ratio this year lower than 0.05',
            'display_functions': ['get_inventories_revenue_ratio', 'get_inventories_revenue_growth'],
            'display_functions_desc': ['Inventories to revenue ratios of last 2 years', 'Inventories to revenue ratio growth']
        },
        'positive_last_two_profits': {
            'description': 'Positive profits for the last two years',
            'display_functions': ['get_two_years_profits'],
            'display_functions_desc': ["Last two years' profits"]
        },
        'lynch_profit_revenue': {
            'description': "If last 5 years' average profits growth rate over 0.2, pass if revenue is bigger than 1B."
                           "If last 5 years' average profits growth rate positive, pass if revenue is bigger than 1.9B."
                           "Else fail.",
            'display_functions': ['get_avg_profit_growth', 'get_last_revenues'],
            'display_functions_desc': ["Last 5 years' average profits growth rate", "Last revenue"]
        }
    },
    "James P. O'shaughnessy": {
        'market_cap': {
            'description': 'Market cap higher than 150M',
            'display_functions': 'get_market_cap',
            'display_functions_desc': 'Market cap'
        },
        'market_cap_revenue': {
            'description': 'Market cap over revenue lower than 1.5',
            'display_functions': ['get_market_cap', 'get_last_revenues'],
            'display_functions_desc': ['Market cap', 'Revenue']
        }
    }
}

investor_threshold = {'Benjamin Graham': {'buy': 0.82, 'hold': 0.65},
                      'Warren Buffet': {'buy': 0.82, 'hold': 0.65},
                      'Peter Lynch': {'buy': 0.82, 'hold': 0.65}}
