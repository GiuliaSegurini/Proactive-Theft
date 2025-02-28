
#%%
#LOGICHE DI FILTRO TRIP PER ESCLUDERE:
#FERMI VEICOLO (SPEED MEDIA TRIP INFERIORE A 0.2KMH)
#POSIZIONI ERRATE PER GPS (SPEED MEDIA TRIP SUPERIORE A 200KMH PER DURATA NOTA)
new_dfmap=copy.deepcopy(new_dfmap_fl)
new_dfmap=new_dfmap[new_dfmap['mean_speed']>0.2]
new_dfmap=new_dfmap[new_dfmap['mspeed']<150]
new_dfmap.reset_index(drop=True,inplace=True)
#new_dfmap=new_dfmap.loc[1500:1750,:]


chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'

# Linux
# chrome_path = '/usr/bin/google-chrome %s'



#MAPPA SINGOLI TRIP per DEVICE soggetto a FURTO
num_max_mappe_device=100 #IMPORTANTE, NUMERO MASSIMO MAPPE DA GENERARE
colors=['deepskyblue','red']
lat_ct=new_dfmap['latitude'].quantile(0.5)
long_ct=new_dfmap['longitude'].quantile(0.5)
devices=new_dfmap['id_terminal'].unique()
for j in range(50,min(int(num_max_mappe_device),len(list(devices)))):
    m = folium.Map(location=[lat_ct,long_ct], zoom_start=8,tiles="OpenStreetMap")  
    for i in [0,1]:
        device=list(devices)[j]
        print(device)
        dfdevice=new_dfmap[new_dfmap['id_terminal']==device]
        mapbounds=[[dfdevice['latitude'].min(),dfdevice['longitude'].min()], [dfdevice['latitude'].max(),dfdevice['longitude'].max()]]
        m.fit_bounds(mapbounds)    
        dfdevice=dfdevice[dfdevice['furto']==i]
        dfdevice.reset_index(drop=True,inplace=True)
#        dfdevice=dfdevice.loc[range(0,len(dfdevice),redux),:]
        points = []   
        for n in range(min(int(1e6),len(dfdevice))):
            points.append([dfdevice.iloc[n]['latitude'],dfdevice.iloc[n]['longitude']])
        if len(points)>1:
            folium.PolyLine(points, color=colors[i],
                weight=5,opacity=0.8).add_to(m)
    map_name=f'{device}_map.html'
    m.save(map_name)
#    webbrowser.open(r'file:///C:/Users/a.sauro/'+map_name)   
    webbrowser.get(chrome_path).open(r'file:///C:/Users/a.sauro/Desktop/MappeFurto28Feb/'+map_name)


#%%
from folium import plugins
from folium.plugins import HeatMap
heatdf=copy.deepcopy(new_dfmap)
heatdf=heatdf[heatdf['furto']==1]
heatdf.sort_values(by='timestamp',ascending=True,inplace=True)
heatdf.drop_duplicates(subset=['id_terminal'], keep='first',inplace=True)
heatdf.reset_index(drop=True,inplace=True)

heat_data=[]
for i in range(len(heatdf)):
    heat_data += [[heatdf.loc[i,'latitude'],heatdf.loc[i,'longitude']]]
m = folium.Map(location=[heatdf['latitude'].quantile(0.5), heatdf['latitude'].quantile(0.5)], zoom_start = 13)
# Plot it on the map
HeatMap(heat_data).add_to(m)

map_name='heatmap_furti.html'
m.save(map_name)
#    webbrowser.open(r'file:///C:/Users/a.sauro/'+map_name)   
webbrowser.get(chrome_path).open(r'file:///C:/Users/a.sauro/Desktop/MappeFurto28Feb/'+map_name)

heatdf=copy.deepcopy(new_dfmap)
heatdf=heatdf[heatdf['furto']==0]
heatdf.sort_values(by='timestamp',ascending=True,inplace=True)
heatdf.drop_duplicates(subset=['id_terminal'], keep='first',inplace=True)
heatdf.reset_index(drop=True,inplace=True)

heat_data=[]
for i in range(len(heatdf)):
    heat_data += [[heatdf.loc[i,'latitude'],heatdf.loc[i,'longitude']]]
m = folium.Map(location=[heatdf['latitude'].quantile(0.5), heatdf['latitude'].quantile(0.5)], zoom_start = 13)
# Plot it on the map
HeatMap(heat_data).add_to(m)

map_name='heatmap_no_furti.html'
m.save(map_name)
#    webbrowser.open(r'file:///C:/Users/a.sauro/'+map_name)   
webbrowser.get(chrome_path).open(r'file:///C:/Users/a.sauro/Desktop/MappeFurto28Feb/'+map_name)

heatdf=copy.deepcopy(new_dfmap)
heatdf=heatdf[heatdf['furto']>=0]
heatdf.sort_values(by='timestamp',ascending=True,inplace=True)
heatdf.drop_duplicates(subset=['id_terminal'], keep='first',inplace=True)
heatdf.reset_index(drop=True,inplace=True)

heat_data=[]
for i in range(len(heatdf)):
    heat_data += [[heatdf.loc[i,'latitude'],heatdf.loc[i,'longitude']]]
m = folium.Map(location=[heatdf['latitude'].quantile(0.5), heatdf['latitude'].quantile(0.5)], zoom_start = 13)
# Plot it on the map
HeatMap(heat_data).add_to(m)

map_name='heatmap_all.html'
m.save(map_name)
#    webbrowser.open(r'file:///C:/Users/a.sauro/'+map_name)   
webbrowser.get(chrome_path).open(r'file:///C:/Users/a.sauro/Desktop/MappeFurto28Feb/'+map_name)