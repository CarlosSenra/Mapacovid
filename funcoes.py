import pandas as pd
import plotly.express as px
import json


#formatando data
def retorna_date(data):
    data = str(data).split(' ')[0]
    lista = data.split('-')
    ano = int(lista[0])
    mes = int(lista[1])
    dia = int(lista[2])
    return ano,mes,dia

#configurações para o gráficos
main_config = {
    "hovermode": "x unified",
    "legend": {
                "title": {"text": None},
                "font" :{"color":"white"},
                "bgcolor": "rgba(0,0,0,0.5)"},
    "margin": {"l":0, "r":0, "t":25, "b":0}
}

def pegaarquivo(nome_arquivo):
    return 'datasets & JSON/{}'.format(nome_arquivo)
    #return 'C:/Users/rafin/Meu Drive/datasets & JSON/{}'.format(nome_arquivo)

def pegaarquivo_pasta(nome_arquivo):
    return 'datasets & JSON/{}'.format(nome_arquivo)
    #return 'C:/Users/rafin/Desktop/projetosautomatico/Projeto Mapa covid/datasets & JSON/{}'.format(nome_arquivo)


def dict_meses():
    meses_dict={1:'Janeiro',2:'Fevereiro',3:'Março',4:'Abril',5:'Maio',6:'Junho',
                7:'Julho',8:'Agosto',9:'Setembro',10:'Outubro',11:'Novembro',12:'Dezembro'}
    return meses_dict


def dict_codigos_estados(): #returna um dicionario com os codigos de cada estado, com o intuito de localizar os arquivos JSON para criação dos mapas
    codigos_estado_dict = {'RO':11,'AC':12,'AM':13,'RR':14,
                            'PA':15,'AP':16,'TO':17,'MA':21,
                            'PI':22,'CE':23,'RN':24,'PB':25,
                            'PE':26,'AL':27,'SE':28,'BA':29,
                            'MG':31,'ES':32,'RJ':33,'SP':35,
                            'PR':41,'SC':42,'RS':43,'MS':50,
                            'MT':51,'GO':52,'DF':53}
    return codigos_estado_dict


def dict_centroides_estados(): #retorna um dicionario com os centroides de cada estado para o posicionamento dos mapas
    dict_centroides ={'AC': {"lat":-8.77 , "lon":-70.55}, 'AL': {"lat":-9.71 , "lon":-35.73},
                      'AM': {"lat":-3.07 , "lon":-61.66}, 'AP': {"lat":1.41  , "lon":-51.77},
                      'BA': {"lat":-12.815652, "lon":-41.338091},
                      'CE': {"lat":-3.71 , "lon":-38.54},
                      'DF': {"lat":-15.83, "lon":-47.86},
                      'ES': {"lat":-19.19, "lon":-40.34},
                      'GO': {"lat":-16.64, "lon":-49.31},
                      'MA': {"lat": -2.55, "lon":-44.30},
                      'MT': {"lat":-12.64, "lon":-55.42},
                      'MS': {"lat":-20.51, "lon":-54.54},
                      'MG': {"lat":-18.10, "lon":-44.38},
                      'PA': {"lat": -5.53, "lon":-52.29},
                      'PB': {"lat": -7.06, "lon":-35.55},
                      'PR': {"lat":-24.89, "lon":-51.55},
                      'PE': {"lat": -8.28, "lon":-35.07},
                      'PI': {"lat": -8.28, "lon":-43.68},
                      'RJ': {"lat":-22.84, "lon":-43.15},
                      'RN': {"lat": -5.22, "lon":-36.52},
                      'RO': {"lat":-11.22, "lon":-62.80},
                      'RS': {"lat":-30.01, "lon":-51.22},
                      'RR': {"lat":  1.89, "lon":-61.22},
                      'SC': {"lat":-27.33, "lon":-49.44},
                      'SE': {"lat":-10.90, "lon":-37.07},
                      'SP': {"lat":-23.55, "lon":-46.64},
                      'TO': {"lat":-10.25, "lon":-48.25},
                    }
    return dict_centroides



