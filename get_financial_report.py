import os
import simfin as sf

from utils.logger import get_logger

logger = get_logger(__name__)

sf.set_api_key(api_key=os.environ.get('SIMFIN_KEY', 'free'))


def get_financial_report(report_kind, ticker, market='us', data_dir='data', variant='annual'):
    sf.set_data_dir(data_dir)
    all_firms = sf.load(dataset=report_kind, variant=variant, market=market)
    all_firms.reset_index(inplace=True)
    ticker_report = all_firms[all_firms['Ticker'] == ticker]
    logger.info(f"Got {len(ticker_report)} {report_kind} records for firm {ticker}")
    return ticker_report
