import os.path
import pandas as pd
from prefect import task


@task
def export_to_csv(df: pd.DataFrame, csv_file: str | None = None) -> None:
    '''Exports a dataframe to a CSV file. If there is a csv file name
    passed, then appends to the csv file. If not, creates a new csv 
    file with a default name.
    '''

    if csv_file:
        df.to_csv(csv_file, 
                mode='a', 
                index=False, 
                header=False) 
    else:
        df.to_csv(os.path.join(
            os.path.dirname(os.path.abspath(__file__)),'exports/report.csv'), 
            index=False)    
