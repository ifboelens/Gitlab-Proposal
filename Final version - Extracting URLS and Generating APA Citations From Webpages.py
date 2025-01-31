#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 11:27:23 2024

@author: isisboelens
"""

import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re

# title of project, my name, and student number:
print("Project Name: Extracting URLS and Generating APA Citations From Webpages")
print('Name: Isis Boelens')
print('Student Number: 6080073')

def generate_apa_citation(driver, url):
    driver.get(url)
    try:
        # Wait for the page to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "title")))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Extract title
        title = soup.title.string.strip() if soup.title else "No title found"
        
        # Extract website name from URL
        parsed_url = urlparse(url)
        website_name = parsed_url.netloc.replace('www.', '')

        # Default author and date values
        author = "No author found"
        date = "n.d."  # Default to "no date"

        # Improved author extraction logic
        author_classes = ['author', 'byline', 'author-name', 'entry-author']
        for class_name in author_classes:
            author_element = soup.find(class_=class_name)
            if author_element:
                # Remove any links and attempt to get plain text
                for a_tag in author_element.find_all('a'):
                    a_tag.decompose()  # Remove <a> tags within the author element
                author_text = author_element.get_text(strip=True).replace("by", "").strip()
                
                if author_text:
                    author = author_text
                    break

        # Fallback to meta tag check for author
        if author == "No author found":
            author_meta = soup.find("meta", {"name": "author"}) or soup.find("meta", {"property": "article:author"})
            if author_meta and author_meta.get("content"):
                author = author_meta["content"].strip()

        # Extract publication date
        date_element = soup.find('time')
        if date_element:
            date = date_element.get_text(strip=True)
        else:
            # Check for other common formats for publication date
            date_element = soup.find(string=lambda text: "Published:" in text if text else False)
            if date_element:
                date_text = date_element.split("Published:")[-1].strip()
                date = date_text if date_text else "n.d."

        # Format APA citation
        citation = f"{author}. ({date}). {title}. {url}"
        
    except Exception as e:
        print(f"Error processing {url}: {e}")
        author, date, website_name, title, citation = None, None, None, None, None
    return author, date, website_name, title, citation

# Extract URLs and citations from an article
def extract_urls_and_citations(soup):
    # Extract all links (URLs) from the article
    urls = [a_tag['href'] for a_tag in soup.find_all('a', href=True)]
    
    # Regex for APA-style citations: (Author, Year)
    citation_pattern = r'\([A-Za-z]+, \d{4}\)'
    text = soup.get_text()
    citations = re.findall(citation_pattern, text)
    
    return urls, citations

# Function to save extracted data into a CSV file
def save_to_csv(data, file_path):
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        for source_name, entries in data.items():
            # Write the source name as a header
            writer.writerow([f"--- {source_name} ---"])

            # Write the table headers
            writer.writerow(["Number", "Type", "URL/Citation"])

            # Write each entry (URL or Citation) for the current source
            for idx, (entry_type, entry_content) in enumerate(entries, 1):
                writer.writerow([idx, entry_type, entry_content])

            # Add an empty row for separation between different sources
            writer.writerow(["" for _ in range(3)])  # Empty row for separation

# Function to display extracted metadata and save data
def display_metadata_and_save(url, author, date, website_name, title, apa_citation, urls, citations, data):
    print(f"\nProcessing URL: {url}")
    print("\n--- Extracted Information ---")
    print(f"Author: {author}")
    print(f"Date: {date}")
    print(f"Website Name: {website_name}")
    print(f"Title: {title}")
    print(f"APA Citation: {apa_citation}")
    
    # Collect URLs and citations for the source
    entries = []
    if urls:
        for url in urls:
            entries.append(("URL", url))
    if citations:
        for citation in citations:
            entries.append(("Citation", citation))
    
    # Add to the data dictionary for saving later
    data[website_name] = entries

# Main function to process multiple URLs
def process_urls(urls, output_file):
    # Initialize WebDriver
    driver = webdriver.Chrome()  # Ensure 'chromedriver' is in your PATH
    data = {}

    try:
        for url in urls:
            # Generate APA citation and metadata
            author, date, website_name, title, apa_citation = generate_apa_citation(driver, url)

            if author is None or date is None:
                print(f"Skipping {url}, due to extraction errors.")
                continue

            # Extract URLs and citations from the article content
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            extracted_urls, extracted_citations = extract_urls_and_citations(soup)

            # Display metadata and save data
            display_metadata_and_save(url, author, date, website_name, title, apa_citation, extracted_urls, extracted_citations, data)
            
    finally:
        driver.quit()  # Close the WebDriver instance

    # Save extracted data to CSV file
    save_to_csv(data, output_file)
    print(f"Data has been saved to {output_file}")

# List of URLs to be processed
urls = [
    "https://www.sciencefocus.com/nature/largest-animal-in-the-world",
    "https://time.com/6958510/are-pickles-good-for-you/",
    "https://www.nature.com/articles/s41392-020-00243-2"
]

# Specify output file path (for Mac, you can specify any location, e.g., Desktop)
output_file = '/Users/isisboelens/Desktop/extracted_data.csv'

# Process URLs and save the results to CSV
process_urls(urls, output_file)


print("\n")

'''
Comments on changes:
1. I wasn't able to resolve the problem with the linked up author name Toby Saunders.

2. I got rid of the table because I didn't see the use of it. This code is useful
when writing a paper so you can cite faster and also get all the URLS from the website.
This made the code shorter, but the output much clearer

3. When running this code on google scholar articles, it has troubles extracting authors.

This likely happens because I added a function on my laptop that through the TU delft I have access to more studies.
Everytime I open an article I need to log in with my username and password, this confuses the code.

Luckily this code isn't needed for scholar articles given that a lot of times the articles
are provided with a citation of the article itself.  '


4. I put all extrated links in a document on my laptop because it was taking in a lot of space in the 
output making the output messy and difficult to read wwhich goes against the purpose of this project.  


Final thoughts:
This final version of my project defenilty has the cleanest and most usefull output. 
The the addition of the use of selenium in version 2 really upgraded this code significanly 
and made the extraction much easier and convinient. Adding the option to define the urls 
as a list made this code much more applicable for its purpose which is research and writing papers. 

Initially in my proposal I had the idea to also add to extract the numerical data in each url. 
This was removed from the end product because I didn't see much value in this addition. 
Also it was hard to define "numerical data". Numercical data are tables and graphs but 
also numbers in text which was hard to define and extract. Being able to get an advanced 
code that is able to do this reliably would be a way to advance this code.

'''



