import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def get_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = [urljoin(url, a['href']) for a in soup.find_all('a', href=True)]
    
    return links



def clean_links(main_url):
    for url in main_url:
        links = get_links(url)
        return links


def final_list_of_links(links):
    final_links = []

    for link in links:
        if '/property/' in link:
            final_links.append(link)
    return final_links        


def get_final_list_of_links(url):
    links = clean_links(url)
    final = final_list_of_links(links)
    remove_dup = list( dict.fromkeys(final) )
    final_list_url= list( dict.fromkeys(remove_dup) )
    return final_list_url
    


f = get_final_list_of_links(g)
print(f)
