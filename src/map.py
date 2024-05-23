import folium
import json
import os
from folium.plugins import Search

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

    
    map_geojson = os.path.join('data', 'map.geojson')
    with open(map_geojson, 'r', encoding='utf-8') as f:
        mapData = json.load(f)

    area = folium.GeoJson(
        mapData,
        style_function=lambda x: {
            'fillColor': '#000000',  # 填充黑色
            'color': '#00000000',    # 无边界颜色
            'weight': 0,             # 无边界
            'fillOpacity': 0.7       # 填充透明度
        }
    ).add_to(map)


    locate_geojson = os.path.join('data', 'location.geojson')
    with open(locate_geojson, 'r', encoding='utf-8') as f:
        locationData = json.load(f)
    def style_function(feature):
        markup = """
                <div style="font-size: 0.8em;">
                <div style="width: 10px;
                            height: 10px;
                            border: 1px solid black;
                            border-radius: 5px;
                            background-color: orange;">
                </div>
            </div>
        """
        return {"html": markup}
    # Add the GeoJSON layer with a tooltip
    fju_geo = folium.GeoJson(
        locationData,
            name="fju",
    tooltip=folium.GeoJsonTooltip(
        fields=["name"], aliases=["地點"], localize=True
    ),marker=folium.Marker(icon=folium.DivIcon()),style_function=style_function
    ).add_to(map)


    # Move the zoom control to the bottom right
    map_script_zoom_control = '<script>document.addEventListener("DOMContentLoaded", function() {\
        document.querySelector("div.leaflet-bottom.leaflet-right").insertBefore(\
            document.querySelector("div.leaflet-control-zoom"), document.querySelector("div.leaflet-control-attribution")\
        );\
    });</script>'
    map.get_root().html.add_child(folium.Element(map_script_zoom_control))


        
    search_box = '''
    <style>
        .form {
            position: relative;
        }
        .form .fa-search {
            position: absolute;
            top: 50%;
            transform: translateY(-50%);
            left: 20px;
            color: #9ca3af;
        }
        .form-input {
            height: 45px;
            text-indent: 33px;
            border-radius: 100px;
            width: 100%;
            font-size: 15px;
            
        }
        .form-input:focus {
            box-shadow: none;
        
        }
        .suggestions {
            max-height: 150px;
            overflow-y: auto;
            position: absolute;
            width: 100%;
            z-index: 1000;
            background-color: #fff;
            margin-top: 5px;
            display: none; /* 默认隐藏 */
            font-size: 15px;
        }
        @media (min-width: 576px) {
            .form-container {
                width: 300px;
            }
        }
        @media (max-width: 575.98px) {
            .form-container {
                width: 80%;
            }
        }
    </style>
    <div class="container" style="position: absolute; top: 10px; z-index: 9999; max-width: 400px;">
        <div class="row height d-flex justify-content-start align-items-center">
            <div class="col form-container">
                <div class="form">
                    <i class="fa fa-search"></i>
                    <input id="searchBox" type="text" class="form-control form-input" placeholder="查詢地點" autocomplete="off">
                    <ul id="suggestions" class="list-group suggestions"></ul>
                </div>
            </div>
        </div>
    </div>
    <script>
        // 假设您有一个名为 map 的地图对象，并且已经在其他地方初始化
        var geoJSONData = {{ geo_json_str }};
        // 从 GeoJSON 数据中提取地点名称
        var places = geoJSONData.features.map(function(feature) {
        return feature.properties.name;
    }).filter(function(name) {
        return name !== null && name.trim() !== '';
    });

    var currentIndex = -1; // 当前选中的建议索引

    document.getElementById('searchBox').addEventListener('input', function () {
        var query = this.value.trim();
        var suggestions = document.getElementById('suggestions');
        suggestions.innerHTML = '';
        currentIndex = -1; // 重置当前索引
        if (query) {
            var filteredPlaces = places.filter(function (place) {
                return place.includes(query);
            });
            filteredPlaces.forEach(function (place) {
                var li = document.createElement('li');
                li.textContent = place;
                li.className = 'list-group-item list-group-item-action';
                li.addEventListener('click', function () {
                    document.getElementById('searchBox').value = place;
                    suggestions.innerHTML = '';
                    suggestions.style.display = 'none';
                    moveToPlace(place);
                });
                suggestions.appendChild(li);
            });
            suggestions.style.display = 'block';
        } else {
            suggestions.style.display = 'none';
        }
    });

    document.getElementById('searchBox').addEventListener('keydown', function (event) {
        var suggestions = document.getElementById('suggestions');
        var items = suggestions.getElementsByTagName('li');
        if (event.key === 'Enter') {
            event.preventDefault();
            selectPlace();
        } else if (event.key === 'ArrowDown') {
            event.preventDefault();
            if (currentIndex < items.length - 1) {
                currentIndex++;
                highlightSuggestion(items, currentIndex);
            }
        } else if (event.key === 'ArrowUp') {
            event.preventDefault();
            if (currentIndex > 0) {
                currentIndex--;
                highlightSuggestion(items, currentIndex);
            }
        }
    });

    document.getElementById('searchBox').addEventListener('focusout', function () {
        selectPlace();
    });

    function selectPlace() {
        var suggestions = document.getElementById('suggestions');
        var items = suggestions.getElementsByTagName('li');
        if (currentIndex >= 0 && currentIndex < items.length) {
            var place = items[currentIndex].textContent;
            document.getElementById('searchBox').value = place;
            suggestions.innerHTML = '';
            suggestions.style.display = 'none';
            moveToPlace(place);
        } else {
            var query = document.getElementById('searchBox').value.trim();
            if (query) {
                var place = places.find(function (p) {
                    return p === query;
                });
                if (place) {
                    document.getElementById('searchBox').value = place;
                    suggestions.innerHTML = '';
                    suggestions.style.display = 'none';
                    moveToPlace(place);
                }
            }
        }
    }

    function highlightSuggestion(items, index) {
        for (var i = 0; i < items.length; i++) {
            if (i === index) {
                items[i].classList.add('active');
                items[i].scrollIntoView({ block: 'nearest' });
            } else {
                items[i].classList.remove('active');
            }
        }
    }

       function moveToPlace(place) {
        var selectedFeature = geoJSONData.features.find(function (feature) {
            return feature.properties.name === place;
        });
        
        if (selectedFeature) {
            var coordinates = selectedFeature.geometry.coordinates;
            var name = selectedFeature.properties.name;
            var alias = selectedFeature.properties.alias?selectedFeature.properties.alias:'Null';
            {{map}}.flyTo([coordinates[1], coordinates[0]], 19);
            L.popup([coordinates[1], coordinates[0]],{content:alias+" "+name}).openOn({{map}});
        }
    }

    
    
</script>
    '''

    # Replace the placeholders with the actual data
    search_box = search_box.replace('{{map}}', map.get_name())
    search_box = search_box.replace('{{ geo_json_str }}', json.dumps(fju_geo.data))

    map.get_root().html.add_child(folium.Element(search_box))

    return map.get_root().render()