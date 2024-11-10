#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  13 15:31:33 2024

@author: isisboelens
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import matplotlib.pyplot as plt
import re
import pandas as pd

# title of project, my name, and student number:
print("Project Name: Extracting URLS and Generating APA Citations From Webpages")
print('Name: Isis Boelens')
print('Student Number: 6080073')

def generate_apa_citation(url):
    # Initialize Selenium WebDriver
    driver = webdriver.Chrome()  # Or use 'webdriver.Firefox()' if you have Firefox installed
    driver.get(url)

    try:
        # Wait until the title element is present (adjust as needed)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "title")))

        # Get the page source and parse it with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Extract the title of the page
        title = soup.title.string.strip() if soup.title else "No title found"
        
        # Extract the website name from the URL
        parsed_url = urlparse(url)
        website_name = parsed_url.netloc.replace('www.', '')  # Remove 'www.' if present

        # Initialize author and date with default values
        author = "No author found"
        date = "n.d."  # Default to "no date"

        # Try to find the author
        author_element = soup.find('p', class_='byline')
        if author_element:
            author = author_element.get_text(strip=True).replace("by", "").strip()  # Clean up the author text

        # Try to find the publication date
        date_element = soup.find('time')
        if date_element:
            date = date_element.get_text(strip=True)  # Get text if available
        else:
            # Check for other common formats for publication date
            date_element = soup.find(string=lambda text: "Published:" in text)
            if date_element:
                date_text = date_element.split("Published:")[-1].strip()
                date = date_text if date_text else "n.d."

        # Format the citation in APA style
        citation = f"{author}. ({date}). {title}. {url}"  # Include URL in citation
        
    finally:
        # Close the driver
        driver.quit()
    
    return author, date, website_name, title, citation  # Return citation as well

# URL to be cited
#url = "https://www.sciencefocus.com/nature/largest-animal-in-the-world"

url = "https://time.com/6958510/are-pickles-good-for-you/"
author, date, website_name, title, apa_citation = generate_apa_citation(url)  # Get citation components

# Print the formatted APA citation
print("\nAPA Citation:")
print(apa_citation)

# Display extracted data in a table
if not author:
    print("Error extracting data from the URL")
else:
    # Data for the table
    labels = [
        "Author's Name", 
        "The Date", 
        "Name of Website", 
        "Website's Title"
    ]
    information = [author, date, website_name, title]
    data = list(zip(labels, information))

    fig, ax = plt.subplots()
    ax.axis('tight')
    ax.axis('off')
    table = ax.table(cellText=data, loc='center', cellLoc='center', colWidths=[0.5, 1.2])
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1, 2)
    plt.show()

# Extract URLs and Citations
def extract_urls(text):
    url_pattern = r'https?://[^\s<>"]+|www\.[^\s<>"]+'
    urls = re.findall(url_pattern, text)
    return urls

def extract_citations(text):
    citation_pattern = r'\([A-Za-z]+, \d{4}\)'
    citations = re.findall(citation_pattern, text)
    return citations

def extract_links_from_html(soup):
    links = []
    for a_tag in soup.find_all('a', href=True):
        links.append(a_tag['href'])
    return links

# Fetch webpage content using Selenium
driver = webdriver.Chrome()  # Make sure ChromeDriver is installed
driver.get(url)

try:
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    page_text = driver.page_source
    soup = BeautifulSoup(page_text, 'html.parser')
    page_text = soup.get_text()
    
    extracted_urls = extract_urls(page_text) + extract_links_from_html(soup)
    extracted_citations = extract_citations(page_text)

    data = {
        "Type": ["URL"] * len(extracted_urls) + ["Citation"] * len(extracted_citations),
        "Source": extracted_urls + extracted_citations
    }

    df = pd.DataFrame(data)
    print(df)
finally:
    driver.quit()
    
    
'''
Comments on progresss:
1. The use of Selenium resulted in more information being able to get extracted, and automated the browser interaction.

2. I tried other links, the code still worked. This was not the case for the first version of this project. 
In that version the code only worked the specific type of class that I defined in the code. You had
to check the class of the website and change this in the code for the code to be able to function.

3. I added my name, student number, and a name of the project

Things to add/improve:
1. I have troubles with the authors that are linked on the website to another page with their bio. This code 
takes their whole bio and puts it as "Author's Name"

2. I want to add that the code can run on a list of urls. So that when writing a paper this code can be used for creating
the reference page.
'''