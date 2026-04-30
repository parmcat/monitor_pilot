
import folium
from folium import plugins
import pandas as pd
import json

with open('IRN.geojson', 'r') as f:
    geojson_data = json.load(f)


provinces_damage = {
    'Tehran': 35,  
    'Mazandaran': 20,
    'Golestan': 20,
    'Razavi Khorasan': 25,  # Mashhad 
    'North Khorasan': 15,
    'South Khorasan': 15,
    'Ardabil': 10,
    'West Azerbaijan': 15,
    'East Azerbaijan': 15,
    'Alborz': 15,  # Military infrastructure near Tehran
    'Qazvin': 10,
    'Zanjan': 15,
    'Isfahan': 20,  # Shiraz area heavily damaged
    'Qom': 10,
    'Markazi': 10,
    'Hamadan': 20,
    'Lorestan': 10,
    'Khuzestan': 32,  # so much oil infrastructure 
    'Ilam': 15,
    'Kurdistan': 15,
    'Kohgiluyeh and Boyer-Ahmad': 10,
    'Bushehr': 18,  # naval facilities damaged
    'Hormozgan': 25,  # Bandar Abbas 
    'Kerman': 11,
    'Yazd': 16,
    'Sistan and Baluchestan': 8,
    'Fars': 17,  # Shiraz area
    'Chaharmahal and Bakhtiari': 8,
    'Isfahan': 16,  # Malayer area
    'Gilan': 15,
    'Semnan': 17,
    'Kermanshah':18
}


