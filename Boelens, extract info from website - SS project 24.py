#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  6 13:45:19 2024

@author: isisboelens
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import matplotlib.pyplot as plt
import re
import pandas as pd

def generate_apa_citation(url):
    # Fetch the webpage
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Error fetching the URL: {response.status_code}")
        return None, None, None, None  # Return None values if error occurs
    
    # Parse the page content
    soup = BeautifulSoup(response.text, 'html.parser')

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
    return author, date, website_name, title, citation  # Return citation as well

# URL to be cited
url = "https://www.sciencefocus.com/nature/largest-animal-in-the-world"
author, date, website_name, title, apa_citation = generate_apa_citation(url)  # Get citation components

# Print the formatted APA citation
apa_title = "  Apa Citation:\n"
print(apa_title)
print(apa_citation)

indent = "\n  Extracted URLs:\n"
print(indent)

# Check if citation extraction was successful
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

    # Replace placeholders with extracted data
    information = [
        author, 
        date, 
        website_name, 
        title
    ]

    # Combine the labels and information into a table format
    data = list(zip(labels, information))

    # Create a figure and axis
    fig, ax = plt.subplots()

    # Hide the axis
    ax.axis('tight')
    ax.axis('off')

    # Create the table
    table = ax.table(cellText=data, loc='center', cellLoc='center', colWidths=[0.5, 1.2])
    
    # Auto-adjust font size and scale the layout
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1, 2)

    # Show the table
    plt.show()


#extracting URLS and Citations from the website

def extract_urls(text):
    url_pattern = r'https?://[^\s<>"]+|www\.[^\s<>"]+'
    urls = re.findall(url_pattern, text)
    return urls

# Function to extract citations (APA/MLA/Chicago style)
def extract_citations(text):
    # Regex for APA-style citations: (Author, Year)
    citation_pattern = r'\([A-Za-z]+, \d{4}\)'
    citations = re.findall(citation_pattern, text)
    return citations

# Function to extract all links (sources) from a webpage
def extract_links_from_html(soup):
    links = []
    for a_tag in soup.find_all('a', href=True):
        links.append(a_tag['href'])
    return links

# Fetch webpage content
response = requests.get(url)
html_content = response.text

# Parse HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Extract text from the webpage
page_text = soup.get_text()

# Extract URLs from the raw text (if available) and HTML links
extracted_urls = extract_urls(page_text) + extract_links_from_html(soup)

# Extract citations from the webpage
extracted_citations = extract_citations(page_text)

# Prepare a DataFrame to organize the data into a table
data = {
    "Type": ["URL"] * len(extracted_urls) + ["Citation"] * len(extracted_citations),
    "Source": extracted_urls + extracted_citations
}

# Create a pandas DataFrame
df = pd.DataFrame(data)

# Display the table
print(df)


'''
Things to improve in this code:    

1. This code is specific for a type of class of the website. For this url example, 
the class=byline. For every website this can differ. How do I fix that? Is it even possible?

2. When trying it on google scholar articles, this code keeps getting the following error.
Error fetching the URL: 403. 

This has likely to do with the fact that it is a robot.txt file. 
I don't know how to extract information from a robot.txt. file as it keeps restraining 
me from extracting information. Is it even possible? or do you need some type of license 
for that?


3. This code does not include extracting any type of numerical data which I did put in
my proposal.

4. It uses very simple libraries. I tried installing selenium but was unsuccesful
'''