# casos MENSAIS
def mapa_absoluto(dataframe,dados,estado,ano,mes): #função que retoruna uma figura do plotlyexpress (mapa com casos absolutos)
    
    #dataframe.data = pd.to_datetime(dataframe.data)
    df_estado = dataframe[dataframe.estado == estado]
    
    codigos_estado_dict_centroides = dict_centroides_estados()
    codigos_estado_dict = dict_codigos_estados()

    df_estado_mapa = df_estado.query('data.dt.month == {} and data.dt.year == {}'.format(mes,ano))
    
    #muni_json = json.load(open(pegaarquivo_pasta('id_geojs-{}-mun.json'.format(codigos_estado_dict[estado]))),encoding= 'utf-8')

    with open(pegaarquivo_pasta('id_geojs-{}-mun.json'.format(codigos_estado_dict[estado])), 'r') as f:
        muni_json = json.load(f)
    if dados == 'Casos':
        fig = px.choropleth_mapbox(df_estado_mapa,
                           locations = 'CD_MUN',
                           color = 'casosmensal',
                           geojson = muni_json,
                           color_continuous_scale="bupu",
                           #range_color=(0, 12),
                           mapbox_style="white-bg",
                           zoom=4, 
                           center = codigos_estado_dict_centroides[estado],
                           hover_data=["municipio"]
                           )
        fig.update_layout(margin={"r":0,"t":0,"l":2,"b":0},
                      width=370,
                      height=300,
                      coloraxis_colorbar=dict(title="Casos",
                                            thickness=10,
                                            len=0.5,
                                            xanchor="left",
                                            yanchor='middle',
                                            y=0.5,
                                            #x=0,
                                            ticks='outside',
                                            ticklen=5))
        
    if dados == "Óbitos":
        fig = px.choropleth_mapbox(df_estado_mapa,
                           locations = 'CD_MUN',
                           color = 'obitosmensal',
                           geojson = muni_json,
                           color_continuous_scale="bupu",
                           #range_color=(0, 12),
                           mapbox_style="white-bg",
                           zoom=4, 
                           center = codigos_estado_dict_centroides[estado],
                           hover_data=["municipio"]
                           )
        
    
        fig.update_layout(margin={"r":0,"t":0,"l":2,"b":0},
                        width=320,
                        height=300,
                        coloraxis_colorbar=dict(title="Casos",
                                            thickness=10,
                                            len=0.5,
                                            xanchor="left",
                                            yanchor='middle',
                                            y=0.5,
                                            #x=0,
                                            ticks='outside',
                                            ticklen=5),
                        legend_font_color='black', 
                        legend_font_size=14)

    
    

    return fig



def mapa_taxa(dataframe,pop,dados,estado,ano,mes): #função que retoruna uma figura do plotlyexpress (mapa com as taxas)
    
    # funcoes para calcular tacxa de obitos e casos
    casos_taxa = lambda row : ((row['casosmensal']/row['pupulacao'])*100)
    obitos_taxa = lambda row : ((row['obitosmensal']/row['pupulacao'])*100)
    ####
    
    populacao = pop

    #dataframe.data = pd.to_datetime(dataframe.data)
    df_estado = dataframe[dataframe.estado == estado]

    codigos_estado_dict_centroides = dict_centroides_estados()
    codigos_estado_dict = dict_codigos_estados()
    
    df_estado_mapa = df_estado.query('data.dt.month == {} and data.dt.year == {}'.format(mes,ano))
    df_estado_mapa = df_estado_mapa.merge(populacao, left_on='municipio',right_on='municipio',how='left')
    
    df_estado_mapa['casosmensaltaxa'] = df_estado_mapa.apply(casos_taxa,axis=1)
    df_estado_mapa['obitosmensaltaxa'] = df_estado_mapa.apply(obitos_taxa,axis=1)
    
    #muni_json = json.load(open(pegaarquivo_pasta('id_geojs-{}-mun.json'.format(codigos_estado_dict[estado])), encoding= 'utf-8'))

    with open(pegaarquivo_pasta('id_geojs-{}-mun.json'.format(codigos_estado_dict[estado])), 'r') as f:
        muni_json = json.load(f)
    
    if dados == 'Casos':
        fig = px.choropleth_mapbox(df_estado_mapa,
                           locations = 'CD_MUN',
                           color = 'casosmensaltaxa',
                           geojson = muni_json,
                           color_continuous_scale="purples",
                           #range_color=(0, 12),
                           mapbox_style= "white-bg",
                           zoom=4, 
                           center = codigos_estado_dict_centroides[estado],
                           #opacity=opacidade,
                           hover_data=["municipio"]
                           )
    if dados == "Óbitos":
        fig = px.choropleth_mapbox(df_estado_mapa,
                           locations = 'CD_MUN',
                           color = 'obitosmensaltaxa',
                           geojson = muni_json,
                           color_continuous_scale="purples",
                           #range_color=(0, 12),
                           #white-bg
                           mapbox_style="white-bg",
                           zoom=4, 
                           center = codigos_estado_dict_centroides[estado],
                           #opacity=opacidade,
                           hover_data=["municipio"]
                           )
      
    
    
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                      width=370,
                      height=300,
                      coloraxis_colorbar=dict(title="Taxa em %",
                                            thickness=10,
                                            len=0.5,
                                            yanchor='middle',
                                            y=0.5,
                                            ticks='outside',
                                            ticklen=5))

    return fig