# Points of interest with damage descriptions for Iran
poi = [
    {
        'name': 'Golestan Palace',
        'lat': 35.7678,
        'lon': 51.4314,
        'province': 'Tehran',
        'damage': 'Moderate - Damaged by airstrikes',
        'type': 'UNESCO Site'
    },
    {
        'name': 'Bisotun Inscription',
        'lat': 34.3903,
        'lon': 47.4295,
        'province': 'Kurdistan',
        'damage': 'Severe - Structural damage',
        'type': 'UNESCO Site'
    },
    {
        'name': 'Khuzestan Oil Refinery',
        'lat': 30.4516,
        'lon': 48.7711,
        'province': 'Khuzestan',
        'damage': 'Critical - Major infrastructure damage',
        'type': 'Industrial Site'
    },
    {
        'name': 'Isfahan Historical Bridge',
        'lat': 32.6572,
        'lon': 51.6681,
        'province': 'Isfahan',
        'damage': 'Being Reconstructed',
        'type': 'Historic Site'

    },


    {
        'name': 'Azadi Indoor Stadium',
        'lat': 35.7689,
        'lon': 51.3389,
        'province': 'Tehran',
        'damage': 'Severe - Structural Damage',
        'type': 'Sports Venue'
    },
    {
        'name': 'Naqsh-e Jahan Square',
        'lat': 32.6565,
        'lon': 51.6681,
        'province': 'Isfahan',
        'damage': 'Moderate - Some Damage',
        'type': 'UNESCO Site'
    },
    
    
    {
        'name': 'Chehel Sotun',
        'lat': 32.6561,
        'lon': 51.6708,
        'province': 'Isfahan',
        'damage': 'Moderate - Some Damage',
        'type': 'UNESCO Site'
    },
    {
        'name': 'Shah Mosque',
        'lat': 32.6567,
        'lon': 51.6680,
        'province': 'Isfahan',
        'damage': 'Minor - Partial Damage',
        'type': 'Religious Site'
    },
    {
        'name': 'Jameh Mosque',
        'lat': 32.6567,
        'lon': 51.6704,
        'province': 'Isfahan',
        'damage': 'Minor - Partial Damage',
        'type': 'Religious Site'
    },
    {
        'name': 'Teymouri Hall',
        'lat': 35.7689,
        'lon': 51.4069,
        'province': 'Tehran',
        'damage': 'Severe - Structural Damage',
        'type': 'Cultural Venue'
    },
    {
        'name': 'Rashk-e Jenan',
        'lat': 35.7500,
        'lon': 51.4200,
        'province': 'Tehran',
        'damage': 'Moderate - Some Damage',
        'type': 'Historic Site'
    },
    {
        'name': 'St Nicholas Orthodox Church of Tehran',
        'lat': 35.7689,
        'lon': 51.4089,
        'province': 'Tehran',
        'damage': 'Minor - Partial Damage',
        'type': 'Religious Site'
    },
    {
        'name': 'Rafi Nia Synagogue',
        'lat': 35.7656,
        'lon': 51.4136,
        'province': 'Tehran',
        'damage': 'Severe - Structural Damage',
        'type': 'Religious Site'
    },
    {
        'name': 'IRIB Media Headquarters',
        'lat': 35.7800,
        'lon': 51.4450,
        'province': 'Tehran',
        'damage': 'Severe - Structural Damage',
        'type': 'Media/Broadcasting'
    },
    {
        'name': 'TehranPars Hospital',
        'lat': 35.74242,
        'lon': 51.53309,
        'province': 'Tehran',
        'damage': 'Moderate - Some Damage',
        'type': 'Medical Facility'
    },
    {
        'name': 'Lamerd Sports Hall',
        'lat': 27.3456,
        'lon': 54.3536,
        'province': 'Hormozgan',
        'damage': 'Moderate - Some Damage',
        'type': 'Sports Venue'
    },
    {
        'name': 'Tehran Bazaar',
        'lat': 35.4003,
        'lon': 51.2510,
        'province': 'Tehran',
        'damage': 'Moderate - Some Damage',
        'type': 'Commercial Site'
    },
    {
        'name': 'Azadi Stadium',
        'lat': 35.7600,
        'lon': 51.5400,
        'province': 'Tehran',
        'damage': 'Severe - Structural Damage',
        'type': 'Sports Venue'
    },
    {
        'name': 'Esmaeli Stadium',
        'lat': 38.9489,
        'lon': 48.4131,
        'province': 'Ardabil',
        'damage': 'Severe - Structural Damage',
        'type': 'Sports Venue'
    },
    {
        'name': 'Shajareh Tayebeh Elementary School',
        'lat': 27.7500,
        'lon': 57.4300,
        'province': 'Hormozgan',
        'damage': 'Severe - Structural Damage',
        'type': 'Educational Facility'
    },


{
        'name': 'Mehrabad Airport',
        'lat': 35.68917,
        'lon': 51.31361,
        'province': 'Tehran',
        'damage': 'Under Reconstruction',
        'type': 'Airport'
    },

{
        'name': 'Imam Khomeini Airport',
        'lat': 35.41611,
        'lon': 51.15222,
        'province': 'Tehran',
        'damage': 'Under Reconstruction',
        'type': 'Airport'
    },

{
        'name': 'Yahya-Abad Bridge',
        'lat': 36.21333,
        'lon': 49.77000,
        'province': 'Qazvin',
        'damage': 'Reconstruction Complete',
        'type': 'Bridge'
    },

{
        'name': 'Qom Railway Bridge',
        'lat': 34.64010,
        'lon': 50.87640,
        'province': 'Qom',
        'damage': 'Reconstruction Complete',
        'type': 'Bridge'
    },

{
        'name': 'Zanjan-Mianeh Railway Bridge',
        'lat': 36.78000,
        'lon': 48.10000,
        'province': 'Zanjan',
        'damage': 'Reconstruction Complete',
        'type': 'Bridge'
    },

{
        'name': 'Karaj Railway Bridge',
        'lat': 35.82868,
        'lon': 51.03674,
        'province': 'Alborz',
        'damage': 'Reconstruction Complete',
        'type': 'Bridge'
    },

{
        'name': 'Tehran-Mashhad Qaleh Railway Bridge',
        'lat': 35.51222,
        'lon': 51.51611,
        'province': 'Tehran',
        'damage': 'Reconstruction Complete',
        'type': 'Bridge'
    },

{
        'name': 'Charbagh Alborz Railway Bridge',
        'lat': 35.80000,
        'lon': 50.95000,
        'province': 'Alborz',
        'damage': 'Reconstruction Complete',
        'type': 'Bridge'
    }

    
]

def create_iran_damage_map():
    # Create the base map centered on Iran
    iran_center = [32.4279, 53.6880]
    m = folium.Map(
        location=iran_center,
        zoom_start=6,
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
            key_on='feature.properties.shapeName',

            # Adjust based on GeoJSON structure
            fill_color='Reds',
            fill_opacity=0.8,
            line_opacity=0.3,
            legend_name='Damage Percentage (%)',).add_to(m)

        
    except Exception as e:
        print(f"Note: Could not load GeoJSON. Error: {e}")
        print("See instructions below to add the GeoJSON file.")

    # Add markers for points of interest
    for point in poi:
        # Create popup with detailed information
        popup_html = f"""
        <div style="font-family: Arial; width: 200px;">
            <h4 style="margin: 5px 0;">{point['name']}</h4>
            <p style="margin: 5px 0;"><b>Province:</b> {point['province']}</p>
            <p style="margin: 5px 0;"><b>Type:</b> {point['type']}</p>
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
    m.save('iran_damage_map.html')
    print("Map saved as 'iran_damage_map.html'")
    return(m)
