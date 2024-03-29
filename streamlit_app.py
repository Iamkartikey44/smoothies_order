# Import python packages
import streamlit as st
import requests


# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """**Choose the fruits you want in your custom Smoothie!**
    """
)

name_on_order  = st.text_input("Name on Smoothie :")
st.write(f'The name on your Smoothie will be: {name_on_order}')

cnx = st.connection('snowflake')
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options")

#st.dataframe(data=my_dataframe, use_container_width=True)

list = ['Apples','Blueberries','Cantaloupe','Dragon Fruit','Elderberries',
'Figs','Guava','Honeydew','Jackfruit','Kiwi','Lime',
'Mango','Nectarine','Orange','Papaya','Quince','Raspberries','Strawberries','Tangerine',
'Ugli Fruit,Vanilla Fruit','Watermelon','Ximenia','Yerba Mate','Ziziphus Jujube']
ingredients_list = st.multiselect("Choose up to 5 ingredients",list,max_selections=5)


if ingredients_list:
	ingredients_string = ''
	for fruit_chosen in ingredients_list:
		ingredients_string += fruit_chosen + ' '
		fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_chosen)
             fv_df = st.dataframe(data=fruityvice_response.json(),use_container_width=True)
 
    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+"""')"""

    #st.write(my_insert_stmt)
    time_to_insert = st.button("Submit Order")
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
	
    st.success(f'Your Smoothie is ordered!,{name_on_order}', icon="✅")


 

