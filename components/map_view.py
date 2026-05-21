import folium
from streamlit_folium import st_folium

def render_map(reports_list):
    """
    Renders a Folium map with markers for each disaster report.
    """
    # 1. Center Map (Default to Hyderabad or the average of reports)
    start_lat = 17.3850
    start_lon = 78.4867
    
    # If we have reports, center map on the latest one
    if reports_list:
        start_lat = reports_list[-1]['lat']
        start_lon = reports_list[-1]['lon']

    m = folium.Map(location=[start_lat, start_lon], zoom_start=12, tiles="Cartodb Positron")

    # 2. Add Markers
    for report in reports_list:
        # Create HTML for the popup (The box that appears when you click)
        popup_html = f"""
        <div style="width:200px">
            <h4>{report['type']} Alert</h4>
            <b>Severity:</b> {report['severity']}/10<br>
            <b>Time:</b> {report['timestamp']}<br>
            <hr>
            {report['description']}
        </div>
        """
        
        # Add the marker
        folium.Marker(
            location=[report['lat'], report['lon']],
            popup=folium.Popup(popup_html, max_width=250),
            tooltip=f"{report['type']} - Click for info",
            icon=folium.Icon(color=report['color'], icon=report['icon'], prefix='fa')
        ).add_to(m)

    # 3. Return the map to Streamlit
    return st_folium(m, width="100%", height=500, returned_objects=[])