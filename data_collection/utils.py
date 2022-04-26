## Auxiliar methods

# -------------- Imports -------------

import requests



# -------------- Auxiliar functions ----

## Try do a request
def try_request(endpoint, params={}, timeout=30, attempts=10):
    for i in range(attempts):
        try:
            request = requests.get(endpoint, params=params, timeout=timeout*((i+1)*2))
            if request.status_code == 404: return False
            if request.status_code == 429:  # too many requests
                time.sleep(10)
            if request.status_code != 200:
                raise Exception("Bad status code %s" % request.status_code)
            if 'Ã' in request.text and not "ç" in request.text:
                request.encoding = "utf-8"
            return request
        except Exception as e:
            print("[%s] for [%s] (attempt %d/%d)" % (e, params, i + 1, attempts))
    if not request or request.status_code == 500: return False # end of attempts