#casos SEMANAIS

def mapa_absoluto_semana(dataframe,dados,estado,ano,mes): #função que retoruna uma figura do plotlyexpress (mapa com casos absolutos)
    
    #dataframe.data = pd.to_datetime(dataframe.data)
    df_estado = dataframe[dataframe.estado == estado]
    
    codigos_estado_dict_centroides = dict_centroides_estados()
    codigos_estado_dict = dict_codigos_estados()

    df_estado_mapa = df_estado.query('data.dt.month == {} and data.dt.year == {}'.format(mes,ano))
    
    #muni_json = json.load(open(pegaarquivo('id_geojs-{}-mun.json'.format(codigos_estado_dict[estado]))),encoding= 'utf-8')

    with open(pegaarquivo_pasta('id_geojs-{}-mun.json'.format(codigos_estado_dict[estado])), 'r') as f:
        muni_json = json.load(f)
    if dados == 'Casos':
        fig = px.choropleth_mapbox(df_estado_mapa,
                           locations = 'CD_MUN',
                           color = 'casossemanal',
                           geojson = muni_json,
                           color_continuous_scale="bupu",
                           #range_color=(0, 12),
                           mapbox_style="white-bg",
                           zoom=4, 
                           center = codigos_estado_dict_centroides[estado],
                           hover_data=["municipio"]
                           )
    if dados == "Óbitos":
        fig = px.choropleth_mapbox(df_estado_mapa,
                           locations = 'CD_MUN',
                           color = 'casossemanal',
                           geojson = muni_json,
                           color_continuous_scale="bupu",
                           #range_color=(0, 12),
                           mapbox_style="white-bg",
                           zoom=4, 
                           center = codigos_estado_dict_centroides[estado],
                           hover_data=["municipio"]
                           )
      
    
    
    fig.update_layout(margin={"r":0,"t":0,"l":2,"b":0},
                      width=400,
                      height=300,
                      coloraxis_colorbar=dict(title="Casos",
                                            thickness=10,
                                            len=0.5,
                                            xanchor="left",
                                            yanchor='middle',
                                            y=0.5,
                                            x=0,
                                            ticks='outside',
                                            ticklen=5))

    return fig

def mapa_taxa_semana(dataframe,pop,dados,estado,ano,mes): #função que retoruna uma figura do plotlyexpress (mapa com as taxas)
    
    # funcoes para calcular tacxa de obitos e casos
    casos_taxa = lambda row : ((row['casossemanal']/row['pupulacao'])*100)
    obitos_taxa = lambda row : ((row['obitossemanal']/row['pupulacao'])*100)
    ####
    
    populacao = pop

    #dataframe.data = pd.to_datetime(dataframe.data)
    df_estado = dataframe[dataframe.estado == estado]

    codigos_estado_dict_centroides = dict_centroides_estados()
    codigos_estado_dict = dict_codigos_estados()
    
    df_estado_mapa = df_estado.query('data.dt.month == {} and data.dt.year == {}'.format(mes,ano))
    df_estado_mapa = df_estado_mapa.merge(populacao, left_on='municipio',right_on='municipio',how='left')
    
    df_estado_mapa['casossemanaltaxa'] = df_estado_mapa.apply(casos_taxa,axis=1)
    df_estado_mapa['obitossemanaltaxa'] = df_estado_mapa.apply(obitos_taxa,axis=1)
    
    #muni_json = json.load(open(pegaarquivo('id_geojs-{}-mun.json'.format(codigos_estado_dict[estado])), encoding= 'utf-8'))

    with open(pegaarquivo_pasta('id_geojs-{}-mun.json'.format(codigos_estado_dict[estado])), 'r') as f:
        muni_json = json.load(f)
    
    if dados == 'Casos':
        fig = px.choropleth_mapbox(df_estado_mapa,
                           locations = 'CD_MUN',
                           color = 'casossemanaltaxa',
                           geojson = muni_json,
                           color_continuous_scale="purples",
                           #range_color=(0, 12),
                           mapbox_style= "white-bg",
                           zoom=4, 
                           center = codigos_estado_dict_centroides[estado],
                           #opacity=opacidade,
                           hover_data=["municipio"]
                           )
    if dados == "Óbitos":
        fig = px.choropleth_mapbox(df_estado_mapa,
                           locations = 'CD_MUN',
                           color = 'obitossemanaltaxa',
                           geojson = muni_json,
                           color_continuous_scale="purples",
                           #range_color=(0, 12),
                           #white-bg
                           mapbox_style="white-bg",
                           zoom=4, 
                           center = codigos_estado_dict_centroides[estado],
                           #opacity=opacidade,
                           hover_data=["municipio"]
                           )
      
    
    
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                      width=400,
                      height=300,
                      coloraxis_colorbar=dict(title="Taxa em %",
                                            thickness=10,
                                            len=0.5,
                                            yanchor='middle',
                                            y=0.5,
                                            ticks='outside',
                                            ticklen=5))

    return fig



