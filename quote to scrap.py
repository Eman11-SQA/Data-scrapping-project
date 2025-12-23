import requests
from bs4 import BeautifulSoup
import pandas as pd

# Step 1: Website URL
url = "https://quotes.toscrape.com/"

# Step 2: Website se HTML download karna
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Step 3: Saare quotes find karna
quotes_data = soup.find_all("div", class_="quote")

# Empty lists to store data
quotes = []
authors = []
tags_list = []

# Step 4: Har quote se data extract karna
for quote in quotes_data:
    # Quote text
    text = quote.find("span", class_="text").text
    quotes.append(text)
    
    # Author
    author = quote.find("small", class_="author").text
    authors.append(author)
    
    # Tags (multiple ho sakte hain)
    tags = [tag.text for tag in quote.find_all("a", class_="tag")]
    tags_list.append(", ".join(tags))  # comma separated

# Step 5: Data ko DataFrame me convert karna
df = pd.DataFrame({
    "Quote": quotes,
    "Author": authors,
    "Tags": tags_list
})

# Step 6: CSV file me save karna
df.to_excel("quotes_data.xlsx", index=False, sheet_name="Quotes")


print("Scraping Completed! Data saved in  quotes excel")
