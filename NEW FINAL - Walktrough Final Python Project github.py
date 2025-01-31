#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 14:07:21 2025

@author: isisboelens
"""

# title of project, my name, and student number:
print("Project Name: Extracting URLS and Generating APA Citations From Webpages")
print('Name: Isis Boelens')
print('Student Number: 6080073')

"""
Since I unsuccesfully used git in my previous submission I will re write my 
project such that the changes are saved in github.

Previously I used multiple files to track my changes. Each version was a 
bettered version of the previous one. Usually I sat down to code for a couple 
of hours and each time I did that I created a new version to make sure 
that if I made the wrong changes I could look back at my initial work. 
Exactly what github would've done for me automatically. 

To get a better hang of git functions I will use this file to track my progress
As my code was good and I am happy with it, I will to re-do what I did
before using the right tracking methods. This way I can show that I understood 
the assigment and can work with github.

In addition, I will add testing, which I did not really do previously.

I will keep my old version and work in the folder "Project Citation" so 
you can see my progress.
"""

import csv
import os
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re

#selenium made code more robust

"""
selenium webdrive: made the code not specific for a type of class or ID, 
but was able to search for those elements themselvse. 
Making the code more adaptable to different webpages! 

Initially requests was used. This allowed to only use one type of class 
(see version1)
"""
from selenium.webdriver.common.by import By

"""
selenium.support.ui: purpose was to use WebDriverWait. To wait for specific 
conditions to be true before proceeding. It prevents errors caused by trying 
to interact with elements that haven't loaded yet
"""
from selenium.support.ui import WebDriverWait

"""
selenium.webdriver.support: provides set of predefined conditions. Makes code 
more efficient by abstracting complex wait conditions into easy useable checks
ensures element you need is ready to use before interacting with it
"""
from selenium.webdriver.support import expected_conditions as EC


#generating apa citation

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

        # author extraction
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
            """
            previously the publication date of the url I used was not able to be found.
            This even though it was written on the webpage right below the author's 
            name! Therefore, I added this, beceause in those cases soup.find("time") 
            can't find the publication date.
            """
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
def save_to_csv(data, file_name):
    # Get the directory where the current script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create the full file path by combining the script directory and the file name
    file_path = os.path.join(script_dir, file_name)
    
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
            writer.writerow(["" for _ in range(3)])  


# Function to display extracted metadata and save data
def display_metadata_and_save(url, author, date, website_name, title, apa_citation, urls, citations, data):
    print(f"\nProcessing URL: {url}")
    print("\n--- Extracted Information ---")
    print(f"Author: {author}")
    print(f"Date: {date}")
    print(f"Website Name: {website_name}")
    print(f"Title: {title}")
    print(f"APA Citation: {apa_citation}")
    





