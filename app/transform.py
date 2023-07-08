import pandas as pd
from prefect import task


@task
def combine_occurrences_agencies(df_occur: pd.DataFrame,
                                 df_agencies: pd.DataFrame) -> pd.DataFrame:
    ''' Joins the occurrences dataframe with the agencies dataframe by 
    the occurrence id. Returns a pandas dataframe.
    '''

    #  Performs left join on occurrences dataframe, using natural join on id.
    df = df_occur.merge(df_agencies,
                        how='left',
                        left_on='id',
                        right_on='id',
                        suffixes=('_event', '_agent'))

    #  Drops all columns but the ones in the list below.
    col_names = ['titulo', 'id', 'datetime', 'orgao', 'status_agent']
    df.drop(columns=set(df.columns).difference(set(col_names)), inplace=True)

    #  Keeps only occurrences which are dealt by CET-RIO.
    df = df.loc[df['orgao'] == 'CET-RIO', :]

    return df


@task
def create_occurrences_report(df_occur: pd.DataFrame,
                              df_occur_agencies: pd.DataFrame) -> pd.DataFrame:
    ''' Creates a dataframe on the format required by the challenge.
    Returns a pandas dataframe.
    '''
    #  Forms a dataframe from the grouping by of titulo counting status_agent
    df_rep = pd.DataFrame(df_occur_agencies.groupby('titulo')
                          ['status_agent'].value_counts())
    df_rep = df_rep.reset_index(allow_duplicates=True)

    #  Merges the datetime with the grouping dataframe on the titulo 
    df_rep = df_rep.merge(df_occur.loc[:, ['titulo', 'datetime']], 
                            left_on='titulo', 
                            right_on='titulo')
    
    df_rep.drop_duplicates(inplace=True)
    df_rep.columns = ['tipo_ocorrencia', 
                      'status_ocorrencia',
                      'quantidade_ocorrencia', 
                      'datetime']
    
    #  Reorders the dataframe
    df_rep = df_rep[['datetime', 
                     'tipo_ocorrencia',
                     'status_ocorrencia', 
                     'quantidade_ocorrencia']]
    
    return df_rep