def grafico_mensal_estadual(dataframe,dados,estado):
    
    dff = pd.DataFrame(dataframe)

    if dados == 'Casos':
        mensal = dff.groupby(by=['estado','data']).casosmensal.sum().unstack(level=0)
    else:
        mensal = dff.groupby(by=['estado','data']).obitosmensal.sum().unstack(level=0)

    fig = px.line(mensal, x=mensal.index, y=estado, labels={x:x for x in estado},title='teste',markers=True)

    fig.update_layout(main_config,
                      xaxis_title='Tempo',
                      yaxis_title= dados + ' mensais',
                      height = 350,
                      legend_title_text='Estados:',
                      title_text = f'{dados} mensais estaduais'
                      )
    fig.update_traces(mode="markers+lines",hovertemplate=None)

    return fig




def grafico_mensal_municipios(dataframe,dados,estado,municipio):

    dff = pd.DataFrame(dataframe)
    df_estado = dff[dff.estado == estado]

    if dados == 'Casos':
        mensal = df_estado.groupby(by=['municipio','data']).casosmensal.sum().unstack(level=0)
    else:
        mensal = df_estado.groupby(by=['municipio','data']).obitosmensal.sum().unstack(level=0)

    fig = px.line(mensal, x=mensal.index, y=municipio, labels={x:x for x in municipio},title='teste',markers=True)

    fig.update_layout(main_config,
                      xaxis_title=' ',
                      yaxis_title= dados + ' mensais',
                      height = 350,
                      legend_title_text='Estados:',
                      title_text = f'{dados} mensais municipais.'
                      )
    fig.update_traces(mode="markers+lines",hovertemplate=None)

    return fig




def grafico_semanal_estadual(dataframe,dados,estado):
    
    dff = pd.DataFrame(dataframe)

    if dados == 'Casos':
        semanal = dff.groupby(by=['estado','data']).casossemanal.sum().unstack(level=0)
    else:
        semanal = dff.groupby(by=['estado','data']).obitosmensalsemanal.sum().unstack(level=0)

    fig = px.line(semanal, x=semanal.index, y=estado, labels={x:x for x in estado},title='teste',markers=True)

    fig.update_layout(main_config,
                      xaxis_title='Tempo',
                      yaxis_title= dados + ' semanais',
                      height = 350,
                      legend_title_text='Estados:',
                      title_text = f'{dados} semanais estaduais'
                      )
    fig.update_traces(mode="markers+lines",hovertemplate=None)

    return fig


def grafico_semanal_municipios(dataframe,dados,estado,municipio):

    dff = pd.DataFrame(dataframe)
    df_estado = dff[dff.estado == estado]

    if dados == 'Casos':
        mensal = df_estado.groupby(by=['municipio','data']).casosmensal.sum().unstack(level=0)
    else:
        mensal = df_estado.groupby(by=['municipio','data']).obitosmensal.sum().unstack(level=0)

    fig = px.line(mensal, x=mensal.index, y=municipio, labels={x:x for x in municipio},title='teste',markers=True)

    fig.update_layout(main_config,
                      xaxis_title=' ',
                      yaxis_title= dados + ' mensais',
                      height = 350,
                      legend_title_text='Estados:',
                      title_text = f'{dados} mensais municipais.'
                      )
    fig.update_traces(mode="markers+lines",hovertemplate=None)

    return fig