import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

st.set_page_config(page_title="COVID India Dashboard", layout="wide")

st.title("🦠 COVID-19 India Analysis Dashboard")

@st.cache_data
def load_data():
    covid = pd.read_csv("covid_19_india.csv")
    vaccine = pd.read_csv("covid_vaccine_statewise.csv")

    covid.drop(
        ['Sno','ConfirmedIndianNational','ConfirmedForeignNational'],
        axis=1,
        inplace=True,
        errors='ignore'
    )

    covid['Active_Cases'] = covid['Confirmed'] - (
        covid['Cured'] + covid['Deaths']
    )

    return covid, vaccine

covid, vaccine = load_data()

menu = st.sidebar.selectbox(
    "Select Section",
    ["Overview","Statewise Analysis","Top Active Cases","Vaccination Analysis"]
)

if menu == "Overview":
    st.subheader("COVID Dataset")
    st.dataframe(covid.head())

    st.subheader("Vaccination Dataset")
    st.dataframe(vaccine.head())

elif menu == "Statewise Analysis":
    statewise = pd.pivot_table(
        covid,
        values=['Confirmed','Deaths','Cured'],
        index='State/UnionTerritory',
        aggfunc=max
    )

    statewise['Recovery Rate'] = (
        statewise['Cured']*100/statewise['Confirmed']
    )

    statewise['Mortality Rate'] = (
        statewise['Deaths']*100/statewise['Confirmed']
    )

    st.subheader("Statewise COVID Summary")
    st.dataframe(statewise.sort_values(
        by='Confirmed',ascending=False
    ))

elif menu == "Top Active Cases":
    top_states = covid.groupby(
        'State/UnionTerritory'
    ).max()[['Active_Cases']].sort_values(
        by='Active_Cases',
        ascending=False
    ).head(10)

    fig = plt.figure(figsize=(10,5))
    sns.barplot(
        data=top_states.reset_index(),
        x='State/UnionTerritory',
        y='Active_Cases'
    )
    plt.xticks(rotation=45)

    st.pyplot(fig)

elif menu == "Vaccination Analysis":

    male = vaccine['Male (Doses Administered)'].sum()
    female = vaccine['Female (Doses Administered)'].sum()

    fig = px.pie(
        names=['Male','Female'],
        values=[male,female],
        title="Male vs Female Vaccination"
    )

    st.plotly_chart(fig)

