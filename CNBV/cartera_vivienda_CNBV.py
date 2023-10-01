#Instalar librerías

import pandas as pd
import streamlit as st
import plotly.express as px

#Leer la información

url = 'https://bit.ly/cartera_vivienda'
df = pd.read_excel(url, sheet_name='IMOR', dtype=str)
df1 = pd.read_excel(url, sheet_name='Acumulado')

#Procesar la información
#IMOR

df_IMOR = df.copy()

replacement_keywords = ["#N/D", "n. a.", "n.a.", "n.d.", 'n. d.', 'n.a']

for keyword in replacement_keywords:
    df_IMOR = df_IMOR.replace({keyword: 0})

df_IMOR.drop_duplicates(subset=['Entidad'], keep='last', inplace=True)
df_IMOR.set_index('Entidad', inplace=True)
df_IMOR = df_IMOR.apply(lambda col: col.astype(float) if col.name != 'Entidad' else col)
df_IMOR = df_IMOR.transpose()
df_IMOR.reset_index(inplace=True)
df_IMOR.rename(columns={'Sistema */': 'Sistema'}, inplace=True)

#Saldo de Cartera

df_Saldo = df1.copy()

replacement_keywords = ["#N/D", "n. a.", "n.a.", "n.d.", 'n. d.', 'n.a']

for keyword in replacement_keywords:
    df_Saldo = df_Saldo.replace({keyword: 0})

df_Saldo.drop_duplicates(subset=['Entidad'], keep='last', inplace=True)
df_Saldo.set_index('Entidad', inplace=True)
df_Saldo = df_Saldo.apply(lambda col: col.astype(float) if col.name != 'Entidad' else col)
df_Saldo = df_Saldo.transpose()
df_Saldo.reset_index(inplace=True)
df_Saldo.rename(columns={'Sistema */': 'Sistema', 'BBVA MÃ©xico': 'BBVA México',
                         'DondÃ© Banco': 'Dondé Banco', 'BansÃ­':'Bansí', 
                         'Ve por MÃ¡s': 'Ve por Más', 'Banco del BajÃ­o': 'Banco del Bajío' }
                         , inplace=True)

#Crecimiento anual saldo de cartera

df_pct = df_Saldo.copy()
df_pct.set_index('index', inplace=True)
df_pct = df_pct.pct_change()*100
df_pct.fillna(0, inplace=True)
df_pct = df_pct.loc["2019":"2023"]
df_pct.reset_index(inplace=True)

df_pct_anual = df_Saldo.copy()
df_pct_anual.set_index('index', inplace=True)
df_pct_anual = df_pct_anual.pct_change(periods=12)*100
df_pct_anual.fillna(0, inplace=True)
df_pct_anual = df_pct_anual.loc["2019":"2023"]
df_pct_anual.reset_index(inplace=True)

#Aquí empieza Streamlite

entidades = ( 'Sistema', 'BBVA México', 'Santander', 'Banamex', 'Banorte',
       'HSBC', 'Scotiabank', 'Inbursa', 'Bank of America', 'Banco del Bajío',
       'Afirme', 'Banco Azteca', 'J.P. Morgan', 'Monex', 'Banregio', 'Invex',
       'Multiva', 'Barclays', 'Banca Mifel', 'Ve por Más', 'CIBanco',
       'Compartamos', 'Bansí', 'Banco Base', 'Actinver', 'Consubanco',
       'Sabadell', 'Inmobiliario Mexicano', 'Autofin', 'BNP Paribas México',
       'Mizuho Bank', 'American Express', 'Bank of China', 'Bankaool', 'ICBC',
       'KEB Hana México', 'Banco S3', 'Shinhan', 'Banco Covalto',
       'ABC Capital', 'Volkswagen Bank', 'Deutsche Bank', 'Forjadores',
       'Dondé Banco', 'Pagatodo')

entidades2 = ('Sistema', 'BBVA México', 'Santander', 'Banamex', 'Banorte',
       'HSBC', 'Scotiabank', 'Inbursa', 'Banco del Bajío', 'J.P. Morgan',
       'Banco Azteca', 'Afirme', 'Bank of America', 'Banregio', 'Multiva',
       'Invex', 'Monex', 'Banca Mifel', 'Barclays', 'Ve por Más', 'CIBanco',
       'Banco Base', 'Actinver', 'Compartamos', 'Bansí', 'Sabadell',
       'American Express', 'Consubanco', 'ABC Capital',
       'Inmobiliario Mexicano', 'Volkswagen Bank', 'Autofin', 'ICBC',
       'Deutsche Bank', 'Mizuho Bank', 'Shinhan', 'Bankaool', 'Dondé Banco',
       'Forjadores')

