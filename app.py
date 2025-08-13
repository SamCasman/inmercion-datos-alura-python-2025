import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Dashboard de Salários en el Área de Datos",
    page_icon="📊",
    layout="wide",
)

df = pd.read_csv("https://github.com/SamCasman/inmercion-datos-alura-python-2025/blob/main/DatosAulaFinal.csv?raw=true")

st.sidebar.header("🔍 Filtros")

años_disponibles = sorted(df['año_trabajo'].unique())
años_selecionados = st.sidebar.multiselect("año_trabajo", años_disponibles, default=años_disponibles)

nivel_experiencia_disponibles = sorted(df['nivel_experiencia'].unique())
nivel_experiencia_selecionadas = st.sidebar.multiselect("nivel_experiencia", nivel_experiencia_disponibles, default=nivel_experiencia_disponibles)

contrato_disponible = sorted(df['puesto'].unique())
contratos_selecionados = st.sidebar.multiselect("Tipo de Contrato", contrato_disponible, default=contrato_disponible)

tamaños_disponibles = sorted(df['tamaño_empresa'].unique())
tamaños_selecionados = st.sidebar.multiselect("Tamaño de la Empresa", tamaños_disponibles, default=tamaños_disponibles)

df_filtrado = df[
    (df['año_trabajo'].isin(años_selecionados)) &
    (df['nivel_experiencia'].isin(nivel_experiencia_selecionadas)) &
    (df['puesto'].isin(contratos_selecionados)) &
    (df['tamaño_empresa'].isin(tamaños_selecionados))
]

st.title("🎲 Dashboard de Análisis de Salarios en el Área de Datos")
st.markdown("Explore los datos salariales en el área de datos de los últimos años. Utilize los filtros de la izquierda para refinar su análisis.")

st.subheader("Métricas generales (Salario anual en USD)")

if not df_filtrado.empty:
    salario_medio = df_filtrado['salario_en_usd'].mean()
    salario_maximo = df_filtrado['salario_en_usd'].max()
    total_registros = df_filtrado.shape[0]
    cargo_mas_frecuente = df_filtrado["puesto"].mode()[0]
else:
    salario_medio, salario_mediano, salario_maximo, total_registros, cargo_mas_comum = 0, 0, 0, ""

col1, col2, col3, col4 = st.columns(4)
col1.metric("Salário médio", f"${salario_medio:,.0f}")
col2.metric("Salário máximo", f"${salario_maximo:,.0f}")
col3.metric("Total de registros", f"{total_registros:,}")
col4.metric("Cargo mas frecuente", cargo_mas_frecuente)

st.markdown("---")

st.subheader("Gráficos")

col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    if not df_filtrado.empty:
        top_cargos = df_filtrado.groupby('puesto')['salario_en_usd'].mean().nlargest(10).sort_values(ascending=True).reset_index()
        grafico_cargos = px.bar(
            top_cargos,
            x='salario_en_usd',
            y='puesto',
            orientation='h',
            title="Top 10 puestos por salario medio",
            labels={'salario_en_usd': 'Media salarial anual (USD)', 'puesto': ''}
        )
        grafico_cargos.update_layout(title_x=0.1, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(grafico_cargos, use_container_width=True)
    else:
        st.warning("Ningun dato para exibir en el gráfico de cargos.")

with col_graf2:
    if not df_filtrado.empty:
        grafico_hist = px.histogram(
            df_filtrado,
            x='salario_en_usd',
            nbins=30,
            title="Distribución de salarios anuales",
            labels={'salario_en_usd': 'Rango salarial (USD)', 'count': ''}
        )
        grafico_hist.update_layout(title_x=0.1)
        st.plotly_chart(grafico_hist, use_container_width=True)
    else:
        st.warning("Ningun dato para exibir en el gráfico de distribución.")

col_graf3, col_graf4 = st.columns(2)

with col_graf3:
    if not df_filtrado.empty:
        remoto_contage = df_filtrado['remoto'].value_counts().reset_index()
        remoto_contage.columns = ['tipo_empleo', 'cantidad']
        grafico_remoto = px.pie(
            remoto_contage,
            names='tipo_empleo',
            values='cantidad',
            title='Proporción de los tipos de empleo',
            hole=0.5
        )
        grafico_remoto.update_traces(textinfo='percent+label')
        grafico_remoto.update_layout(title_x=0.1)
        st.plotly_chart(grafico_remoto, use_container_width=True)
    else:
        st.warning("Ningun dato para exibir en el gráfico de tipos de empleo.")

with col_graf4:
    if not df_filtrado.empty:
        df_ds = df_filtrado[df_filtrado['puesto'] == 'Data Scientist']
        media_ds_pais = df_ds.groupby('residencia_iso3')['salario_en_usd'].mean().reset_index()
        grafico_paises = px.choropleth(media_ds_pais,
            locations='residencia_iso3',
            color='salario_en_usd',
            color_continuous_scale='rdylgn',
            title='Salario medio de Cientista de Datos por país',
            labels={'salario_en_usd': 'Salario medio (USD)', 'residencia_iso3': 'País'})
        grafico_paises.update_layout(title_x=0.1)
        st.plotly_chart(grafico_paises, use_container_width=True)
    else:
        st.warning("Ningun dato para exibir en el gráfico de países.")

st.subheader("Datos Detallados")
st.dataframe(df_filtrado)
