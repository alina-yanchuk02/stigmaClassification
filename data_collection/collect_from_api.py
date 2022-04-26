"""
Automatic classification of stigmatizing mental illness articles in online news journals - April 2022
Author: Alina Yanchuk - alinayanchuk@ua.pt
"""

### Collect and save relevant data from Arquivo.pt TextSearch API 


# -------------- Imports -------------

import json

from search import search

from web_scraping import get_data

import concurrent.futures

import time

import csv


# -------------- Main functions ------
    
## Collect URLs from API, perform web scraping and write to CSV
def collect():

    urls_to_scrap = {}

    terms = ["esquizofrenia", "esquizofrénico", "esquizofrenico", "esquizofrénica", "esquizofrenica", "esquizofrénicas", "esquizofrenicas", "esquizofrénicos", "esquizofrenicos", "esquizofrenicamente", "esquizofrenizar", "psicose", "psicótica", "psicotica", "psicóticas", "psicoticas", "psicótico", "psicotico", "psicóticos", "psicóticos"]
    journals = ["publico.pt", "www.publico.pt", "jornal.publico.pt", "dossiers.publico.pt", "desporto.publico.pt", "www.publico.clix.pt", "digital.publico.pt", "blogues.publico.pt", "economia.publico.pt", "m.publico.pt", "ultimahora.publico.pt", "observador.pt", "www.dn.pt", "dn.sapo.pt", "www.dn.sapo.pt", "expresso.pt", "aeiou.expresso.pt", "expresso.sapo.pt", "www.correiodamanha.pt", "www.cmjornal.xl.pt", "www.cmjornal.pt", "www.jn.pt", "jn.pt", "jn.sapo.pt", "abola.pt", "www.abola.pt", "abola.pt:80", "aeiou.visao.pt", "visao.sapo.pt", "www.sabado.pt", "www.sabado.xl.pt", "www.sabado.xl.pt:80", "sabado.pt"]

    total_urls = 0

    duplicate = False

    data = []

    for journal in journals:
        for term in terms:         
            items = search(query_terms = term, site_search = journal, max_items = 2000, next_page = False)
            for item in items:
                if journal in item["linkToOriginalFile"]: # if the returned url really corresponds to this journal
                    if journal in urls_to_scrap: 
                        for element in urls_to_scrap[journal]: # deduplication
                            if element["linkToArchive"] == item["linkToArchive"]: 
                                duplicate = True
                                break
                        if duplicate == False: 
                            item["journal"]=journal
                            urls_to_scrap[journal].append(item)
                            total_urls += 1
                        else: duplicate = False
                    else: 
                        item["journal"]=journal
                        urls_to_scrap[journal]=[item]
                        total_urls+=1
                else: # if the returned url corresponds to another journal
                    for j in journals: # search for this journal
                        if j in str(item["linkToOriginalFile"]):
                            if j in urls_to_scrap: 
                                for element in urls_to_scrap[j]: # deduplication by "linkToArchive"
                                    if element["linkToArchive"] == item["linkToArchive"]: 
                                        duplicate = True
                                        break
                                if duplicate == False: 
                                    item["journal"]=j
                                    urls_to_scrap[j].append(item)
                                    total_urls += 1
                                else: duplicate = False
                            else: 
                                item["journal"]=j
                                urls_to_scrap[j] = [item]
                                total_urls += 1

    print("Number of urls extracted: " + str(total_urls) + "\n")

    print("Begin scraping...\n")

    start_time = time.time()
    
    for journal in urls_to_scrap:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for data_scraped in executor.map(get_data, urls_to_scrap[journal]):
                if data_scraped!=None: 
                    data.append(data_scraped)
    
    end_time = time.time()

    print("Web scraping took " + str(end_time-start_time) + " seconds.\n\n")

    #with open('output_scraping', 'w') as scraping_file: json.dump(data, scraping_file)
    #scraping_file.close()
    #with open('output_scraping') as scraping_file: data = json.load(scraping_file)
    #scraping_file.close()

    data = deduplicate(data, terms)

    write_to_file(data)

    results(data)
    


# -------------- Auxiliar functions ------

