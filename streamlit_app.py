import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError
streamlit.title('My Parents New Healthy Diner')
streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oat Meal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')
streamlit.header('🍌🥭Build Your Own Fruit Smoothie🥝🍇')
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
#display the table on the page
streamlit.dataframe(fruits_to_show)
streamlit.header('Fruityvice Fruit Advice!')
try:
#create the repeatable code block(called function)
 def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
#streamlit.dataframe(fruityvice_normalized)
  return fruityvice_normalized
#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
 fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
 if not fruit_choice:
  streamlit.error("please select a fruit to get info")
 else:
  back_from_function = get_fruityvice_data(fruit_choice)
  streamlit.dataframe(back_from_function)
  #streamlit.write('The user entered ', fruit_choice)

#print(fruityvice_response)
except URLError as e:
  streamlit.error()
#streamlit.stop()
#snowflake-related functions
def get_fruit_load_list():
 with my_cnx.cursor() as my_cur:
  my_cur.execute("use warehouse pc_rivery_wh")
  my_cur.execute("select * from fruit_load_list")
  return my_cur.fetchall()

# Add a button to load the fruit
if streamlit.button('Get Fruit Load List'):
 my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
 my_data_rows = get_fruit_load_list()
 streamlit.dataframe(my_data_rows)
 
#add_my_fruit = streamlit.text_input('What fruit would you like to add?','Jackfruit') 
#streamlit.write('Thanks for adding ', add_my_fruit)
#my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values ('from streamlit')")


#Allow the end user to add a fruit to the list
def insert_row_snowflake(new_fruit):
 with my_cnx.cursor() as my_cur:
  my_cur.execute("use warehouse pc_rivery_wh")
  my_cur.execute("insert into fruit_load_list values ('from streamlit')")
  return "Thanks for adding " + new_fruit

add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a Fruit to the List'):
 my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
 back_from_function = insert_row_snowflake(add_my_fruit)
 streamlit.text(back_from_function)
