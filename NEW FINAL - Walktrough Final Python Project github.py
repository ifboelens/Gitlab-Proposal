#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 14:07:21 2025

@author: isisboelens
"""

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


















