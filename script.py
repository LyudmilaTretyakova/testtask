import regex as re
from bs4 import BeautifulSoup
import requests
import requests_futures
import aiohttp
import asyncio
from requests_futures.sessions import FuturesSession
import tree

trees = []

valid_regex = r"^https?\:\/\/([\w\.]+)wikipedia.org\/wiki\/([\w]+\_?)+"
links = dict()
global checkset
checkset = set()
loop = asyncio.get_event_loop()
def check_valid(link):
    if re.split(valid_regex, link):
        respond = requests.get(link)
        if respond.status_code != 200:
            return True
    else:
        return True


def check_valid_int(intvalue):
    if intvalue>=1 and intvalue<=20:
        return True


async def run_link(link):
    try:
        response = await requests.get(link)
        links = []
        soup = BeautifulSoup(response.text, "html.parser")
        links_ = soup.find(id="bodyContent").find_all("a")
        for link in links_:
            if 'href' in link.attrs:
                if link.attrs['href'].startswith('/wiki/')and check_valid("https://en.wikipedia.org" + link['href']):
                    links.append("https://en.wikipedia.org" + link['href'])
                elif link.attrs['href'].startswith('https') and check_valid(link['href']): #DO IT WITH WIKIIIIIIIII
                    links.append(link['href'])
        return links
    except:
        print("An exception occurred")

    finally:
        return links

def appendaslist(links):
    async_list = []
    for i in links:
        async_list.append(loop.create_task(run_link(i)))
    return async_list


async def main(n,link):
    #action_item =requestsf.get(link, hooks={'link': run_link})
    links[link] = run_link(link)
    async_list = []
    async_list = appendaslist(links[link])
    loop.run_until_complete(asyncio.gather(*async_list))

    #async_list.append(action_item)
    for i in range(1,n):
        # async with aiohttp.ClientSession() as session:
        tasks = []
        for c in list(links.keys()):
            for j in list(links[c]):
                if j not in checkset:
                    appendlink =run_link(j)
                    async_list.append(loop.create_task(run_link(j)))
                    loop.run_until_complete(asyncio.gather(*async_list))
                    links[j] =  appendlink
                    checkset.update(appendlink)
                print(links)

    print(links)

async def run_linkas(session,link):
    async with session.get(link) as resp:
        response = await resp.text()
        links = []
        soup = BeautifulSoup(response, "html.parser")
        links_ = soup.find(id="bodyContent").find_all("a")
        for link in links_:
            if 'href' in link.attrs:
                if link.attrs['href'].startswith('/wiki/'): #and check_valid("https://en.wikipedia.org" + link['href']):
                    links.append("https://en.wikipedia.org" + link['href'])
                elif link.attrs['href'].startswith('https'): #and check_valid(link['href']): #DO IT WITH WIKIIIIIIIII
                    links.append(link['href'])
        return link,links


async def mains(url, n):
    checksett = set()
    async with aiohttp.ClientSession() as session:
        pokemon_url = [url]
        checksett.add(url)
        for i in range(0,n):
            tasks=[]
            for j in pokemon_url:
                if j not in checkset:
                    tasks.append(asyncio.ensure_future(run_linkas(session, j)))

            original_pokemon = await asyncio.gather(*tasks)
            print(original_pokemon)
            checkset |= checksett
            listtree = []
            mytree = tree.Tree(original_pokemon[0][0])
            for pokemon in original_pokemon[0]:
                mytreech = tree.Tree(original_pokemon[0][1])
                mytreech.left(original_pokemon[0][0])
                listtree.append(mytreech)
                pokemon_url.append(pokemon[1])
            mytree.right(listtree)

            checksett |= set(original_pokemon[0])


if __name__ == "__main__":
    input_link = input("Input Wiki link: ")
    if check_valid(input_link):
        print("Url is not valid, please enter valid url")
    else:
        input_int = int(input("Input Integer link: "))
        if check_valid_int(input_int):
            #asyncio.run(main(input_int,input_link))
            asyncio.run(mains(input_link,input_int))
        else:
            print("Int is not valid, please enter valid int from 1 to 20")
