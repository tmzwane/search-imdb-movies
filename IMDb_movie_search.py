import re
import sys
from urllib.request import urlopen
try:
    from bs4 import BeautifulSoup
except ImportError:
    from BeautifulSoup import BeautifulSoup
from datetime import datetime

#Capture start time
startTime = datetime.now()

#Ask user for a movie name
movie_title = input("Enter the name of the movie you'd like to view: \n")

#clean up spaces from user's input for the url
movie_title = re.sub(r"\s+", '+', movie_title)

# Will be used to search the movie https://www.imdb.com/find?q=avengers&s=tt&ref_=fn_al_tt_mr
URL = "https://www.imdb.com/find?q=" + movie_title + "&s=tt&ref_=fn_al_tt_mr"

# Will be used to get release dates per title
imdb_home = "https://www.imdb.com"

#Collins was  here
html_text = urlopen(URL)
soup = BeautifulSoup(html_text, "lxml")

#init the array and counts
titleslist = []
titlesURL = []
titles_release_date = []

# This count is to ensure we don't repeat the release date
print_list = 0
mrd_loop = 0

# Get search results in the table from IMDb
title_released = soup.find('table', class_="findList")


print("\n") 
"""
Loop through the results appending the title name to the titlelist list 
and clean up the tags surrouding the name
"""
try:
    for titles in title_released.findAll('td', class_="result_text"):
        movie = titles.findAll('a', href=True)
        for i in range(len(movie)):

            titleslist.append(movie[i].find(text=True))
            titlesURL.append(movie[i]['href'])

            #open each title URL from the result to get the release date
            movie_html = urlopen(imdb_home + titlesURL[mrd_loop])
            soup2 = BeautifulSoup(movie_html, "lxml")

            movie_release_date = soup2.find('div', class_="subtext")

            for mrd in movie_release_date.findAll('a'):
                release_date = mrd.find(text=True)
            
            #append the release date to the title's release date list
            titles_release_date.append(release_date)

            mrd_loop += 1

        if len(titleslist) > 0:
        #    if movie_title in titleslist[print_list]:
                print (titleslist[print_list] + ": " + titles_release_date[print_list])
                print_list += 1

        if print_list >= 10:

            comp_time = datetime.now() - startTime
            sys.exit("...List Completed after "+ comp_time)

    if print_list < 1:
        print (movie_title + " is not in the list")

except Exception:
    sys.exit(movie_title + " is not in the list")