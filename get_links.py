from requests_html import HTMLSession
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import colorama
from requests_html import HTMLSession
import re


# init the colorama module
colorama.init()

GREEN = colorama.Fore.GREEN
GRAY = colorama.Fore.LIGHTBLACK_EX
RESET = colorama.Fore.RESET
YELLOW = colorama.Fore.YELLOW

# initialize the set of links (unique links)
internal_urls = set()
external_urls = set()

total_urls_visited = 0


def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def get_all_website_links(url):
    """
    Returns all URLs that is found on `url` in which it belongs to the same website
    """
    # all URLs of `url`
    urls = set()
    # domain name of the URL without the protocol
    domain_name = urlparse(url).netloc
    # initialize an HTTP session
    session = HTMLSession()
    # make HTTP request & retrieve response
    response = session.get(url)
    # execute Javascript
    try:
        response.html.render()
    except:
        pass
    soup = BeautifulSoup(response.html.html, "html.parser")
    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            # href empty tag
            continue
        # join the URL if it's relative (not absolute link)
        href = urljoin(url, href)
        parsed_href = urlparse(href)
        # remove URL GET parameters, URL fragments, etc.
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        if not is_valid(href):
            # not a valid URL
            continue
        if href in internal_urls:
            # already in the set
            continue
        if any(re.findall(r'.gif|.jpg|.pdf|.jpeg|.txt|.mov|.png', href, re.IGNORECASE)):
            # not a valid URL
            continue
        tempDomain = domain_name

        if "www" in domain_name:
            tempDomain = domain_name[4:]
        if tempDomain not in href or "http" not in href:
            # external link
            if href not in external_urls:
                print(f"{GRAY}[!] External link: {href}{RESET}")
            continue
        print(f"{GREEN}[*] Internal link: {href}{RESET}")
        urls.add(href)
        internal_urls.add(href)
    return urls


def crawl(url, max_urls=30):
    """
    Crawls a web page and extracts all links.
    You'll find all links in `external_urls` and `internal_urls` global set variables.
    params:
        max_urls (int): number of max urls to crawl, default is 30.
    """
    global total_urls_visited
    total_urls_visited += 1
    print(f"{YELLOW}[*] Crawling: {url}{RESET}")
    links = get_all_website_links(url)
    for link in links:
        if total_urls_visited > max_urls:
            break
        crawl(link, max_urls=max_urls)



if __name__ == "__main__":
    try:
        fileURL = open('URL.txt', 'r')
        URLList = fileURL.readlines()

        for url in URLList:
            max_urls = 30

            crawl(url, max_urls=max_urls)

            print("[+] Total Internal links:", len(internal_urls))
            print("[+] Total URLs:", len(internal_urls))
            print("[+] Total crawled URLs:", max_urls)

            domain_name = urlparse(url).netloc

            # save the internal links to a file
            with open(f"{domain_name}_internal_links.txt", "w") as f:
                for internal_link in internal_urls:
                    print(internal_link.strip(), file=f)

            internal_urls = set()

    except Exception as e:
        print(str(e))
