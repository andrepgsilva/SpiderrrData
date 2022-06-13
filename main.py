from MicrosoftTranslate import MicrosoftTranslate
from bs4 import BeautifulSoup
import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()

A_SITE = os.environ.get('A_SITE')
TARGET_SITE = os.environ.get('TARGET_SITE')
CREATE_POST_ENDPOINT = os.environ.get('CREATE_POST_ENDPOINT')

page = requests.get(TARGET_SITE)
soup = BeautifulSoup(page.content, "html.parser")

# firstPostLink = soup.find('a', class_="bc-img-link").get('href')

firstPostLink = soup.select_one('.home-latest .sentinel-home-list article a.bc-img-link').get('href')
firstPostLink = TARGET_SITE + firstPostLink
firstPostRequest = requests.get(firstPostLink)

firstPostPage = BeautifulSoup(firstPostRequest.content, "html.parser")
mainContent = firstPostPage.select('section#article-body p, figure')

# Get the title
articleTitle = firstPostPage.select('h1.article-title')[0].string

#Feature image link
featuredImage = firstPostPage.select_one('section#article-body source[media="(min-width: 1024px)"]')
featuredImageLink = featuredImage['data-srcset']

# Remove useless content
isUselessElementFound = False
for element in mainContent:
    if element.find('span', class_='next-single'):
        isUselessElementFound = True
    if (isUselessElementFound):
        element.clear()

# Change some links
mainContentLinks = firstPostPage.select(
    'section#article-body a[href^="' + TARGET_SITE + '"]')
for link in mainContentLinks:
    link['href'] = A_SITE

translatorTool = MicrosoftTranslate()
translationResult = translatorTool.translate([
    {'text': articleTitle},
    {'text': str(mainContent)}
])
translationResult = json.loads(translationResult)

# Create the post
articleTitle = translationResult[0]['translations'][0]['text']
mainContentString = translationResult[1]['translations'][0]['text']

payload = {
    'featured_image': featuredImageLink,
    'title': articleTitle,
    'content': mainContentString,
}

requestResult = requests.post(CREATE_POST_ENDPOINT, json = payload)
print(requestResult.text)