import os
import simfin as sf

from utils.logger import get_logger

logger = get_logger(__name__)

sf.set_api_key(api_key=os.environ.get('SIMFIN_KEY', 'free'))


def get_financial_markets(data_dir: str='data'):
    logger.info("Loading a list of the financial markets")
    sf.set_data_dir(data_dir)
    markets_df = sf.load_markets()
    return {val: key for key, val in markets_df['Market Name'].items()}
