from os import path
import pandas as pd
import simfin as sf

from utils.logger import get_logger

logger = get_logger(__name__)

sf.set_api_key(api_key='free')


def get_financial_report(report_kind, ticker, market='us', read_data_dir=None, write_data_dir='data', variant='annual'):
    if pd.isnull(read_data_dir):
        logger.info(
            f"Reading {report_kind} dataset of market {market} from simfin api. Data will be written to {write_data_dir}")
        sf.set_data_dir(write_data_dir)
        all_firms = sf.load(dataset=report_kind, variant=variant, market=market)
        all_firms.reset_index(inplace=True)
        ticker_report = all_firms[all_firms['Ticker'] == ticker]
        logger.info(f"Got {len(ticker_report)} {report_kind} records for firm {ticker}")
        return ticker_report
    else:
        logger.info(f"Reading {report_kind} dataset of market {market} from dir {read_data_dir}")
        file_name = f"{market}-{report_kind}-{variant}.csv"
        report_file_path = path.join(read_data_dir, file_name)
        all_firms = pd.read_csv(report_file_path, sep=';')
        ticker_report = all_firms[all_firms['Ticker'] == ticker]
        logger.info(f"Got {len(ticker_report)} {report_kind} records for firm {ticker}")
        return ticker_report
