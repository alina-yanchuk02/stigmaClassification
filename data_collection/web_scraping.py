"""
Automatic classification of stigmatizing mental illness articles in online news journals - April 2022
Author: Alina Yanchuk - alinayanchuk@ua.pt
"""

## Scraping of HTML pages by url

# -------------- Imports -------------

from utils import try_request

from newspaper import Article

# -------------- Main functions ------

## Web scraping and filtering
def get_data(item):

    terms = ["Esquizofrenia", "esquizofrenia", "Esquizofrénico", "esquizofrénico", "Esquizofrenico", "esquizofrenico", "Esquizofrénica", "esquizofrénica", "Esquizofrenica", "esquizofrenica", "Esquizofrénicas", "esquizofrénicas", "Esquizofrenicas", "esquizofrenicas", "Esquizofrénicos", "esquizofrénicos", "Esquizofrenicos", "esquizofrenicos", "Esquizofrenicamente", "esquizofrenicamente", "Esquizofrenizar", "esquizofrenizar", "psicose", "Psicose", "psicótica", "Psicótica", "psicotica", "Psicotica", "psicóticas", "Psicóticas", "psicoticas", "Psicoticas", "psicótico", "Psicótico", "psicotico", "Psicotico", "psicóticos", "Psicóticos", "psicóticos", "Psicoticos"]
    data = {}

    try:
        page = Article(item["linkToOriginalFile"], language="pt")
        page.download()
    except: print("Error in scraping: can't get the page")

    try:
        page.parse()
        page.nlp()

        title = page.title
        content = page.text
        authors = page.authors
        publish_date = page.publish_date

        if any(term in title for term in terms) or any(term in content for term in terms): # if any term in news headline or content
            data["label"] = ""
            data["headline"] = title
            data["journal"] = item["journal"]
            data["content"] = content
            data["authors"] = authors
            data["publishDate"] = str(publish_date)
            data["archiveDate"] = str(item["tstamp"])
            data["linkToArchive"] = item["linkToArchive"]

            data = clean(data)

            return data   

    except:
        print("Can't scap. | " + item["linkToArchive"] + " | " + str(item["tstamp"]))

    return None


# -------------- Auxiliar functions ------

