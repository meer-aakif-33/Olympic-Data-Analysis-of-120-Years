import streamlit as st
import pandas as pd
import preprocessor,helper
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.figure_factory as ff

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df, region_df)

st.sidebar.title("Olympics Analysis")
st.sidebar.image('https://logo-marque.com/wp-content/uploads/2021/09/Olympics-Logo-1913-1986.jpg')
user_menu = st.sidebar.radio(
    'Select an option',
    ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete wise Analysis')
)

#st.dataframe(df)

if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years, country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tallyy = helper.fetch_medal_tallyy(df, selected_year, selected_country)

    if selected_year =='Overall' and selected_country == 'Overall':
        st.title("Overall Tally")
    if selected_year !='Overall' and selected_country == 'Overall':
        st.title("Medal Tally in " + str(selected_year) + " Olympics")
    if selected_year =='Overall' and selected_country != 'Overall':
        st.title(selected_country + " Overall performance")
    if selected_year !='Overall' and selected_country != 'Overall':
        st.title(selected_country + " performance in " + str(selected_year) + " Olympics")

    st.table(medal_tallyy)
if user_menu == 'Overall Analysis':
    editiions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    nations = df['region'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]

    st.title("Top statistics")
    col1, col2,col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editiions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2,col3 = st.columns(3)

    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)

    nations_over_time = helper.data_over_time(df, 'region')
    fig = px.line(nations_over_time, x="Edition", y="region")
    st.title("Parcipating Nations over the years")
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(events_over_time, x="Edition", y="Event")
    st.title("Events over the years")
    st.plotly_chart(fig)

    athletes_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athletes_over_time, x="Edition", y="Name")
    st.title("Athletes over the years")
    st.plotly_chart(fig)


    st.title("No. of Events over time(Every Sport)")
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])

    pivot_df = x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int')
    fig, axis = plt.subplots(figsize=(25, 25))  
    sns.heatmap(pivot_df, ax=axis, annot=True, fmt="d")  # Add numbers with annot=True
    st.pyplot(fig)

    st.title("Most successfull Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()

    sport_list.insert(0, 'Overall')

    selected_sport = st.selectbox('Select a Sport',sport_list)
    x = helper.most_successful(df, selected_sport)
    st.table(x)

if user_menu == 'Country-wise Analysis':

    st.title("Country wise Analysis")
    country_list = df['region'].dropna().unique().tolist()
    #or just drop the na values as done above country_list = df['region'].unique().tolist()
    # country_list = [str(country) for country in country_list]
    country_list.sort()


    selected_country = st.selectbox('Select a Sport',country_list)

    country_df = helper.yearwise_medal_tally(df, selected_country)

    fig = px.line(country_df, x="Year", y="Medal")
    st.title(selected_country+" Medal Tally over the years")
    st.plotly_chart(fig)

    st.title(selected_country +" excels in the following sports")
    pt = helper.country_event_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(25, 25))  

    if not pt.empty:
        pt_filled = pt.fillna(0)  # Replace NaN with 0
        ax = sns.heatmap(pt_filled, annot=True)
        st.pyplot(fig)
    else:
        st.warning("Heatmap cannot be displayed because the data is empty.")

    st.title("Top 10 athlethes of "+ selected_country)
    top10_df = helper.most_successful_athletes_country_wise(df, selected_country)
    st.table(top10_df)

if user_menu == 'Athlete wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    x1 = athlete_df['Age'].dropna()

    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Bronze Medalist','Silver Medalist'], show_hist=False, show_rug=False)

    fig.update_layout(autosize=False, width=1000, height=680)
    st.title("Distribution of Age")
    st.plotly_chart(fig)

    x = []
    name = []

    # famous_sports = athlete_df['Sport'].value_counts().head(25).index.tolist()

    famous_sports = [
    "Football", "Tug-of-War", "Art Competitions", "Weightlifting", "Wrestling",
    "Water Polo", "Hockey", "Rowing", "Fencing", "Shooting", "Boxing", "Taekwondo",
    "Cycling", "Diving", "Ice Hockey", "Basketball", "Judo", "Swimming",
    "Badminton", "Sailing", "Gymnastics", "Athletics", "Canoeing", "Tennis",
    "Golf", "Softball", "Archery", "Volleyball", "Synchronized Swimming",
    "Table Tennis", "Baseball", "Rhythmic Gymnastics", "Rugby Sevens",
    "Beach Volleyball", "Triathlon", "Rugby"]

    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        ages = temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna()

        if not ages.empty:  # Ensure non-empty data
            x.append(ages)
            name.append(sport)
    
    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)

    fig.update_layout(autosize=False, width=1000, height=680)
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)




    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()

    sport_list.insert(0, 'Overall')

    selected_sport = st.selectbox('Select a Sport',sport_list)

    temp_df = helper.weight_vs_height(df, selected_sport)
    fig, ax = plt.subplots()

    ax = sns.scatterplot(x=temp_df['Weight'], y=temp_df['Height'], hue=temp_df["Medal"], style=temp_df['Sex'], s=50)
    st.title("Height vs Weight")
    st.pyplot(fig)

    st.title("Men vs Women participation over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x='Year', y=['Male', 'Female'])
    fig.update_layout(autosize=False, width=1000, height=680)

    st.plotly_chart(fig)