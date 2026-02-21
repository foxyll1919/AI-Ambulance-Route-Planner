import streamlit as st
import osmnx as ox
import networkx as nx
import folium
import random

st.set_page_config(layout="wide")
st.title("🚑 Smart Emergency Ambulance Routing System")

# ---------------------------------------------------
# 1️⃣ Load Road Network (Using graph_from_point)
# ---------------------------------------------------
@st.cache_resource
def load_graph():
    center_point = (18.6298, 73.7997)  # Pimpri center
    G = ox.graph_from_point(
        center_point,
        dist=5000,
        network_type="drive"
    )
    return G

G = load_graph()

# ---------------------------------------------------
# 2️⃣ Define Multiple Hospitals
# ---------------------------------------------------
hospitals = {
    "Hospital 1": (18.6180, 73.8030),
    "Hospital 2": (18.6350, 73.7900),
    "Hospital 3": (18.6220, 73.8120)
}

# ---------------------------------------------------
# 3️⃣ Sidebar Inputs
# ---------------------------------------------------
st.sidebar.header("🚑 Ambulance Location")

start_lat = st.sidebar.number_input("Start Latitude", value=18.6298)
start_lon = st.sidebar.number_input("Start Longitude", value=73.7997)

traffic_level = st.sidebar.slider("Traffic Intensity", 0, 10, 3)

# ---------------------------------------------------
# 4️⃣ Apply Traffic Simulation
# ---------------------------------------------------
G_traffic = G.copy()

for u, v, data in G_traffic.edges(data=True):
    base_length = data.get("length", 1)
    traffic_delay = random.uniform(0, traffic_level)
    data["traffic_weight"] = base_length + traffic_delay * 10

# ---------------------------------------------------
# 5️⃣ Convert Start to Nearest Node
# ---------------------------------------------------
start_node = ox.distance.nearest_nodes(G_traffic, start_lon, start_lat)

# ---------------------------------------------------
# 6️⃣ Find Nearest Hospital Automatically
# ---------------------------------------------------
min_distance = float("inf")
best_route = None
selected_hospital_name = None
selected_hospital_coords = None

for name, (lat, lon) in hospitals.items():

    hospital_node = ox.distance.nearest_nodes(G_traffic, lon, lat)

    try:
        route = nx.astar_path(
            G_traffic,
            start_node,
            hospital_node,
            weight="traffic_weight"
        )

        distance = nx.path_weight(
            G_traffic,
            route,
            weight="traffic_weight"
        )

        if distance < min_distance:
            min_distance = distance
            best_route = route
            selected_hospital_name = name
            selected_hospital_coords = (lat, lon)

    except:
        continue

# ---------------------------------------------------
# 7️⃣ Display Results
# ---------------------------------------------------
if best_route:

    st.success(f"🏥 Nearest Hospital: {selected_hospital_name}")
    st.info(f"Estimated Travel Cost (Traffic Adjusted): {round(min_distance,2)} meters")

    # ---------------------------------------------------
    # 8️⃣ Create Folium Map (Manual Route Drawing)
    # ---------------------------------------------------

    # Extract route coordinates
    route_coords = [
        (G_traffic.nodes[node]['y'], G_traffic.nodes[node]['x'])
        for node in best_route
    ]

    # Create map centered at start
    route_map = folium.Map(location=[start_lat, start_lon], zoom_start=14)

    # Draw route line
    folium.PolyLine(route_coords, color="red", weight=5).add_to(route_map)

    # Add Start Marker
    folium.Marker(
        location=[start_lat, start_lon],
        popup="Ambulance Start",
        icon=folium.Icon(color="green")
    ).add_to(route_map)

    # Add Hospital Marker
    folium.Marker(
        location=selected_hospital_coords,
        popup=selected_hospital_name,
        icon=folium.Icon(color="blue")
    ).add_to(route_map)

    st.components.v1.html(route_map._repr_html_(), height=600)

else:
    st.error("No route found. Try adjusting the start location.")