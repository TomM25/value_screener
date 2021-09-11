# region display
display = {
    'Benjamin Graham': {
        'last revenue': {
            'description': 'Sales revenue > 350M',
            'display_functions': ['get_last_revenue'],
            'display_functions_desc': ['last_revenue']
        },
        'profits growth': {
            'description': '30% EPS growth and not negative in the last 5 years',
            'display_functions': ['get_last_profits', 'get_profits_growth'],
            'display_functions_desc': ['5 last profits', 'profits growth last two years']
        },
        'earnings_multiplier': {
            'description': 'Earnings multiplier lower than 15',
            'display_functions': ['get_earnings_multiplier'],
            'display_functions_desc': ['earnings_multiplier']
        },
        'current_ratio': {
            'description': 'Current ratio higher than 2',
            'display_functions': ['get_current_ratio'],
            'display_functions_desc': ['current_ratio']
        },
        'equity_earnings': {
            'description': 'Equity multiplier times earnings multiplier lower than 22',
            'display_functions': ['get_equity_multiplier', 'get_earnings_multiplier'],
            'display_functions_desc': ['equity_multiplier', 'earnings_multiplier']
        },
        'working_capital_long_term_liabilities': {
            'description': 'Working capital higher than long term liabilities',
            'display_functions': ['get_long_term_liabilities', 'get_working_capital'],
            'display_functions_desc': ['long_term_liabilities', 'working_capital']
        }
    }}
