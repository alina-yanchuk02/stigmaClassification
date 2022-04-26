"""
Automatic classification of stigmatizing mental illness articles in online news journals - April 2022
Author: Alina Yanchuk - alinayanchuk@ua.pt
"""

### Search with Arquivo.pt TextSearch API


# -------------- Imports -------------

from utils import try_request


# -------------- Main functions ------
    
## Search by text query. Return list with extracted URLs.  
def search(query_terms, site_search, _from=1996, _to=2021, page_type="html", max_items=2000, fields="title,tstamp,originalURL,linkToOriginalFile,linkToArchive", pretty_print="false", next_page=False):
    endpoint = "https://arquivo.pt/textsearch"
    timeout = 30
    attempts = 1
    params = {
        "q": query_terms,
        "from": _from,
        "to": _to,
        "type": page_type,
        "siteSearch": site_search,
        "maxItems": max_items,
        "fields": fields,
        "prettyPrint": pretty_print,
    }
    items = []

    response = try_request(endpoint=endpoint, params=params, timeout=timeout, attempts=attempts)
    response = response.json()
    if not response: return []

    for result in response["response_items"]: 
        item = {}
        item["title"]=result["title"]
        item["linkToArchive"]=result["linkToArchive"]
        item["tstamp"]=result["tstamp"]
        item["originalURL"]=result["originalURL"]
        item["linkToOriginalFile"]=result["linkToOriginalFile"]
        items.append(item)

    if next_page==True:
        while (True):
            if "next_page" in response: 
                next_page_link = response["next_page"]
                response = try_request(endpoint=next_page_link, timeout=timeout, attempts=attempts)
                response = response.json()
                if response: 
                    for result in response["response_items"]: 
                        item = {}
                        item["title"]=result["title"]
                        item["tstamp"]=result["tstamp"]
                        item["originalURL"]=result["originalURL"]
                        item["linkToOriginalFile"]=result["linkToOriginalFile"]
                        items.append(item)
            else: break

    #print("Nº of pages for "+site_search+" | "+query+" : "+str(len(items)))
    return items
