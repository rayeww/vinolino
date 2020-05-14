"""
Author: Mario Ruh, mario.ruh@students.fhnw.ch and Raymond Oberholzer, raymond.oberholzer@students.fhnw.ch
"""

import pandas as pd
import streamlit as st
from PIL import Image
import SessionState

session = SessionState.get(run_id=0) # used to reset session with reset button

# import data
data = pd.read_csv('wein_utf8.csv')

# title
st.title('Vinolino')
st.image('Titelbild.jpg', use_column_width=True)
st.sidebar.text('Wählen Sie Ihre Selektionskriterien')

# reset button
if st.sidebar.button("Reset"):
  session.run_id += 1

# list of existing wine typs
typs_list = data['Weintyp'].unique().tolist()
typs_list.insert(0,'Alle')

# list of existing character typs
characters_list = data.Charakter.unique().tolist()
characters_list.insert(0,'Alle')

# list of existing flavor typs
flavor_list = data.Geschmack.unique().tolist()
flavor_list.insert(0,'Alle')

# list of existing land typs
land_list = data.Land.unique().tolist()
land_list.insert(0,'Alle')

# list of prices
price_list = data.Preis.unique().tolist()
price_list.insert(0,'Alle')

# menu
winetyp = st.sidebar.selectbox('Welchen Typ Wein bevorzugen Sie?', typs_list, key=session.run_id)  # select winetyp
characters = st.sidebar.selectbox('Welchen Charakter soll der Wein haben?', characters_list, key=session.run_id)  # select charakter
flavor = st.sidebar.selectbox('Welchen Geschmack soll der Wein haben?', flavor_list, key=session.run_id)  # select flavor
land = st.sidebar.selectbox('Von welchem Land soll der Wein kommen?', land_list, key=session.run_id)  # select land
preis1, preis2 = st.sidebar.slider('Preis',int(data['Preis'].min()),int(data['Preis'].max()), (int(data['Preis'].min()),int(data['Preis'].max())), key=session.run_id) #select price




#if else for "Alle" button (dropdownmenu's)
if winetyp == "Alle":
    winetyp = typs_list
else:
    winetyp = [winetyp]

if characters == "Alle":
    characters = characters_list
else:
    characters = [characters]

if flavor == "Alle":
    flavor = flavor_list
else:
    flavor = [flavor]

if land == "Alle":
    land = land_list
else:
    land = [land]

data = data[data['Weintyp'].isin(winetyp)]
data = data[data['Charakter'].isin(characters)]
data = data[data['Geschmack'].isin(flavor)]
data = data[data['Land'].isin(land)]
data = data[data['Preis'].between(preis1,preis2)]

if len(data) > 0:
    st.table(data)

else:
    st.markdown("## Mit diesem Selektionsmerkmal wurden keine passende Weine gefunden.")

    st.markdown('Wählen Sie bitte andere Kriterien aus.')

# print list of images
# if len(data) <=6:
names = list(data['Name'])
images = []
true_names = []
for name in names:
    try:
        image = Image.open(f'Wein_Bilder/{name}.jpg')
        images.append(image)
        true_names.append(name)
    except:
        st.write(f'Keine Abbildung für {name} verfügbar.')

st.image(images, width=100, caption=true_names)