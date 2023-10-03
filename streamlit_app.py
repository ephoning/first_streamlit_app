import pandas
import requests
import snowflake.connector
import streamlit
from urllib.error import URLError

streamlit.title("diner demo")

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index("Fruit")

# pick list
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# show DF
streamlit.dataframe(fruits_to_show)

streamlit.header("Fruityvice Fruit Advice!")

def get_fruityvice_data(fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

try:
    fruit_choice = streamlit.text_input("Choose fruit")
    if not fruit_choice:
        streamlit.error("Please select a fruit to get information.")
    else:
        fruit_result = get_fruityvice_data(fruit_choice)
        streamlit.dataframe(fruit_result)
except URLError as e:
    streamlit.error()

#my_cur.execute("select current_user(), current_account(), current_region()")
#my_data_row = my_cur.fetchone()
#streamlit.text("Hello from Snowflake:")

my_cnx = snowflake.connector.connect(**streamlit.secrets['snowflake'])

def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("select * from fruit_load_list")
        return my_cur.fetchall()
    
streamlit.header("The fruit load list contains:")
if streamlit.button("Get fruit load list"):
    my_data_rows = get_fruit_load_list()
    streamlit.dataframe(my_data_rows)

def insert_row_snowflake(new_fruit):
    with my_cnx.cursor as my_cur:
        my_cur.execute(f"insert into fruit_load_list values ('{new_fruit}')")

add_my_fruit = streamlit.text_input("What  fruit would you like to add?")
if streamlit.button("Add fruit to the list"):
    insert_row_snowflake(add_my_fruit)