## Write to csv
def write_to_file(data):

    csv_columns = ['label','journal','headline','content','authors','publishDate','archiveDate','linkToArchive']

    with open("data.csv", 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for entry in data:
            writer.writerow(entry)
    csvfile.close()


## Remove duplicate news, by content or headline
def deduplicate(data, terms):
  
    temp = []
    duplicate = False

    for entry in data:
        if len(temp) != 0:
            for entry_temp in temp:
                equal = 0
                if len(entry["content"]) <= len(entry_temp["content"]): # if one string is smaller or equal
                    if entry["content"] in entry_temp["content"]: # check if substring is in the string
                        duplicate = True
                        break
                if len(entry_temp["content"]) <= len(entry["content"]): # if the other string is smaller or equal
                    if entry_temp["content"] in entry["content"]: 
                        duplicate = True
                        break
                text_part = entry["content"].split('.') # if the sencence with one of the target terms (in the list terms) and the two sentences before and the two sentences after the target sentence of one string are in the second string
                target = next((s for s in text_part if any(term in s for term in terms)), "")
                if target!="":
                    target_index = text_part.index(target)
                    if target_index-1>=0: 
                        if text_part[target_index-1] in entry_temp["content"]: equal+=1
                    if target_index-2>=0: 
                        if text_part[target_index-2] in entry_temp["content"]: equal+=1
                    if len(text_part)>target_index+1: 
                        if text_part[target_index+1] in entry_temp["content"]: equal+=1
                    if len(text_part)>target_index+2: 
                        if text_part[target_index+2] in entry_temp["content"]: equal+=1
                    if equal==4:
                        duplicate = True
                        break
                if len(entry["headline"]) > 30: # if title has more than 30 characters
                    if entry["headline"] == entry_temp["headline"]: # check if the titles are the same
                        duplicate = True
                        break
                        
            if duplicate==False: temp.append(entry)
            else: duplicate = False
        else: temp.append(entry)

    return temp

## Group and print results
def results(data):

    publico = ["publico.pt", "www.publico.pt", "jornal.publico.pt", "dossiers.publico.pt", "desporto.publico.pt", "www.publico.clix.pt", "digital.publico.pt", "blogues.publico.pt", "economia.publico.pt", "m.publico.pt", "ultimahora.publico.pt"]
    observador = ["observador.pt"]
    dn = ["www.dn.pt", "dn.sapo.pt", "www.dn.sapo.pt"]
    expresso = ["expresso.pt", "aeiou.expresso.pt", "expresso.sapo.pt"]
    cm = ["www.correiomanha.pt", "www.correiodamanha.pt", "www.cmjornal.xl.pt", "www.cmjornal.pt"]
    jn = ["www.jn.pt", "jn.pt", "jn.sapo.pt"]
    abola = ["abola.pt", "www.abola.pt", "abola.pt:80"]
    visao = ["aeiou.visao.pt", "visao.sapo.pt"]
    sabado = ["www.sabado.pt", "www.sabado.xl.pt", "www.sabado.xl.pt:80", "sabado.pt"]

    publico_count = 0
    observador_count = 0
    dn_count = 0
    expresso_count = 0
    cm_count = 0
    jn_count = 0
    abola_count = 0
    visao_count = 0
    sabado_count = 0

    for entry in data:
        if entry["journal"] in publico: publico_count += 1
        elif entry["journal"] in observador: observador_count += 1
        elif entry["journal"] in dn: dn_count += 1
        elif entry["journal"] in expresso: expresso_count += 1
        elif entry["journal"] in cm: cm_count += 1
        elif entry["journal"] in jn: jn_count += 1
        elif entry["journal"] in abola: abola_count+=1
        elif entry["journal"] in visao: visao_count += 1
        elif entry["journal"] in sabado: sabado_count += 1
    
    print("Extracted " + str(len(data)) + " news.\n")
    print("Público -> " + str(publico_count))
    print("DN -> " + str(dn_count))
    print("Observador -> " + str(observador_count))
    print("Expresso -> " + str(expresso_count))
    print("CM -> " + str(cm_count))
    print("JN -> " + str(jn_count))
    print("A Bola -> " + str(abola_count))
    print("Visão -> " + str(visao_count))
    print("Sábado -> " + str(sabado_count))



# Main
collect()


    