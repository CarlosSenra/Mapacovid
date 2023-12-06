import funcoes
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import json
from datetime import date, timedelta

#print(date(2020, 1, 1).year)


# dados mensais
#df_principal = pd.read_csv('https://drive.google.com/uc?id=107RDHErgijFiI3LQRVbSVLOOurFmtit6')
df_principal = pd.read_csv(funcoes.pegaarquivo_pasta('dados_mensais.csv'))
df_principal.drop(columns='Unnamed: 0',
                  inplace=True)
df_principal.data = pd.to_datetime(df_principal.data)

df_principal = df_principal[df_principal.data < '2023-01-01']

df_populacao = pd.read_csv(funcoes.pegaarquivo_pasta('populacao.csv'))

lista_estados = list(df_principal.estado.unique())
lista_estados.sort()
lista_estados = np.array(lista_estados)




# Adiciona uma sidebar
st.sidebar.title("Opções")

# Adiciona widgets à sidebar
add_radio = st.sidebar.radio(
        "Escolha entre Casos registrados ou Óbitos registrados",
        ("Casos", "Óbitos")
    )
st.sidebar.divider()
st.sidebar.write("Valores negativos são explicados pelas correções diárias(em meses específicos) nos dados retirados em 'covid.saude.gov.br'.")    
# Exibe o resultado na página principal
if add_radio == "Casos":            # definindo as tab mensal
        
        st.title("Mapas de Casos Mensais Covid-19")
        st.write("Selecione um Estado:")
        
        estado_box = st.selectbox("mes",label_visibility ="collapsed",
                                    options=[x for x in lista_estados])
        
        ano_min,mes_min,dia_min = funcoes.retorna_date(df_principal.data.min())
        ano_max,mes_max,dia_max = funcoes.retorna_date(df_principal.data.max())
        
        d = st.date_input("Selecione uma data. (Os dados são mensais - AAAA/MM/DD)",
                            date(ano_min, mes_min, dia_min),
                            min_value = date(ano_min, mes_min, dia_min), 
                            max_value = date(ano_max,mes_max,dia_max)
                            )
        
        
        mapa_absoluto = funcoes.mapa_absoluto(df_principal,"Casos",estado_box,d.year,d.month)
        mapa_taxa = funcoes.mapa_taxa(df_principal,df_populacao,"Casos",estado_box,d.year,d.month)

        #criando duas colunas
        col1, col2 = st.columns(2)
    
        # Define o conteúdo de cada coluna
        # cada coluna contem um mapa
        
        with col1:
            st.markdown("#### Mapa casos mensais absolutos")
            st.markdown("Valores de casos absolutos por municipios do estado elecionado:")
            st.plotly_chart(mapa_absoluto)

        with col2:
            st.markdown("#### Mapa mensal de taxas")
            st.markdown("Valores das taxas de casos calculadas em relacão a população dos municipio do estado selecionado:")
            st.plotly_chart(mapa_taxa)

        #definindo multiselect de municipios baseado no estado selecionado em 'estado_box'
        lista_municipios = df_principal[df_principal.estado==estado_box].municipio.unique()
        municipios = st.multiselect('Selecione os estados de interesse e compare mensalmente os mesmos:',
                                  lista_municipios,
                                  lista_municipios[0])
        

        # definindo o grafico de linha para comparar os municipios
        grafico_linha_mensal_municipal = funcoes.grafico_mensal_municipios(df_principal,'Casos',estado_box,municipios)

        st.plotly_chart(grafico_linha_mensal_municipal)

        st.divider()
        #definindo multiselect de estados para grafico mensal
        estados = st.multiselect('Selecione os municípios de interesse e compare mensalmente os mesmos:',
                                  lista_estados,
                                  lista_estados[0])
        

        #definindo o grafico e plotando o mesmo
        grafico_linha_mensal = funcoes.grafico_mensal_estadual(df_principal,"Casos",estados)

        st.plotly_chart(grafico_linha_mensal)

        #Definindo selectbox com esdatos para criar grafico de linha dos municipios


if add_radio == "Óbitos":           # definindo as tab mensal


        st.title("Mapas de Óbitos Mensais Covid-19")
        st.write("Selecione um Estado:")
        
        estado_box = st.selectbox("mes",label_visibility ="collapsed",
                                    options=[x for x in lista_estados])
        
        ano_min,mes_min,dia_min = funcoes.retorna_date(df_principal.data.min())
        ano_max,mes_max,dia_max = funcoes.retorna_date(df_principal.data.max())
        
        d = st.date_input("Selecione uma data. (Os dados são mensais - AAAA/MM/DD)",
                            date(ano_min, mes_min, dia_min),
                            min_value = date(ano_min, mes_min, dia_min), 
                            max_value = date(ano_max,mes_max,dia_max)
                            )
        
        
        mapa_absoluto = funcoes.mapa_absoluto(df_principal,"Óbitos",estado_box,d.year,d.month)
        mapa_taxa = funcoes.mapa_taxa(df_principal,df_populacao,"Óbitos",estado_box,d.year,d.month)

        #criando duas colunas
        col1, col2 = st.columns(2,gap='large')
        # Define o conteúdo de cada coluna
        # cada coluna contem um mapa 
        with col1:
            st.markdown("#### Mapa óbitos mensais absolutos")
            st.markdown("Valores de óbitos absolutos por municipios do estado elecionado:")
            st.plotly_chart(mapa_absoluto)
        with col2:
            st.markdown("#### Mapa mensal de taxas")
            st.markdown("Valores das taxas de óbitos calculadas em relacão a população dos municipio do estado selecionado:")
            st.plotly_chart(mapa_taxa)


        #definindo multiselect de municipios baseado no estado selecionado em 'estado_box'
        lista_municipios = df_principal[df_principal.estado==estado_box].municipio.unique()
        municipios = st.multiselect('Selecione os estados de interesse e compare mensalmente os mesmos:',
                                  lista_municipios,
                                  lista_municipios[0])
        

        # definindo o grafico de linha para comparar os municipios
        grafico_linha_mensal_municipal = funcoes.grafico_mensal_municipios(df_principal,"Óbitos",estado_box,municipios)

        st.plotly_chart(grafico_linha_mensal_municipal)

        st.divider()

        #definindo multiselect de estados para grafico mensal
        estados = st.multiselect('Selecione os estados de interesse e compare mensalmente os mesmos:',
                                  lista_estados,
                                  lista_estados[0])
        
        #definindo o grafico e plotando o mesmo
        mapa_linha_mensal = funcoes.grafico_mensal_estadual(df_principal,"Óbitos",estados)

        st.plotly_chart(mapa_linha_mensal)

        
