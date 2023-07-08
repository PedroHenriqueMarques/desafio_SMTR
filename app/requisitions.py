import time
from typing import Dict

import requests


def makeRequest(url: str, 
                params: Dict | None = None,
                count: int | None = None,
                timeout: int | None = None,
                max_tries: int | None = None) -> requests.Response:
    ''' Makes a request to <url>, using <params>, for up to <max_tries>
    times. Returns a Response object.
    '''

    if not max_tries:
        max_tries = 5

    if not timeout:
        timeout = 10
    
    if not count:
        count = 0

    if count >= max_tries:
        return requests.get(url, params=params, timeout=timeout)
    
    try:
        res = requests.get(url, params=params, timeout=timeout)
        if res.status_code >= 500:
            raise requests.exceptions.HTTPError(
                f'Internal server error. Code: {res.status_code}')
    #  in case there is a http error, try again
    except requests.exceptions.HTTPError:
        time.sleep(count + 1)
        res = makeRequest(url, 
                          params=params, 
                          count=count + 1, 
                          timeout=timeout, 
                          max_tries=max_tries)

    #  for unexpected errors, don't return
    except requests.exceptions.RequestException as requestError:
        return requestError

    else:
        return res


if __name__ == '__main__':
    url = 'https://api.dados.rio/v2/adm_cor_comando/ocorrencias_abertas/'
    response = makeRequest(url)
    print(response.status_code)
    print(response.headers)
    print(response.json())
