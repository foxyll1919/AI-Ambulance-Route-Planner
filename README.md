# 🚑 Smart Emergency Ambulance Routing System

An AI-based smart city project that finds the fastest route to the nearest hospital using:

- 🧠 A* Search Algorithm
- 🗺 Real OpenStreetMap road network
- 🚦 Traffic simulation
- 🌐 Streamlit web application

---

## 📌 Project Overview

This system models a smart emergency response solution where:

1. The ambulance start location is provided.
2. Multiple hospitals are evaluated.
3. Traffic-adjusted path cost is calculated.
4. A* algorithm selects the fastest route.
5. The optimal route is displayed on a real interactive map.

---

## ⚙️ Tech Stack

- Python
- Streamlit
- OSMnx
- NetworkX
- Folium
- Scikit-learn

---

## 🚀 Features

✔ Real road network (Pimpri, Maharashtra)  
✔ Dynamic traffic intensity control  
✔ Automatic nearest hospital selection  
✔ A* pathfinding algorithm  
✔ Interactive map visualization  
✔ Clean web interface  

---

## 🧠 Algorithm Used

The routing uses the A* Search Algorithm:

f(n) = g(n) + h(n)

Where:
- g(n) = actual travel cost (distance + traffic weight)
- h(n) = heuristic estimate to hospital
- f(n) = total estimated cost

This ensures optimal and efficient emergency routing.

---

## 🖥 How To Run Locally

1. Clone the repository

git clone https://github.com/YOUR_USERNAME/AI-Ambulance-Route-Planner.git

2. Navigate into project folder

cd AI-Ambulance-Route-Planner

3. Install dependencies

pip install -r requirements.txt

4. Run the Streamlit app

streamlit run smart_ambulance_app.py

---

## 📷 Demo

(Add screenshot here later)

---

## 📜 License

MIT License