#Saldo de Cartera

#st.snow()

st.set_page_config(page_title="Análisis Banca | Edgar Trejo")


st.title(":green[Análisis de la cartera de crédito a la vivienda de la Banca Comercial]")

st.markdown("---")

st.markdown("*Con cifras de las CNBV al me    s de Junio 2023 | Portafolio de Infomación de la Comisión Nacional Bancaria y de Valores(CNBV)*")

st.markdown(":link: **[Página de la CNBV](https://portafolioinfo.cnbv.gob.mx/Paginas/Inicio.aspx)**")

st.markdown(":link: Elaborado por: **[Edgar Trejo](https://linkedin.com/in/edgar-trejo-03077748)**")

st.markdown(":link:**[GitHub](https://github.com/EdgarTrejoh)**")

st.markdown("---")
#st.link_button("CNBV", "https://portafolioinfo.cnbv.gob.mx/Paginas/Inicio.aspx")

st.header(":blue[Saldo de Cartera]", divider="orange")

st.text("Cifras en mdp.")

st.data_editor(df_Saldo, column_config={
                "index": st.column_config.DatetimeColumn(
                "Periodo de información:",
                format="D MMM YYYY",
            )
        },
    hide_index=True,
   )


st.markdown("**Tabla 1.** Fuente: Portafolio de información CNBV")

st.header(":blue[**Gráfica:** Saldo de Cartera]", divider="orange")

left_column, right_column = st.columns(2)

with left_column:
    chosen = st.selectbox(
        'Selecciona una Entidad Financiera',
        (entidades))
    st.write(f"Entidad Financiera seleccionada: {chosen} ")

right_column.line_chart(data=df_Saldo,  y=df_Saldo[["Sistema", chosen]])

st.markdown("**Gráfica 1.** Elaboración propia. Fuente: Portafolio de información CNBV")

st.divider()
st.subheader(":blue[Saldo de Cartera: Crecimiento mensual y anual]")
st.divider()

tab1, tab2 = st.tabs(["📈Gráfica mensual", "📈Gráfica anual" ])

fig = px.line(df_pct, x='index', y=df_pct.columns, title="Saldo de Cartera: Crecimiento mensual")

tab1.subheader("Gráfica Mensual")
tab1.plotly_chart(fig, theme="streamlit", use_container_width=True)
st.markdown("**Gráfica 2.** Información mensual. Elaboración propia. Fuente: Portafolio de información CNBV")

tab2.subheader("Gráfica Anual")

fig2 = px.line(df_pct_anual, x='index', y=["BBVA México","Banorte","Santander","Scotiabank","HSBC","Banamex"],
               title="Principales Entidades Financieras. Saldo de Cartera: Crecimiento Anual")

tab2.plotly_chart(fig2, theme="streamlit", use_container_width=True)
st.markdown("**Gráfica 3.** Información anual. Elaboración propia. Fuente: Portafolio de información CNBV")

#IMOR

st.header(":blue[Índice de Morosidad: IMOR]", divider="orange")

tab1, tab2 = st.tabs(["📈Gráfica", "🗃 Tabla" ])

fig3 = px.line(df_IMOR, x='index', y=df_IMOR.columns, title="IMOR")

tab1.subheader("Gráfica IMOR")
tab1.plotly_chart(fig3, theme="streamlit", use_container_width=True)
st.markdown("**Gráfica 4.** Elaboración propia. Fuente: Portafolio de información CNBV")

tab2.subheader("Tabla de Datos")

tab2.data_editor(df_IMOR, column_config={
                "index": st.column_config.DatetimeColumn(
                "Periodo de información:",
                format="D MMM YYYY",
            )
        },
    hide_index=True, 
   )
st.markdown("**Tabla 2.** Fuente: Portafolio de información CNBV")

st.header(":blue[**Gráfica: Índice de Morosidad**]", divider="orange")

left_column, right_column = st.columns(2)

with left_column:
    chosen = st.selectbox(
        'Selecciona una Entidad Financiera',
        (entidades2))
    st.write(f"Entidad Financiera seleccionada: {chosen} ")

right_column.line_chart(data=df_IMOR,  y=df_IMOR[["Sistema", chosen]])
st.markdown("**Gráfica 5.** Elaboración propia. Fuente: Portafolio de información CNBV")

st.divider()
st.subheader(":blue[IMOR: Principales Entidades Financieras]")
st.divider()

fig4 = px.line(df_IMOR, x='index', y=["BBVA México","Banorte","Santander","Scotiabank","HSBC","Banamex"])
st.plotly_chart(fig4, theme="streamlit", use_container_width=True)
st.markdown("**Gráfica 6.** Elaboración propia. Fuente: Portafolio de información CNBV")