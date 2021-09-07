from os import path
import pandas as pd
import simfin as sf

from utils.logger import get_logger

logger = get_logger(__name__)

sf.set_api_key(api_key='free')


def get_financial_report(report_kind, ticker, market='us', read_data_dir=None, write_data_dir='data'):
    if pd.isnull(read_data_dir):
        logger.info(
            f"Reading {report_kind} dataset of market {market} from simfin api. Data will be written to {write_data_dir}")
        sf.set_data_dir(write_data_dir)
        all_firms = sf.load(dataset=report_kind, variant='annual', market=market)
        logger.info(f"Got all firms' {report_kind} data. Now filtering for ticker {ticker} only")
        all_firms.reset_index(inplace=True)
        ticker_report = all_firms[all_firms['Ticker'] == ticker]
        return ticker_report
    else:
        logger.info(f"Reading {report_kind} dataset of market {market} from dir {read_data_dir}")
        file_name = f"{market}-{report_kind}-annual.csv"
        report_file_path = path.join(read_data_dir, file_name)
        all_firms = pd.read_csv(report_file_path, sep=';')
        logger.info(f"Got all firms' {report_kind} data. Now filtering for ticker {ticker} only")
        ticker_report = all_firms[all_firms['Ticker'] == ticker]
        return ticker_report


