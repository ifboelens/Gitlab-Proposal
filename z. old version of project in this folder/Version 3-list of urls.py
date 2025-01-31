#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  22 10:55:12 2024

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

# Function to generate APA citation and extract metadata
def generate_apa_citation(driver, url):
    driver.get(url)

    try:
        # Wait for the page to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "title")))

        # Get page source and parse with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Extract the title
        title = soup.title.string.strip() if soup.title else "No title found"
        
        # Extract website name from the URL
        parsed_url = urlparse(url)
        website_name = parsed_url.netloc.replace('www.', '')

        # Initialize author and date with default values
        author = "No author found"
        date = "n.d."  # Default to "no date"

        # Common author-related classes and attributes to search for
        author_classes = [
            'author', 'byline', 'author-name', 'posted-by', 'entry-author', 
            'article-author', 'written-by'
        ]

        # Attempt to find the author element based on common class names
        for class_name in author_classes:
            author_element = soup.find(class_=class_name)
            if author_element and author_element.name != 'a':  # Ensure it's not a link
                author = author_element.get_text(strip=True).replace("by", "").strip()
                break
        
        # Fallback: If no author found in typical classes, try searching meta tags
        if author == "No author found":
            author_meta = soup.find("meta", {"name": "author"}) or soup.find("meta", {"property": "article:author"})
            if author_meta and author_meta.get("content"):
                author = author_meta["content"].strip()

        # Find the publication date
        date_element = soup.find('time')
        if date_element:
            date = date_element.get_text(strip=True)
        else:
            # Check for other common date formats
            date_element = soup.find(string=lambda text: "Published:" in text)
            if date_element:
                date_text = date_element.split("Published:")[-1].strip()
                date = date_text if date_text else "n.d."

        # Format the APA citation
        citation = f"{author}. ({date}). {title}. {url}"
        
    except Exception as e:
        print(f"Error processing {url}: {e}")
        author, date, website_name, title, citation = None, None, None, None, None
    return author, date, website_name, title, citation

# Function to extract URLs from text using regex
def extract_urls(text):
    url_pattern = r'https?://[^\s<>"]+|www\.[^\s<>"]+'
    return re.findall(url_pattern, text)

# Function to extract citations in APA format
def extract_citations(text):
    citation_pattern = r'\([A-Za-z]+, \d{4}\)'
    return re.findall(citation_pattern, text)

# Function to extract all links from HTML using BeautifulSoup
def extract_links_from_html(soup):
    return [a_tag['href'] for a_tag in soup.find_all('a', href=True)]

# Function to display a table for each URL's metadata
def display_metadata_table(labels, information):
    data = list(zip(labels, information))
    fig, ax = plt.subplots()
    ax.axis('tight')
    ax.axis('off')
    table = ax.table(cellText=data, loc='center', cellLoc='center', colWidths=[0.5, 1.2])
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1, 2)
    plt.show()

# Main function to process multiple URLs
def process_urls(urls):
    # Initialize WebDriver
    driver = webdriver.Chrome()  # Or use 'webdriver.Firefox()' if preferred

    try:
        for url in urls:
            print(f"\nProcessing URL: {url}")
            
            # Generate APA citation and metadata for each URL
            author, date, website_name, title, apa_citation = generate_apa_citation(driver, url)

            if apa_citation:
                print("\nAPA Citation:\n", apa_citation)

                # Display extracted data in a table
                labels = ["Author's Name", "The Date", "Name of Website", "Website's Title"]
                information = [author, date, website_name, title]
                display_metadata_table(labels, information)

                # Fetch page text and extract URLs and citations
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                page_text = soup.get_text()
                
                # Extract URLs and citations
                extracted_urls = extract_urls(page_text) + extract_links_from_html(soup)
                extracted_citations = extract_citations(page_text)

                # Organize extracted URLs and citations in a DataFrame
                data = {
                    "Type": ["URL"] * len(extracted_urls) + ["Citation"] * len(extracted_citations),
                    "Source": extracted_urls + extracted_citations
                }
                df = pd.DataFrame(data)
                print("\nExtracted URLs and Citations:")
                print(df)
            else:
                print(f"Failed to generate citation for {url}")
                
    finally:
        driver.quit()

# List of URLs to be processed
urls = [
    "https://www.sciencefocus.com/nature/largest-animal-in-the-world",
    "https://time.com/6958510/are-pickles-good-for-you/"]

# Process the list of URLs
process_urls(urls)

'''
Comments on progresss:
1. I added the option to list the urls and this worked! 

Things to improve/add:
1. there is still trouble with extracting Toby Saunders name proberly. 
His bio gets extracted, not his name...

2. The urls that get extracted take in a lot of space. I want to put them 
in a seperate document on my computer.

3. The plots seem useless. I like it better to have the information in the console.

4. Meet packaging criteria
'''

