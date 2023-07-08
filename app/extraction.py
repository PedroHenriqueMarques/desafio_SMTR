from typing import List

import pandas as pd
from requests import Response
from prefect import Flow, task, get_run_logger

from requisitions import makeRequest

@task
def get_occurrences() -> pd.DataFrame | None:
    logger = get_run_logger()
    ''' Makes a request to the API to retrieve data from open 
    occurences. Returns a pandas dataframe if the request is 
    successful, returns None, otherwise.
    '''

    url = 'https://api.dados.rio/v2/adm_cor_comando/ocorrencias_abertas/'
    response = makeRequest(url)
    response_data = response.json()
    if isinstance(response, Response):
        df = pd.DataFrame(response_data['eventos'])
        df['datetime'] = pd.to_datetime([response.headers['Date']] * df.shape[0]).tz_localize('utc').tz_convert('America/Sao_Paulo').tz_localize(None)
        logger.info('Occurrences extraction successful.')
        return df
    logger.warning('Occurrences extraction failed.')


def get_occurrences_agencies(id_list: List[int]) -> pd.DataFrame:
    ''' Makes a request to the API to retrieve data from open 
    occurences. Returns a pandas dataframe if the request is 
    successful, returns None, otherwise.
    '''

    url = 'https://api.dados.rio/v2/adm_cor_comando/ocorrencias_orgaos_responsaveis/'
    df_resps = pd.DataFrame()
    
    #  for each occurrence id, find the responsible agency.
    for ids in id_list:
        params = {'eventoId': ids}
        response = makeRequest(url, params)
        if isinstance(response, Response):
            if response.ok:
                #  appends each response to a dataframe
                df_resps = pd.concat([df_resps,
                                      pd.DataFrame(response.json()['atividades'])])
                df_resps['id'] = [ids] * df_resps.shape[0]                

    return df_resps


if __name__ == '__main__':
    with Flow('test') as flow:
        df_occur = get_occurrences()
        print(df_occur)
        if isinstance(df_occur, pd.DataFrame):
            df_agencies = get_occurrences_agencies(df_occur['id'].tolist()[0])
                                            
        else:
            df_agencies = get_occurrences_agencies([99012])
        print(df_agencies)
        flow.run()
