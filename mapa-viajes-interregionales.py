from flask import Flask , render_template
from flask_cors import CORS
from flask import jsonify, request, send_file
import flask
from sqlalchemy import create_engine, select, MetaData, Table, func, and_
import pandas as pd
import folium
import geopandas

app = Flask(__name__)

@app.route("/")
def hello():
    engine = create_engine('sqlite:///resources/base_datos_def.sqlite')
    metadata=MetaData()
    tabla=Table('tabla_2', metadata, autoload=True, autoload_with=engine)
    stmt=select([func.min(tabla.columns.fecha),func.max(tabla.columns.fecha)])
    proxy_result=engine.execute(stmt)
    result=proxy_result.fetchall()
    fecha_min=result[0][0]
    fecha_max=result[0][1]

    return render_template('index6.html',fecha_min=fecha_min, fecha_max=fecha_max)

@app.route('/background_process')

@app.route('/get_map', methods=['GET', 'POST'])
def get_map():
    fecha_inicio=request.args.get('fecha_inicio', 0, type=str)
    fecha_termino=request.args.get('fecha_termino', 0, type=str)
    hora_inicio=request.args.get('hora_inicio', 0, type=str)
    hora_termino=request.args.get('hora_termino', 0, type=str)
    #print fecha_inicio
    #print fecha_termino
    tabla_coordenadas=pd.DataFrame({'region':[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],
                                'centroide':[(-20.20846680432151, -69.39593397795421),
                                             (-23.5361502255913, -69.12097341010443),
                                             (-27.39491653747887, -69.90995854592933),
                                             (-30.61837270282146, -70.86087968470927),
                                             (-32.78354511283093, -70.95907896685472),
                                             (-34.43549056629101, -71.04654249909848),
                                             (-35.62131360941913, -71.4453022265221),
                                             (-37.20012490247623, -72.24726974370338),
                                             (-38.64932008964095, -72.27467621238263),
                                             (-42.04162042097533, -72.89532012893434),
                                             (-46.43042076492267, -73.24848728696547),
                                             (-52.44780426654368, -71.89875186302086),
                                             (-33.60459641123774, -70.62691900103086),
                                             (-40.00529752727184, -72.57121406710303),
                                             (-18.4873038977637, -69.62391233908097)]})
    engine = create_engine('sqlite:///resources/base_datos_def.sqlite')
    metadata=MetaData()
    tabla=Table('tabla_2', metadata, autoload=True, autoload_with=engine)

    stmt=select([tabla])
    stmt=select([tabla.columns.region_origen,tabla.columns.region_destino,func.sum(tabla.columns.cantidad)])
    stmt=stmt.where(and_(tabla.columns.fecha + tabla.columns.hora >= fecha_inicio + hora_inicio,
                         tabla.columns.fecha + tabla.columns.hora < fecha_termino + hora_termino))
    stmt=stmt.group_by(tabla.columns.region_origen,tabla.columns.region_destino)
    proxy_result=engine.execute(stmt)
    result=proxy_result.fetchall()
    result=pd.DataFrame(result,columns=['origen','destino','cantidad'])
    #MAPA
    OHiggins=folium.FeatureGroup(name="Libertador_Bernardo O'Higgins", overlay=True, control=True)
    LosLagos=folium.FeatureGroup(name="Los Lagos", overlay=True, control=True)
    Atacama=folium.FeatureGroup(name="Atacama", overlay=True, control=True)
    Metropolitana=folium.FeatureGroup(name="Metropolitana", overlay=True, control=True)
    Araucania=folium.FeatureGroup(name="Araucania", overlay=True, control=True)
    Maule=folium.FeatureGroup(name="Maule", overlay=True, control=True)
    Valparaiso=folium.FeatureGroup(name="Valparaiso", overlay=True, control=True)
    Tarapaca=folium.FeatureGroup(name="Tarapaca", overlay=True, control=True)
    LosRios=folium.FeatureGroup(name="Los Rios", overlay=True, control=True)
    BioBio=folium.FeatureGroup(name="Bio Bio", overlay=True, control=True)
    Aysen=folium.FeatureGroup(name="Aysen", overlay=True, control=True)
    Antofagasta=folium.FeatureGroup(name="Antofagasta", overlay=True, control=True)
    AricaParinacota=folium.FeatureGroup(name="Arica y Parinacota", overlay=True, control=True)
    Coquimbo=folium.FeatureGroup(name="Coquimbo", overlay=True, control=True)
    Magallanes=folium.FeatureGroup(name="Magallanes y Antartica", overlay=True, control=True)

    mapa=folium.Map(location=[-33.4372, -70.6506],tiles='Stamen Toner')
    i=0
    for e in range(len(tabla_coordenadas.region)):
        if e!=i:
            if len(result[(result.origen==tabla_coordenadas.region[i]) & (result.destino==tabla_coordenadas.region[e])])>0:
                folium.vector_layers.PolyLine([tabla_coordenadas.centroide[i],tabla_coordenadas.centroide[e]],popup=(str('origen-destino:'+str(tabla_coordenadas.region[i])+'-'+str(tabla_coordenadas.region[e])+', cantidad de viajes:'+str(result[(result.origen==tabla_coordenadas.region[i]) & (result.destino==tabla_coordenadas.region[e])].cantidad.values[0]))),weight=5,color='red').add_to(Tarapaca)
    i=1
    for e in range(len(tabla_coordenadas.region)):
        if e!=i:
            if len(result[(result.origen==tabla_coordenadas.region[i]) & (result.destino==tabla_coordenadas.region[e])])>0:
                folium.vector_layers.PolyLine([tabla_coordenadas.centroide[i],tabla_coordenadas.centroide[e]],popup=(str('origen-destino:'+str(tabla_coordenadas.region[i])+'-'+str(tabla_coordenadas.region[e])+', cantidad de viajes:'+str(result[(result.origen==tabla_coordenadas.region[i]) & (result.destino==tabla_coordenadas.region[e])].cantidad.values[0]))),weight=5,color='#FFA500').add_to(Antofagasta)
    i=2
    for e in range(len(tabla_coordenadas.region)):
        if e!=i:
            if len(result[(result.origen==tabla_coordenadas.region[i]) & (result.destino==tabla_coordenadas.region[e])])>0:                 
                folium.vector_layers.PolyLine([tabla_coordenadas.centroide[i],tabla_coordenadas.centroide[e]],popup=(str('origen-destino:'+str(tabla_coordenadas.region[i])+'-'+str(tabla_coordenadas.region[e])+', cantidad de viajes:'+str(result[(result.origen==tabla_coordenadas.region[i]) & (result.destino==tabla_coordenadas.region[e])].cantidad.values[0]))),weight=5,color='#006400').add_to(Atacama)
    i=3
    for e in range(len(tabla_coordenadas.region)):
        if e!=i:
            if len(result[(result.origen==tabla_coordenadas.region[i]) & (result.destino==tabla_coordenadas.region[e])])>0:
                folium.vector_layers.PolyLine([tabla_coordenadas.centroide[i],tabla_coordenadas.centroide[e]],popup=(str('origen-destino:'+str(tabla_coordenadas.region[i])+'-'+str(tabla_coordenadas.region[e])+', cantidad de viajes:'+str(result[(result.origen==tabla_coordenadas.region[i]) & (result.destino==tabla_coordenadas.region[e])].cantidad.values[0]))),weight=5,color='black').add_to(Coquimbo)
    i=4
    for e in range(len(tabla_coordenadas.region)):
        if e!=i:
            if len(result[(result.origen==tabla_coordenadas.region[i]) & (result.destino==tabla_coordenadas.region[e])])>0:
                folium.vector_layers.PolyLine([tabla_coordenadas.centroide[i],tabla_coordenadas.centroide[e]],popup=(str('origen-destino:'+str(tabla_coordenadas.region[i])+'-'+str(tabla_coordenadas.region[e])+', cantidad de viajes:'+str(result[(result.origen==tabla_coordenadas.region[i]) & (result.destino==tabla_coordenadas.region[e])].cantidad.values[0]))),weight=5,color='#7CFC00').add_to(Valparaiso)
    i=5
    for e in range(len(tabla_coordenadas.region)):
        if e!=i:
            if len(result[(result.origen==tabla_coordenadas.region[i]) & (result.destino==tabla_coordenadas.region[e])])>0:
                folium.vector_layers.PolyLine([tabla_coordenadas.centroide[i],tabla_coordenadas.centroide[e]],popup=(str('origen-destino:'+str(tabla_coordenadas.region[i])+'-'+str(tabla_coordenadas.region[e])+', cantidad de viajes:'+str(result[(result.origen==tabla_coordenadas.region[i]) & (result.destino==tabla_coordenadas.region[e])].cantidad.values[0]))),weight=5,color='#D3D3D3').add_to(OHiggins)
    i=6
    for e in range(len(tabla_coordenadas.region)):
        if e!=i:
            if len(result[(result.origen==tabla_coordenadas.region[i]) & (result.destino==tabla_coordenadas.region[e])])>0:
                folium.vector_layers.PolyLine([tabla_coordenadas.centroide[i],tabla_coordenadas.centroide[e]],popup=(str('origen-destino:'+str(tabla_coordenadas.region[i])+'-'+str(tabla_coordenadas.region[e])+', cantidad de viajes:'+str(result[(result.origen==tabla_coordenadas.region[i]) & (result.destino==tabla_coordenadas.region[e])].cantidad.values[0]))),weight=5,color='#00CED1').add_to(Maule)
    i=7
    for e in range(len(tabla_coordenadas.region)):
        if e!=i:
            if len(result[(result.origen==tabla_coordenadas.region[i]) & (result.destino==tabla_coordenadas.region[e])])>0:
                folium.vector_layers.PolyLine([tabla_coordenadas.centroide[i],tabla_coordenadas.centroide[e]],popup=(str('origen-destino:'+str(tabla_coordenadas.region[i])+'-'+str(tabla_coordenadas.region[e])+', cantidad de viajes:'+str(result[(result.origen==tabla_coordenadas.region[i]) & (result.destino==tabla_coordenadas.region[e])].cantidad.values[0]))),weight=5,color='#FFFF00').add_to(BioBio)
    i=8
    for e in range(len(tabla_coordenadas.region)):
        if e!=i:
            if len(result[(result.origen==tabla_coordenadas.region[i]) & (result.destino==tabla_coordenadas.region[e])])>0:
                folium.vector_layers.PolyLine([tabla_coordenadas.centroide[i],tabla_coordenadas.centroide[e]],popup=(str('origen-destino:'+str(tabla_coordenadas.region[i])+'-'+str(tabla_coordenadas.region[e])+', cantidad de viajes:'+str(result[(result.origen==tabla_coordenadas.region[i]) & (result.destino==tabla_coordenadas.region[e])].cantidad.values[0]))),weight=5,color='#00BFFF').add_to(Araucania)
    i=9
    for e in range(len(tabla_coordenadas.region)):
        if e!=i:
            if len(result[(result.origen==tabla_coordenadas.region[i]) & (result.destino==tabla_coordenadas.region[e])])>0:
                folium.vector_layers.PolyLine([tabla_coordenadas.centroide[i],tabla_coordenadas.centroide[e]],popup=(str('origen-destino:'+str(tabla_coordenadas.region[i])+'-'+str(tabla_coordenadas.region[e])+', cantidad de viajes:'+str(result[(result.origen==tabla_coordenadas.region[i]) & (result.destino==tabla_coordenadas.region[e])].cantidad.values[0]))),weight=5,color='#000080').add_to(LosLagos)
    i=10
    for e in range(len(tabla_coordenadas.region)):
        if e!=i:
            if len(result[(result.origen==tabla_coordenadas.region[i]) & (result.destino==tabla_coordenadas.region[e])])>0:
                folium.vector_layers.PolyLine([tabla_coordenadas.centroide[i],tabla_coordenadas.centroide[e]],popup=(str('origen-destino:'+str(tabla_coordenadas.region[i])+'-'+str(tabla_coordenadas.region[e])+', cantidad de viajes:'+str(result[(result.origen==tabla_coordenadas.region[i]) & (result.destino==tabla_coordenadas.region[e])].cantidad.values[0]))),weight=5,color='#6A5ACD').add_to(Aysen)
    i=11
    for e in range(len(tabla_coordenadas.region)):
        if e!=i:
            if len(result[(result.origen==tabla_coordenadas.region[i]) & (result.destino==tabla_coordenadas.region[e])])>0:
                folium.vector_layers.PolyLine([tabla_coordenadas.centroide[i],tabla_coordenadas.centroide[e]],popup=(str('origen-destino:'+str(tabla_coordenadas.region[i])+'-'+str(tabla_coordenadas.region[e])+', cantidad de viajes:'+str(result[(result.origen==tabla_coordenadas.region[i]) & (result.destino==tabla_coordenadas.region[e])].cantidad.values[0]))),weight=5,color='#FF00FF').add_to(Magallanes)
    i=12
    for e in range(len(tabla_coordenadas.region)):
        if e!=i:
            if len(result[(result.origen==tabla_coordenadas.region[i]) & (result.destino==tabla_coordenadas.region[e])])>0:
                folium.vector_layers.PolyLine([tabla_coordenadas.centroide[i],tabla_coordenadas.centroide[e]],popup=(str('origen-destino:'+str(tabla_coordenadas.region[i])+'-'+str(tabla_coordenadas.region[e])+', cantidad de viajes:'+str(result[(result.origen==tabla_coordenadas.region[i]) & (result.destino==tabla_coordenadas.region[e])].cantidad.values[0]))),weight=5,color='#2F4F4F').add_to(Metropolitana)
    i=13
    for e in range(len(tabla_coordenadas.region)):
        if e!=i:
            if len(result[(result.origen==tabla_coordenadas.region[i]) & (result.destino==tabla_coordenadas.region[e])])>0:
                folium.vector_layers.PolyLine([tabla_coordenadas.centroide[i],tabla_coordenadas.centroide[e]],popup=(str('origen-destino:'+str(tabla_coordenadas.region[i])+'-'+str(tabla_coordenadas.region[e])+', cantidad de viajes:'+str(result[(result.origen==tabla_coordenadas.region[i]) & (result.destino==tabla_coordenadas.region[e])].cantidad.values[0]))),weight=5,color='#DAA520').add_to(LosRios)
    i=14
    for e in range(len(tabla_coordenadas.region)):
        if e!=i:
            if len(result[(result.origen==tabla_coordenadas.region[i]) & (result.destino==tabla_coordenadas.region[e])])>0:
                folium.vector_layers.PolyLine([tabla_coordenadas.centroide[i],tabla_coordenadas.centroide[e]],popup=(str('origen-destino:'+str(tabla_coordenadas.region[i])+'-'+str(tabla_coordenadas.region[e])+', cantidad de viajes:'+str(result[(result.origen==tabla_coordenadas.region[i]) & (result.destino==tabla_coordenadas.region[e])].cantidad.values[0]))),weight=5,color='#4B0082').add_to(AricaParinacota)

    regiones_shp_sin_modificar=geopandas.read_file('resources/Capas_shp/regiones_simplificada.shp')

    folium.GeoJson(
        regiones_shp_sin_modificar.geometry[regiones_shp_sin_modificar.region==1].values[0],
        style_function=lambda feature: {
            'fillColor': 'red',
            'color' : 'red',
            'weight' : 1,
            'fillOpacity' : 0.5,
            }
        ).add_to(Tarapaca)

    folium.GeoJson(
        regiones_shp_sin_modificar.geometry[regiones_shp_sin_modificar.region==2].values[0],
        style_function=lambda feature: {
            'fillColor': '#FFA500',
            'color' : '#FFA500',
            'weight' : 1,
            'fillOpacity' : 0.5,
            }
        ).add_to(Antofagasta)

    folium.GeoJson(
        regiones_shp_sin_modificar.geometry[regiones_shp_sin_modificar.region==3].values[0],
        style_function=lambda feature: {
            'fillColor': '#006400',
            'color' : '#006400',
            'weight' : 1,
            'fillOpacity' : 0.5,
            }
        ).add_to(Atacama)

    folium.GeoJson(
        regiones_shp_sin_modificar.geometry[regiones_shp_sin_modificar.region==4].values[0],
        style_function=lambda feature: {
            'fillColor': 'black',
            'color' : 'black',
            'weight' : 1,
            'fillOpacity' : 0.5,
            }
        ).add_to(Coquimbo)

    folium.GeoJson(
        regiones_shp_sin_modificar.geometry[regiones_shp_sin_modificar.region==5].values[0],
        style_function=lambda feature: {
            'fillColor': '#7CFC00',
            'color' : '#7CFC00',
            'weight' : 1,
            'fillOpacity' : 0.5,
            }
        ).add_to(Valparaiso)

    folium.GeoJson(
        regiones_shp_sin_modificar.geometry[regiones_shp_sin_modificar.region==6].values[0],
        style_function=lambda feature: {
            'fillColor': '#D3D3D3',
            'color' : '#D3D3D3',
            'weight' : 1,
            'fillOpacity' : 0.5,
            }
        ).add_to(OHiggins)

    folium.GeoJson(
        regiones_shp_sin_modificar.geometry[regiones_shp_sin_modificar.region==7].values[0],
        style_function=lambda feature: {
            'fillColor': '#00CED1',
            'color' : '#00CED1',
            'weight' : 1,
            'fillOpacity' : 0.5,
            }
        ).add_to(Maule)

    folium.GeoJson(
        regiones_shp_sin_modificar.geometry[regiones_shp_sin_modificar.region==8].values[0],
        style_function=lambda feature: {
            'fillColor': '#FFFF00',
            'color' : '#FFFF00',
            'weight' : 1,
            'fillOpacity' : 0.5,
            }
        ).add_to(BioBio)

    folium.GeoJson(
        regiones_shp_sin_modificar.geometry[regiones_shp_sin_modificar.region==9].values[0],
        style_function=lambda feature: {
            'fillColor': '#00BFFF',
            'color' : '#00BFFF',
            'weight' : 1,
            'fillOpacity' : 0.5,
            }
        ).add_to(Araucania)   
      
    folium.GeoJson(
        regiones_shp_sin_modificar.geometry[regiones_shp_sin_modificar.region==10].values[0],
        style_function=lambda feature: {
            'fillColor': '#000080',
            'color' : '#000080',
            'weight' : 1,
            'fillOpacity' : 0.5,
            }
        ).add_to(LosLagos)   

    folium.GeoJson(
        regiones_shp_sin_modificar.geometry[regiones_shp_sin_modificar.region==11].values[0],
        style_function=lambda feature: {
            'fillColor':'#6A5ACD',
            'color' : '#6A5ACD',
            'weight' : 1,
            'fillOpacity' : 0.5,
            }
        ).add_to(Aysen)   

    folium.GeoJson(
        regiones_shp_sin_modificar.geometry[regiones_shp_sin_modificar.region==12].values[0],
        style_function=lambda feature: {
            'fillColor': '#FF00FF',
            'color' : '#FF00FF',
            'weight' : 1,
            'fillOpacity' : 0.5,
            }
        ).add_to(Magallanes)   

    folium.GeoJson(
        regiones_shp_sin_modificar.geometry[regiones_shp_sin_modificar.region==13].values[0],
        style_function=lambda feature: {
            'fillColor': '#2F4F4F',
            'color' : '#2F4F4F',
            'weight' : 1,
            'fillOpacity' : 0.5,
            }
        ).add_to(Metropolitana)   

    folium.GeoJson(
        regiones_shp_sin_modificar.geometry[regiones_shp_sin_modificar.region==14].values[0],
        style_function=lambda feature: {
            'fillColor': '#DAA520',
            'color' : '#DAA520',
            'weight' : 1,
            'fillOpacity' : 0.5,
            }
        ).add_to(LosRios)   

    folium.GeoJson(
        regiones_shp_sin_modificar.geometry[regiones_shp_sin_modificar.region==15].values[0],
        style_function=lambda feature: {
            'fillColor': '#800000',
            'color' : '#800000',
            'weight' : 1,
            'fillOpacity' : 0.5,
            }
        ).add_to(AricaParinacota)   

    OHiggins.add_to(mapa)
    LosLagos.add_to(mapa)
    Atacama.add_to(mapa)
    Metropolitana.add_to(mapa)
    Araucania.add_to(mapa)
    Maule.add_to(mapa)
    Valparaiso.add_to(mapa)
    Tarapaca.add_to(mapa)
    LosRios.add_to(mapa)
    BioBio.add_to(mapa)
    Aysen.add_to(mapa)
    Antofagasta.add_to(mapa)
    AricaParinacota.add_to(mapa)
    Coquimbo.add_to(mapa)
    Magallanes.add_to(mapa)
    folium.LayerControl().add_to(mapa)

    return mapa.get_root().render()

@app.route('/show_map')
def show_map():
    mapa=folium.Map(location=[-33.4372, -70.6506],tiles='Stamen Toner')
    return mapa.get_root().render()


if __name__ == "__main__":
    app.run()

