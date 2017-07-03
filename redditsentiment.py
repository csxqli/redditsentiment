import requests
from bs4 import BeautifulSoup
# Imports the Google Cloud client library
from google.cloud import language

# Instantiates a client
language_client = language.Client()

url = 'https://www.reddit.com/r/ethtrader/top/?sort=top&t=all'

r = requests.get(url, headers = {'User-agent': 'youllneverguess'})
#Use fresh username since Reddit rejects the default Python one
r
print(r.status_code)
#a status code of 200 means that everything is okay
soup = BeautifulSoup(r.content, 'html.parser')
siteTable = soup.find("div", { "id" : "siteTable"})
hits = siteTable.find_all("div", { "class" : "thing" } )

i = 0

for hit in hits:
	i = i + 1
	print("-------------------------------------------")
	username = hit.find("a", { "class" : "author"})
	datetime = hit.find("time")['datetime']
	score = hit.find("div", { "class" : "score unvoted"}).text
	for link in hit.find_all('a', href=True):
		if "https://www.reddit.com/r/" in link['href']:
			link = link['href']
			followed = requests.get(link, headers = {'User-agent': 'ethscraper 1.0'})
			followed
			linksoup = BeautifulSoup(followed.content, 'html.parser')
			content = linksoup.find("div", { "class" : "content"})
			paragraphs = content.find_all("p")
			text = ""
			for paragraph in paragraphs:
				text = text + " " + paragraph.text
			document = language_client.document_from_text(text)
			sentiment = document.analyze_sentiment().sentiment
	print(i, "| Username:", username.string, "| Date & Time:", datetime, "| Votes:", score, "|", 'Sentiment: {}, Magnitude: {}'.format(sentiment.score, sentiment.magnitude))
  
  # Copyright 2017 Peter Charles Gleason a.k.a Petro Orynycz-Gleason
