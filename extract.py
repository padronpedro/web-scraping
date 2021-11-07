from requests_html import HTMLSession
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

f = open("emails.txt", "a")

#page url
url =r"https://www.postresreina.com"

try:
  fileURL = open('URL.txt', 'r')
  URLList = fileURL.readlines()

  for url in URLList:

    domain_name = urlparse(url).netloc

    #regex pattern
    pattern =r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+"

    #initialize the session
    session = HTMLSession()

    filename = domain_name+"_internal_links.txt"

    try:
        fileLinks = open(filename, 'r')
        URLList = fileLinks.readlines()

        f.write("=========================\n")
        f.write("Website: " + url + "\n")
        print("Processing ----> ", url)

        for oneURL in URLList:
            #send the get request
            response = session.get(oneURL)

            #simulate JS running code
            response.html.render()

            #get body element
            body = response.html.find("body")[0]

            #extract emails
            emails = re.findall(pattern, body.text)

            for index,email in enumerate(emails):
                f.write("email " + str(index+1) + ": " + email + "\n")

    except Exception as e:
        print(str(e))

except Exception as e:
  print(str(e))

f.close()

print('Finished')