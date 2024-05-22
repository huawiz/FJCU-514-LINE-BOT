import folium
import json
import os

def renderMap():

    min_lon, max_lon = 121.4282, 121.4362
    min_lat, max_lat = 25.0322, 25.0408



    map = folium.Map(
        location=[(min_lat + max_lat) / 2, (min_lon + max_lon) / 2],
        zoom_start=17,
        max_bounds=True,
        min_lat=min_lat,
        max_lat=max_lat,
        min_lon=min_lon,
        max_lon=max_lon,
        min_zoom=16,max_zoom=19,
        attribution_control=False
    )

    
    geojson = os.path.join('data', 'map.geojson')
    with open(geojson, 'r', encoding='utf-8') as f:
        jsonCourseData = json.load(f)

    area = folium.GeoJson(
        jsonCourseData,
        style_function=lambda x: {
            'fillColor': '#000000',  # 填充黑色
            'color': '#00000000',    # 无边界颜色
            'weight': 0,             # 无边界
            'fillOpacity': 0.7       # 填充透明度
        }
    ).add_to(map)

    return map.get_root().render()