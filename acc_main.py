# imports

import streamlit as st
import streamlit_themes as st_theme
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import pandas_datareader as pdr
import plotly.io as pio
import requests
import numpy as np
import folium
from folium import plugins
from streamlit_folium import st_folium
from mapper import create_iran_damage_map
from mapper_leb import create_lebanon_damage_map
import json
import feedparser


################################## THEMES AND LOOKS ############################

# apply a preset theme
st_theme.set_preset_theme('Beach')
pio.templates.default = "ggplot2"

# page configuration
st.set_page_config(page_title="Geopolitical Conflict Monitor Pilot", layout="wide")

st.title("Conflict Monitor")

# create tabs
tab_we, tab_irlb, tab_hmz, tab_a = st.tabs(["West Asia", "Damage Maps for Hardest Hit", "Hormuz", "Appendix and AI Disclosures"])


####################################### ACLED DATA IMPORT ############################

# manual data import because the API fucking sucks 
df = pd.read_csv('ME_data_clean_2.csv')
df = df.replace('Palestine', 'Palestine - Gaza')
df = df.replace('Israel', 'Occupied Palestine')
result_dict = {}

for country in df['COUNTRY'].unique():
    country_df = df[df['COUNTRY'] == country]
    
     # group by sub event type and sum fatalities and also calc total fatalities 
    sub_event_fatalities = country_df.groupby('SUB_EVENT_TYPE')['FATALITIES'].sum().to_dict()
    total_fatalities = country_df['FATALITIES'].sum()
    
    # combine per country
    country_data = {**sub_event_fatalities, 'total': total_fatalities}
    result_dict[country] = country_data
    
    # add West Bank manually because we make our own maps in this house
    result_dict.update({'Palestine - West Bank': {'Air/drone strike': 3, 'Armed clash': 2, 'Attack': 2, 'Remote explosive/landmine/IED': 1, 'Shelling/artillery/missile attack': 5, 'total': np.int64(13)}})
    result_dict.update({'Qatar': {'Air/drone strike': 14, 'Armed clash': 1, 'Shelling/artillery/missile attack': 6, 'total': np.int64(21)}})
    result_dict.update({'Jordan': {'Air/drone strike': 15, 'Remote explosive/landmine/IED': 1, 'Shelling/artillery/missile attack': 13, 'total': np.int64(29)}})

################################################################################
# TAB AI DISCLOSURES + APPENDIX
###############################################################################
with tab_a: 
    st.header("Appendix")
    
    # final section with methodology
    st.markdown("""
    <div style="background-color: #f9f9f9; padding: 20px; border-radius: 8px; margin-top: 30px;">

    ### Methodology & Data Sources

     **Methodology:**
    - Damage rating was assessed manually using reports from various sources (refer to Data Sources). The annotation was also manual.
    - Infographics of the Strait of Hormuz were made using Kirita image diting software and based on WikiImages resources
    - Stock market values reflect the Brent Crude (oil) and the Henry Hub (natural gas) and are pulled on execution using pandas datareader

    **Data Sources:**
    - Satellite Imagery: OpenStreetMaps, Reuters
    - Casualties and Damage Reporting: ACLED.org (Armed Conflict Location and Event Data), Reuters, Middle East Eye, OSINT (Open Source Intelligence)
    - News Sidebar: Dropsite 
    - Economical Reporting: AlJazeera, Henry Hub, Brent Crude Index
    - Fatality monitor data is only from February 28th until April 7th, it will be updated later using ACLED next month for April-March if possible
    - ACLED API is not always reliable and neither is the open-source py-wrapper, this database is downloaded--it also does not reflect demonstartions or abductions
    - The only categories "counted" are war-related eg. air/drone strike, attacks, shellings, IED incidents etc.

    **Maps Notes:**
    - The fatalities monitor map has been intentionally manipulated using ISO-code hacking methods in order to display data from the West Bank, a "disputed territory" according to Plotly developers
    - Custom GeoJSON solutions will be implemented in the future in order to produce a better map, this is largely a workaround, apologies for any geographical bluriness in this region
    - To avoid complicity in apartheid and colonization, both Israeli and Palestinian fatalities beyond the West Bank and Gaza are attributed to Occupied Palestine on the fatalities map
    - To avoid complicity in apartheid and colonization, the fatalities map also denotes the 1945 borders of Lebanon and Syria respectively
    - Any maps on this site that do not reflect the above will eventually be updated to do so
    

    **AI Disclosure:**
    AI was used in the following ways in production:
    - As a website template drafting tool
    - As a debugging tool
    - As a proofreading tool
    - As a news aggregation tool (NOTE: aggregation NOT production of news)

    **Developer's Guarantee:**
    AI was not used in formulating of conclusions, only in compilation of some, but not all, sources--which were always confirmed manually 
    A computer cannot think, therefore a computer cannot be held responsible fo decisions
    
 
    </div>
    """, unsafe_allow_html=True)
     
