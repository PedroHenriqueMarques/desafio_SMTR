import os

from prefect import flow, get_run_logger

import extraction as ext
from parallelization import parallel_function
import transform as tr
from exporter import export_to_csv

@flow
def run_etl():
    logger = get_run_logger()
    logger.info('Starting extraction.')
    df_occur = ext.get_occurrences()
    df_agencies = parallel_function(ext.get_occurrences_agencies, 
                                    df_occur['id'].tolist())

    df_occur_agencies = tr.combine_occurrences_agencies(df_occur, df_agencies)
    df_rep = tr.create_occurrences_report(df_occur, df_occur_agencies)
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'exports')
    with os.scandir(path) as dir:
        dir_names = [d.name for d in dir]
    if 'report.csv' in dir_names:
        export_to_csv(df_rep, os.path.join(path,'report.csv'))
        logger.info("Appending to 'report.csv'")
    else:
        logger.info("'report.csv' not found. Creating 'report.csv'")
        export_to_csv(df_rep)

if __name__ == "__main__":
    run_etl()