## Clean unnecessary info and normalize
def clean(data):

    data["content"] = data["content"].replace("\n", " ")
    if "TV Hoje " in data["content"]: data["content"] = data["content"].replace("TV Hoje ", " ")
    if "OPINIÃO " in data["content"]: data["content"] = data["content"].replace("OPINIÃO ", " ")
    if "COMENTÁRIO " in data["content"]: data["content"] = data["content"].replace("COMENTÁRIO ", " ")
    if "JN Editorial " in data["content"]: data["content"] = data["content"].replace("JN Editorial ", " ")
    if "| | | | | | " in data["content"]: data["content"] = data["content"].replace("| | | | | | ", " ") 
    if "Nota Este texto é da inteira responsabilidade do autor e da entidade representada." in data["content"]: data["content"] = data["content"].replace("Nota Este texto é da inteira responsabilidade do autor e da entidade representada.", " ") 
    if "OPINIÃO" in data["content"]: data["content"] = data["content"].replace("OPINIÃO ", " ")
    if "d.r. Tamanho Letra Enviar  Partilhar  Lida Gostou desta notícia? Sim  Não URL COMENTÁRIO MAIS VOTADO" in data["content"]: data["content"] = data["content"].replace("d.r. Tamanho Letra Enviar  Partilhar  Lida Gostou desta notícia? Sim  Não URL COMENTÁRIO MAIS VOTADO", " ")
    if "TV Hoje" in data["content"]: data["content"] = data["content"].replace("TV Hoje", " ")
    if "DN Online: " in data["headline"]: data["headline"] = data["headline"].replace("DN Online: ", " ")
    if "JORNAL PUBLICO: " in data["headline"]: data["headline"] = data["headline"].replace("JORNAL PUBLICO: ", " ")
    if "Suplemento Mil Folhas" in data["headline"]: data["headline"] = " "
    if "TV Hoje" in data["headline"]: data["headline"] = " "
    if "Suplemento Pública" in data["headline"]: data["headline"] = " "
    if "Suplemento Y" in data["headline"]: data["headline"] = " "
    if "Espaço Público" in data["headline"]: data["headline"] = " "
    if "Opinião" in data["headline"]: data["headline"] = " "
    if "Cartaz" in data["headline"]: data["headline"] = " "
    if "Jornal de Noticias" in data["headline"]: data["headline"] = " "
    if "Diário de Notícias" in data["headline"]: data["headline"] = " "
    if "Diario de Notícias" in data["headline"]: data["headline"] = " "
    if "JN Editorial" in data["headline"]: data["headline"] = " "
    if "dossiers publico.pt" in data["headline"]: data["headline"] = " "
    if "dossiers.publico.pt" in data["headline"]: data["headline"] = " "
    if "– Observador" in data["headline"]: data["headline"] = " "
    if "Imprimir Artigo" in data["headline"]: data["headline"] = " "
    if "EXPRESSO — Notícias, opinião, blogues, fóruns, podcasts. O semanário de referência português." in data["headline"]: data["headline"] = " "
    if "Inês Pedrosa" in data["headline"]: data["headline"] = " "
    if "Luis Pedro Nunes" in data["headline"]: data["headline"] = " "
    if "J.L.Saldanha" in data["headline"]: data["headline"] = " "
    if "Expresso - Expresso.pt" in data["headline"]: data["headline"] = " "
    if data["headline"] == "DN": data["headline"] = " "
    if data["headline"] == "Última Hora": data["headline"] = " "
    if data["headline"] == "Publico.pt": data["headline"] = " "
    if data["headline"] == "PUBLICO.PT": data["headline"] = " "
    if data["headline"] == "Untitled Document": data["headline"] = " "
    if data["headline"] == "PUBLICO.PT": data["headline"] = " "
    if data["headline"] == "PUBLICO.PT": data["headline"] = " "
    if "DN" in data["headline"]: data["headline"] = " "
    if "Henrique Monteiro" in data["headline"]: data["headline"] = " "
    if "Correio da Manhã" in data["headline"]: data["headline"] = " "
    if "Expresso - Expresso.pt" in data["headline"]: data["headline"] = " "
    if "EXPRESSO On.Line:" in data["headline"]: data["headline"] = data["headline"].replace("EXPRESSO On.Line:", "")
    if "EXPRESSO: " in data["headline"]: data["headline"] = data["headline"].replace("EXPRESSO: ", "")
    if " 00:00:00" in data["publishDate"]: data["publishDate"] = data["publishDate"].replace(" 00:00:00", "")

    if len(data["archiveDate"]) > 7:
        year_archive = data["archiveDate"][0:4]
        month_archive = data["archiveDate"][4:6]
        day_archive = data["archiveDate"][6:8]
        data["archiveDate"] = year_archive + '-' + month_archive + '-' + day_archive


    title = data["headline"].lower()
    content = data["content"].lower()
    authors = data["authors"]
    
    if len(title) > 1:
        if title in content: # remove title from content
            data["content"] = data["content"].replace(title, "")
    
    if len(authors) > 0:
        for author in authors: # remove authors from content
            original_author = author
            author = author.lower()
            if ("por " + author) in content:
                data["content"] = data["content"].replace(("Por " + author.upper()), "")
                data["content"] = data["content"].replace(("POR " + author.upper()), "")
                data["content"] = data["content"].replace(("Por " + original_author), "")
                data["content"] = data["content"].replace(("POR " + original_author), "")
                data["content"] = data["content"].replace(("por " + author.upper()), "")
                data["content"] = data["content"].replace(("por " + original_author), "")
            if author in content:
                data["content"] = data["content"].replace(author.upper(), "")
                data["content"] = data["content"].replace(author, "")
                data["content"] = data["content"].replace(original_author, "")
    
    if data["journal"] in content: # remove journal URL from content
        data["content"] = data["content"].replace(data["journal"], "")

    return data
        
    



        