########################################
# TAB HORMUZ
########################################

with tab_hmz:
    st.header("Strait of Hormuz")
    st.image("PersianGulf_Map_T3.png", caption="The Strait of Hormuz forms a natural chokepoint for military and civilian vessels alike")
    st.markdown("""The Strait of Hormuz is a critical waterway separating Iran from other Persian Gulf countries, serving as a natural chokepoint due to its narrow breadth and relatively shallow, choppy waters. Approximately 21-30% of the world's petroleum-related trade passes through the Strait, which hosts several oil terminals where refined oil completes its journey and becomes ready for export. The region is also vital for natural gas extraction, given its proximity to major natural gas fields, and for seawater desalination infrastructure. While fuel's importance is widely recognized, many petroleum derivatives remain underappreciated despite their critical role in the global economy, including nitrogen fertilizers, clothing-grade polyester, consumer plastics, and numerous pharmaceutical goods such as solvents, binders, and drug coatings. Gulf countries depend heavily on water desalination because the region is naturally water-scarce, and demand has surged unprecedentedly in recent years. Paradoxically, some countries most in need of desalination cannot afford it, though for those that can, it is a lifeline. The Iranian government's armed blockade of the Strait has proven highly effective at raising prices across countless goods and services, pushing the global economy into a precarious situation. While some cargo ships have been permitted passage, only a fraction of necessary volume reaches global markets, leaving East and South Asian countries—which rely disproportionately on Gulf oil—particularly hard-hit. The U.S. naval blockade cannot operate within the Strait itself due to heavy fortification and insufficient depth for most US warships, so the "blockade-on-the-blockade" has been limited to the Gulf of Aden. This geographic constraint has catalyzed significant economic developments in the region, including the exchange of petroleum for Chinese Yuan instead of US Dollars, a major challenge to the petro-dollar system that historically tied petroleum exchanges to a single currency and enabled unilateral economic sanctions. Escalating tensions in the Bab al-Mandeb Strait of Yemen remain a concern, with potential to trigger a third conflict. For now, the Strait of Hormuz persists as a critical natural chokepoint for military and civilian vessels alike, creating a maritime danger zone that transcends the land borders of any single Gulf state. """)
    
    st.divider()
    
    

    # exchange rate: 1 USD = 7.2 CNY
    USD_TO_CNY = 7.2

    # create dropdown menus at the top
    col1, col2 = st.columns(2)

    with col1:
        commodity = st.selectbox(
            "Select Commodity",
            options=["Oil (Brent Crude)", "Natural Gas (Henry Hub)"],
            key="commodity_selector"
        )

    with col2:
        currency = st.selectbox(
            "Select Currency",
            options=["USD", "CNY (Yuan)"],
            key="currency_selector"
        )

    # time series visualization
    st.subheader(f"{commodity} Price - Last 12 Months")

    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
    
        if "Oil" in commodity:
            # fetch Brent crude oil prices
            data = pdr.get_data_fred('DCOILBRENTEU', start=start_date, end=end_date)
            data = data.dropna()
            fred_code = 'DCOILBRENTEU'
            unit = "/barrel"
            line_color = '#1f77b4'
        
        else: # gas
            # fetch natural gas prices
            data = pdr.get_data_fred('DHHNGSP', start=start_date, end=end_date)
            data = data.dropna()
            fred_code = 'DHHNGSP'
            unit = "/MMBtu"
            line_color = '#ff7f0e'
    
        if len(data) > 0:
            # convert currency if needed
            y_values = data[fred_code].values
            if currency == "CNY (Yuan)":
                y_values = y_values * USD_TO_CNY
                currency_symbol = "¥"
                currency_label = "CNY"
            else:
                currency_symbol = "$"
                currency_label = "USD"
        
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=data.index,
                y=y_values,
                mode='lines',
                name='Price',
                line=dict(color=line_color, width=2),
                hovertemplate=f'<b>%{{x|%Y-%m-%d}}</b><br>{currency_symbol}%{{y:.2f}}{unit}<extra></extra>'
            ))
        
            fig.update_layout(
                title=f"Live {commodity} Prices",
                xaxis_title="Date",
                yaxis_title=f"Price ({currency_label}{unit})",
                hovermode='x unified',
                height=500,
                margin=dict(l=50, r=20, t=50, b=50)
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error(f"No {commodity.lower()} price data available")
        
    except Exception as e:
        st.error(f"Unable to fetch price data: {type(e).__name__}: {str(e)}")

##################################################
# stats 
    st.divider()
    st.subheader("Key Insights")
    
    insights_col1, insights_col2 = st.columns(2)
    
    with insights_col1:
        st.metric("Oil prices are increasing:", "Brent Crude", "65%")
        
    with insights_col2:
        st.metric("Natural gas prices are increasing:", "HenryHub Natural Gas", "20%")
       
##################################################
    
    # create two columns
    col1, col2 = st.columns(2)
    
    # ============= COLUMN 1: Gulf Desalinated Water =============
    with col1:
        st.subheader("Desalinated Water Reliance by Country")
        
        # data: % of freshwater supply from desalination
        water_data = {
            "Country": ["Qatar", "Bahrain", "Occupied Palestine", "Kuwait", "United Arab Emirates", "Oman",
                       "Saudi Arabia", "Iraq", "Iran", "Jordan"],
            "Reliance (%)": [61, 59, 50, 47, 41, 23, 18, 10, 3, 0.99]
        }
        
        water_df = pd.DataFrame(water_data)
        water_df = water_df.sort_values("Reliance (%)", ascending=True)
        
        # create horizontal bar chart
        fig1 = go.Figure(data=[
            go.Bar(
                y=water_df["Country"],
                x=water_df["Reliance (%)"],
                orientation='h',
                marker=dict(color= "#194a7a", opacity=0.8),
                text=water_df["Reliance (%)"].astype(str) + "%",
                textposition='auto',
            )
        ])
        
        fig1.update_layout(
            xaxis_title="% of Desalinated Water in Use",
            yaxis_title="Country",
            height=500,
            margin=dict(l=100, r=20, t=20, b=50),
            showlegend=False,
            hovermode='closest'
        )
        
        st.plotly_chart(fig1, use_container_width=True)
    
    # ============= COLUMN 2: Gulf Oil Reliance =============
    with col2:
        st.subheader("Reliance on Gulf Oil Imports")
        
        # % of oil imports from Gulf region
        oil_data = {
            "Country": ["China", "India", "South Korea", "Japan"],
            "Gulf Oil Reliance (%)": [45, 65, 70, 82]
        }
        
        oil_df = pd.DataFrame(oil_data)
        
        fig2 = go.Figure(data=[
        go.Bar(
        x=oil_df["Country"],
        y=oil_df["Gulf Oil Reliance (%)"],
        marker=dict(color=[
            "#194a7a",     # navy blue
            "#78938a",     # darkish green
            "#525e75",     # darkish blue
            "#cfd5dc"      # pale grey
        ], opacity=0.8),
        text=oil_df["Gulf Oil Reliance (%)"].astype(str) + "%",
        textposition='auto')])

        
        fig2.update_layout(
            xaxis_title="Country",
            yaxis_title="% of Oil Imports from Gulf",
            height=500,
            margin=dict(l=50, r=20, t=20, b=50),
            showlegend=False,
            hovermode='closest',
            yaxis=dict(range=[0, 100])
        )
        
        st.plotly_chart(fig2, use_container_width=True)
    
  


    
############################################################
# TAB IRAN-LEBANON
############################################################


with tab_irlb:
    
    st.header("Damage and Recovery Assessment Maps")

    st.markdown("""
    While an aerial ceasefire holds in Iran, Lebanon is still under fire. This interactive map of all eight governates is regularly updated with recent strike locations and corresponding damage reports.
    """)


    st.info("💡 **Tip:** Click on map markers to view detailed strike reports for specific locations.")

    l = create_lebanon_damage_map()
    st_folium(l, width=1000, height=800)

    st.warning("⚠️ **Note:** Data is current as of April 2026. Some areas may have limited accessibility. Please note all fatalities are civilian in nature.")

    # article/content area
    st.markdown("""
    <div style="background-color: #f0f2f6; padding: 20px; border-radius: 8px; margin: 20px 0;">

    **Situation Summary:**

    Lebanon is being subject to one of the most brutal bombing campaigns in recent history, begining to outpace some previous US bombardments in Iraq and Afghanistan. The southern provinces are disproportionately affected. This is the sixth IDF invasion attempt of Lebanon over all.  

    </div>
    """, unsafe_allow_html=True)

    # Pull quote
    st.markdown("""
    <div style="border-left: 4px solid #1f77b4; padding-left: 20px; margin: 30px 0; font-style: italic; color: #555;">

    "A ceasefire was supposed to be implemented on April 16th, but that is not the reality I am hearing from families on the ground"

    <p style="margin-top: 10px; font-size: 0.9em; color: #888;">— Rashida Tlaib</p>

    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.write("This interactive provincial map of Iran provides detailed damage and recovery assessment estimates.")
    st.info("💡 **Tip:** Click on map markers to view detailed damage and recovery reports for specific locations.")


    # maps
    m = create_iran_damage_map()
    st_folium(m, width=1000, height=800)

    st.warning("⚠️ **Note:** Data is current as of April 2026. Some areas may have limited accessibility. Please note that all fatalities are civilian in nature.")

    # article/content area
    st.markdown("""
    <div style="background-color: #f0f2f6; padding: 20px; border-radius: 8px; margin: 20px 0;">

    **Situation Summary:**

    While the damage in Iran is extensive, an aerial ceasefire is holding and repair efforts are underway. The approximate cost is 20 billion (USD) with public infrastructure such as railways and airports taking priority.
    Sources estimate that it is unlikely that this ceasefire will hold permanenetly, however. 
    </div>
    """, unsafe_allow_html=True)

    # Pull quote
    st.markdown("""
    <div style="border-left: 4px solid #1f77b4; padding-left: 20px; margin: 30px 0; font-style: italic; color: #555;">

    "A full ceasefire remains unlikely in Iran. This, we are hearing, is more of a pause."

    <p style="margin-top: 10px; font-size: 0.9em; color: #888;">— Middle East Eye Editorial Board </p>

    </div>
    """, unsafe_allow_html=True)

    

    

    
##############################################################
# WEST ASIA
###############################################################
with tab_we:
    st.header("Linked View Fatality Monitor - West Asia")

    st.markdown("""ACLED data, civilian harm across West Asia since late February has been increasing. While this feels obvious due to ongoing wars, it is important to observe these numbers because recent media reports in many countries have been reticent to discuss these disheareningly high death tolls for various practical and emotional reasons. Iran and Lebanon have experienced the heaviest toll, with massive displacement and extensive damage to civilian infrastructure. Civilians across the entire Gulf have faced ongoing anxiety from strikes on energy facilities, airports, and ports, with migrant workers among the vulnerable populations exposed to the violence. Beyond direct strikes, the broader effects—including displacement, disruptions to electricity and essential goods, and damage to cultural heritage—have compounded the humanitarian crisis across the region. While ACLED collects all kinds of conflict related data including protests, abductions, military fatalities and more, only civilian fatalities related to wartime violence have been counted here.

    """, unsafe_allow_html=True)

    # Add an intro section
    st.info("💡 **Tip:** Use the dropdown to select the region of your choice.")
    
    # real data
    casualty_data = result_dict
    
    # ISO country codes for choropleth
    iso_codes = {
        "Palestine - Gaza": "PSE",
        "Occupied Palestine": "ISR",
        "Palestine - West Bank": "NIU",
        "Lebanon": "LBN",
        "Syria": "SYR",
        "Jordan": "JOR",
        "Iran": "IRN",
        "Iraq": "IRQ",
        "Saudi Arabia": "SAU",
        "Yemen": "YEM",
        "Oman": "OMN",
        "Kuwait": "KWT",
        "Qatar": "QAT",
        "Bahrain": "BHR",
        "United Arab Emirates": "ARE",
        "Turkey": "TUR"
    }
    
    # prepare data for choropleth
    df_map = pd.DataFrame({
        "country": list(casualty_data.keys()),
        "iso_alpha": [iso_codes[c] for c in casualty_data.keys()],
        "total_deaths": [casualty_data[c]["total"] for c in casualty_data.keys()]
    })

    # Store selected country in session state
    if "selected_country_we" not in st.session_state:
        st.session_state.selected_country_we = ""

    # Create a container for the map
    map_container = st.container()
    
    with map_container:
        # Determine color scale based on selection
        selected_country = st.session_state.selected_country_we
        
        if selected_country and selected_country in casualty_data:
            # Create custom color mapping: grey for all except selected (red)
            df_map['color_value'] = df_map['country'].apply(
                lambda x: casualty_data[x]["total"] if x == selected_country else 0
            )
            color_scale = "Reds"
            z_max = casualty_data[selected_country]["total"]
        else:
            # All grey when nothing selected
            df_map['color_value'] = 1  # Uniform grey
            color_scale = [[0, "#d3d3d3"], [1, "#d3d3d3"]]  # Grey
            z_max = 1
        
        # Create choropleth
        fig_choropleth = px.choropleth(
            df_map,
            locations="iso_alpha",
            color="color_value",
            hover_name="country",
            hover_data={"iso_alpha": False, "total_deaths": ":,", "color_value": False},
            color_continuous_scale=color_scale,
            scope="asia"
        )

        # Add Palestine - West Bank as a custom marker
        wb_color = "#8b0000" if selected_country == "West Bank" else "#d3d3d3"
        fig_choropleth.add_trace(go.Scattergeo(
            lon=[35.23],
            lat=[31.95],
            mode="markers",
            marker=dict(size=20, color=wb_color, symbol="circle"),
            hovertemplate="<b>Palestine - West Bank</b><br>Deaths: %{customdata[0]:,}",
            customdata=[[casualty_data["Palestine - West Bank"]["total"]]],
            name="*Estimated, not in ACLED data"
        ))

        
        fig_choropleth.update_layout(
            geo=dict(
                center=dict(lat=28, lon=48),
                projection_scale=3.5
            ),
            coloraxis_colorbar=dict(
                title="Deaths",
                tickformat=",",
                thickness=15,
                len=0.7
            ) if selected_country else dict(),
            height=500,
            margin=dict(l=0, r=0, t=0, b=0)
        )
        
        st.plotly_chart(fig_choropleth, use_container_width=True)

        st.warning("⚠️ Sadly, Plotly defaults do not include Bahrain on maps due to its small size. Data for Bahrain is still available in chart form after selecting it from the menu.")
    

    # Country selection
    selected_country = st.selectbox(
        "Select a country to view casualty details:",
        options=[""] + list(casualty_data.keys()),
        format_func=lambda x: "Choose a country" if x == "" else x,
        key="country_select_we",
        on_change=lambda: st.session_state.update({"selected_country_we": st.session_state.country_select_we})
    )
    
    # Update session state
    st.session_state.selected_country_we = selected_country

    # Display donut chart only if country is selected
    if selected_country:
        st.subheader(f"Casualties - {selected_country}")
    
        data = casualty_data[selected_country]
    
        # Define categories
        categories = [
            'Air/drone strike',
            'Shelling/artillery/missile attack',
            'Attack',
            'Armed clash',
            'Remote explosive/landmine/IED'
        ]
        values = [data.get(cat, 0) for cat in categories]
    
        # Filter out zero values
        non_zero_data = [(cat, val) for cat, val in zip(categories, values) if val > 0]
    
        if non_zero_data:
            categories, values = zip(*non_zero_data)
            
            # Professional, understated color palette
            colors = [
                "194a7a",   # navy blue
                "#78938a",  # darkish green
                "#525e75",  # darkish blue
                "#f1ddbf",  # sandy biscuit 
                "#CFD5DC"   # pale grey
            ]
            
            fig_casualties = go.Figure(
                data=[go.Pie(
                    labels=categories,
                    values=values,
                    hole=0.4,
                    marker=dict(colors=colors[:len(categories)]),
                    text=[f"{v:,}" for v in values],
                    textposition="inside",
                    textfont=dict(size=12, color="white"),
                    hovertemplate="<b>%{label}</b><br>Deaths: %{value:,}<extra></extra>"
                )]
            )
        
            fig_casualties.update_layout(
                title=f"Total Deaths: {data.get('total', 0):,}",
                height=400,
                showlegend=True,
                legend=dict(
                    orientation="v",
                    yanchor="middle",
                    y=0.5,
                    xanchor="left",
                    x=1.02
                ),
                margin=dict(l=50, r=150, t=50, b=50),
                font=dict(family="Arial, sans-serif", size=11, color="#333333")
            )
        
            st.plotly_chart(fig_casualties, use_container_width=True)
        else:
            st.info(f"No casualty data available for {selected_country}")


###########################################################################
# SIDEBAR AND ACCENTS 
###########################################################################


st.set_page_config(initial_sidebar_state="expanded")

@st.cache_data(ttl=300)
def fetch_rss_news():
    """Fetch and filter RSS feeds for Iran and Lebanon"""
    feeds = [
        "https://feeds.reuters.com/reuters/worldNews",
        "https://feeds.bbc.co.uk/news/world/rss.xml",
        "https://feeds.bloomberg.com/markets/news.rss",
    ]
    
    articles = []
    keywords = ["Iran", "Lebanon"]
    
    for feed_url in feeds:
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:10]:
                title = entry.get("title", "").lower()
                if any(keyword in title for keyword in keywords):
                    articles.append({
                        "title": entry.get("title", "No title"),
                        "link": entry.get("link", "#"),
                        "source": feed.feed.get("title", "Unknown"),
                    })
        except:
            pass
    
    return articles[:5]

# Display in sidebar
st.sidebar.header("📰 Live News")
articles = fetch_rss_news()

if articles:
    for article in articles:
        st.sidebar.markdown(f"**{article['title'][:60]}...**")
        st.sidebar.caption(article["source"])
        st.sidebar.link_button("Read", article["link"], use_container_width=True)
else:
    st.sidebar.info("No articles found")

