#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 17:34:43 2025

@author: isisboelens
"""


import pytest
from unittest.mock import MagicMock
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from new_final_walkthrough_final_python_project import generate_apa_citation


@pytest.fixture
def mock_driver():
    # Mock the Selenium WebDriver
    driver = MagicMock()
    driver.get = MagicMock()  # Mock the get function
    return driver


@pytest.fixture
def mock_soup():
    # Mock BeautifulSoup with a sample HTML content
    html_content = """
    <html>
        <head><title>Sample Title</title></head>
        <body>
            <div class="author">John Doe</div>
            <time datetime="2023-01-01">January 1, 2023</time>
        </body>
    </html>
    """
    return BeautifulSoup(html_content, 'html.parser')


def test_generate_apa_citation(mock_driver, mock_soup):
    # Mock WebDriver to return specific soup when the page loads
    mock_driver.page_source = str(mock_soup)

    # Create a mock for WebDriverWait to simulate the 'until' condition
    mock_wait = MagicMock()
    mock_wait.until = MagicMock(return_value=True)

    # Use the mock_wait in place of the actual WebDriverWait
    WebDriverWait.return_value = mock_wait

    # Test with a sample URL
    url = "https://example.com/sample-article"
    author, date, website_name, title, citation = generate_apa_citation(mock_driver, url)

    # Check that the title is correctly parsed
    assert title == "Sample Title", f"Expected 'Sample Title', but got {title}"

    # Check that the author is correctly parsed
    assert author == "John Doe", f"Expected 'John Doe', but got {author}"

    # Check that the date is correctly parsed
    assert date == "January 1, 2023", f"Expected 'January 1, 2023', but got {date}"

    # Check that the website name is correctly parsed
    assert website_name == "example.com", f"Expected 'example.com', but got {website_name}"

    # Check that the APA citation is correctly formatted
    expected_citation = "John Doe. (January 1, 2023). Sample Title. https://example.com/sample-article"
    assert citation == expected_citation, f"Expected APA citation: {expected_citation}, but got {citation}"
