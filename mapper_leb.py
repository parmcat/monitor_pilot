
import folium
from folium import plugins
import pandas as pd
import json

with open('LBN.json', 'r') as f:
    geojson_data = json.load(f)


provinces_damage = {
    'Beirut': 25,  
    'MountLebanon': 20,
    'North': 15,
    'South': 60,  
    'Bekaa': 35,
    'Nabatiyeh': 50,
    'Akkar':20,
    'Baalbak-Hermel': 40,
}


# Points of interest with damage descriptions for the Lebanon
poi_leb = [
   
    {
        'name': 'Al Sawaneh',
        'lat': 33.2336,
        'lon': 35.4390,
        'province': 'Nabatieh',
        'damage': 'Severe',
        'notes': 'Latest strike on April 27th'
    },
    {
        'name': 'Nabatiyeh',
        'lat': 33.3850,
        'lon': 35.2281,
        'province': 'Nabatieh',
        'damage': 'Severe',
        'notes': 'Latest strike on April 28th'
    },

    {
        'name': 'Aroun',
        'lat': 33.3315,
        'lon': 35.5259,
        'province': 'Nabatieh',
        'damage': 'Severe',
        'notes': 'Latest strike on April 26th'
    },


    {
        'name': 'Bint Jbeil',
        'lat': 33.1208,
        'lon': 35.4336,
        'province': 'Nabatieh',
        'damage': 'Severe',
        'notes': 'Latest strike on April 28th'
    },


    {
        'name': 'Shamaa',
        'lat': 33.1456,
        'lon': 35.2081,
        'province': 'South',
        'damage': 'Severe',
        'notes': 'Latest strike on April 20th'
    },
    
    {
        'name': 'Jibshit',
        'lat': 33.3671,
        'lon': 35.4375,
        'province': 'Nabatieh',
        'damage': 'Moderate',
        'notes': 'Latest strike on April 29th'
    },


    {
        'name': 'Qaqaiyat al-Jisr',
        'lat': 33.3256,
        'lon': 35.4181,
        'province': 'Nabatieh',
        'damage': 'Severe',
        'notes': 'Latest strike on April 20th'
    },

    {
        'name': 'Taybeh',
        'lat': 33.2764,
        'lon': 35.5206,
        'province': 'Nabatieh',
        'damage': 'Severe',
        'notes': 'Latest strike on April 20th'
    },
    
]


def create_lebanon_damage_map():

    # Create the base map centered on Lebanon
    lebanon_center = [33.8547, 35.8623]
    m = folium.Map(
        location=lebanon_center,
        zoom_start=8,
        tiles="Cartodb Positron"
    )

    
    # Create the dataframe for the chloropleth
    damage_df = pd.DataFrame(list(provinces_damage.items()), columns=['Province', 'Damage_Percentage'])

    # Add choropleth using province names
    try:
        folium.Choropleth(
            geo_data= geojson_data,
            name='Damage Percentage',
            data=damage_df,
            columns=['Province', 'Damage_Percentage'],
            key_on='feature.properties.NAME_1',

            # Adjust based on GeoJSON structure
            fill_color='Reds',
            fill_opacity=0.8,
            line_opacity=0.3,
            legend_name='Damage Percentage (%)',).add_to(m)

        
    except Exception as e:
        print(f"Note: Could not load GeoJSON. Error: {e}")
        print("See instructions below to add the GeoJSON file.")

    # Add markers for points of interest
    for point in poi_leb:
        # Create popup with detailed information
        popup_html = f"""
        <div style="font-family: Arial; width: 200px;">
            <h4 style="margin: 5px 0;">{point['name']}</h4>
            <p style="margin: 5px 0;"><b>Province:</b> {point['province']}</p>
            <p style="margin: 5px 0;"><b>Notes:</b> {point['notes']}</p>
            <p style="margin: 5px 0;"><b>Damage Status:</b></p>
            <p style="margin: 5px 0; color: #d9534f;">{point['damage']}</p>
        </div>
        """
    
        # Determine marker color based on damage severity
        if 'Critical' in point['damage']:
            color = 'red'
            icon = 'exclamation'
        elif 'Severe' in point['damage']:
            color = 'orange'
            icon = 'warning'
        elif 'Moderate' in point['damage']:
            color = 'orange'
            icon = 'info-sign'
        else:
            color = 'yellow'
            icon = 'info-sign'
    
        folium.Marker(
            location=[point['lat'], point['lon']],
            popup=folium.Popup(popup_html, max_width=250),
            icon=folium.Icon(color=color, icon=icon),
            tooltip=point['name']
        ).add_to(m)

    # Add layer control
    folium.LayerControl().add_to(m)
    # folium.TileLayer('CartoDB positron').set_as_active().add_to(m)

    # Save the map
    m.save('lebanon_damage_map.html')
    print("Map saved as 'lebanon_damage_map.html'")
    return(m)
