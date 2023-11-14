# Use BeautifulSoup, requests and pandas libraries for web scraping the required information
# Analyze the HTML code of a webpage to find the relevant information
# Store the extracted data as a CSV file and SQL Database



# pandas library for data storage and manipulation
# BeautifulSoup library for interpreting the HTML document
# requests library to communicate with the web page
# sqlite3 for creating the database instance

# pip install pandas
# pip install bs4

import requests
import sqlite3
import pandas as pd
from bs4 import BeautifulSoup

url = 'https://web.archive.org/web/20230902185655/https://en.everybodywiki.com/100_Most_Highly-Ranked_Films'
db_name = 'Movies.db'
table_name = 'Top_50'
csv_path = r'C:\Users\esraa\Desktop\Python_Projects\Movies_WebScraping\top_50_films.csv'
df = pd.DataFrame(columns=["Average Rank","Film","Year"])
count = 0

# Loading the webpage for Webscraping
html_page = requests.get(url).text
data = BeautifulSoup(html_page, 'html.parser') #parse the text in the HTML format using BeautifulSoup to enable extraction of relevant information

# Scraping of required information
tables = data.find_all('tbody')
rows = tables[0].find_all('tr')

# iterate over the rows to find the required data
for row in rows:
    if count < 50 :
        col = row.find_all('td')
        if len(col)!=0:
            data_dict = {"Average Rank": int(col[0].contents[0]),
                         "Film": str(col[1].contents[0]),
                         "Year": int(col[2].contents[0])}
            df1 = pd.DataFrame(data_dict, index=[0])
            df = pd.concat([df,df1], ignore_index=True)
            count+=1
    else:
        break

# Print the contents of the dataframe
print(df)

# Storing the data in a csv file
df.to_csv(csv_path)

# store the required data in a database
conn = sqlite3.connect(db_name)  # initialize a connection to the database
df.to_sql(table_name, conn, if_exists='replace', index=False)  # save the dataframe as a table
conn.close()   # close the connection