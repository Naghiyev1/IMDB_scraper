from selenium import webdriver
import pandas as pd
import time
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import requests

driver = webdriver.Chrome(executable_path='C:\\Users\\hnagh\\Desktop\\Development\\chromedriver.exe')
driver.get('https://imdb.com')

# maximize window
driver.maximize_window()

# dropdown
dropdown = driver.find_element_by_class_name('ipc-icon--arrow-drop-down')
dropdown.click()
time.sleep(1)

# advanced search from dropdown menu
element = driver.find_element_by_link_text('Advanced Search')
element.click()

# click on advanced title search
adv_title = driver.find_element_by_link_text('Advanced Title Search')
adv_title.click()

# select feature film
feature_film = driver.find_element_by_id('title_type-1')
feature_film.click()

# select tv movie
tv_movie = driver.find_element_by_id('title_type-2')
tv_movie.click()

# min date
min_date = driver.find_element_by_name('release_date-min')
min_date.click()
min_date.send_keys('1999')

# max date
max_date = driver.find_element_by_name('release_date-max')
max_date.click()
max_date.send_keys('2020')

# rating min
rating_min = driver.find_element_by_name('user_rating-min')
rating_min.click()
dropdown_2 = Select(rating_min)
dropdown_2.select_by_visible_text('1.0')

# rating max
rating_max = driver.find_element_by_name('user_rating-max')
rating_max.click()
dropdown_3 = Select(rating_max)
dropdown_3.select_by_visible_text('10')

# oscar nominated
oscar_nominated = driver.find_element_by_id('groups-7')
oscar_nominated.click()

# color
color = driver.find_element_by_id('colors-1')
color.click()

# language
language = driver.find_element_by_name('languages')
dropdown_4 = Select(language)
dropdown_4.select_by_visible_text('English')

# 250results
results_count = driver.find_element_by_id('search-count')
dropdown_5 = Select(results_count)
dropdown_5.select_by_index(2)

# submit
submit = driver.find_element_by_xpath('(//button[@type="submit"])[2]')
submit.click()

# current
current_url = driver.current_url

# get request
response = requests.get(current_url)

# soup object
soup = BeautifulSoup(response.content, 'html.parser')

# result items (starting point)
list_items = soup.find_all('div', {'class':'lister-item'})

# movie title
#list_items[0].find('h3').find('a').get_text()

# year
#list_items[0].find('h3').find('span', {'class':'lister-item-year'}).get_text().replace('(', '').replace(')', '')

# duration
#list_items[0].find('span', {'class':'runtime'}).get_text()

# genre
#list_items[0].find('span', {'class':'genre'}).get_text().strip()

# rating
#list_items[0].find('div', {'class':'ratings-imdb-rating'}).get_text().strip()

# list comprehension
movie_title = [result.find('h3').find('a').get_text()for result in list_items]
year = [result.find('span', {'class':'lister-item-year'}).get_text().replace('(', '').replace(')', '') for result in list_items]
duration = [result.find('span', {'class':'runtime'}).get_text()for result in list_items]
genre = [result.find('span', {'class':'genre'}).get_text().strip()for result in list_items]
rating = [result.find('div', {'class':'ratings-imdb-rating'}).get_text().strip()for result in list_items]

# create dataframe
imdb_df = pd.DataFrame({'Movie Title':movie_title, 'Year':year, 'Diration':duration, 'Genre':genre, 'Rating':rating})

# output on excel
imdb_df.to_excel('imdb_multiple_pages.xlsx', index=False)
