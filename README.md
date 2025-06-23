# 🌍 AI Travel Agent & Expense Planner

> **Plan smarter, travel better.**  
A modular, OOP-based system that helps users plan trips to any city in the world — with real-time data and complete budget estimation.

---

## ✈️ Purpose

The **AI Travel Agent & Expense Planner** is built to assist users in:

- Discovering top attractions, activities, and restaurants
- Getting real-time weather updates
- Estimating hotel costs based on stay duration and budget
- Calculating currency conversion to the user's native currency
- Generating a complete itinerary for multi-day trips
- Calculating total expenses including hotel, transport, and activities
- Summarizing the trip in a clean output format

---

## 🧱 Features Breakdown

Each feature is encapsulated using **Object-Oriented Programming** for modularity and maintainability.

### 1. 🏙️ Attractions & Activities
- Discover popular **attractions**, **restaurants**, and **local activities**
- Search for **transportation options** within the city

### 2. 🌦️ Weather Forecasting
- Get **current weather conditions**
- Fetch **multi-day weather forecasts** to plan activities accordingly

### 3. 🏨 Hotel Planning
- Search for hotels in a specified location
- Estimate **per-day cost** × **number of days**
- Filter by **budget range**

### 4. 💰 Total Cost Estimation
- Perform currency conversion using real-time **exchange rates**
- Calculate:
  - Hotel + Activities + Transport + Food
  - **Daily budget**
  - **Total trip cost**

### 5. 📅 Itinerary Generation
- Generate a day-by-day **plan** based on user preferences and available activities
- Output a **full itinerary** in readable format

### 6. 📋 Trip Summary
- Compile all sections into a **single travel summary** with highlights
- Useful for printing, exporting, or sharing

---

## 🛠️ Tech Stack

- **Language**: Python  
- **APIs Used**: OpenWeatherMap, Google Places, Currency Exchange API, etc.  
- **Design Pattern**: Object-Oriented Programming (OOP)  
- **Deployment**: Can be run locally or extended as a web service

---

## 🧩 Code Structure

📁 ai_travel_planner
│
├── 🧳 trip_planner.py         # Main driver class
├── 📍 location_module.py      # Handles attractions, activities, food
├── ☁️ weather_module.py       # Fetches current and forecast weather
├── 🏨 hotel_module.py         # Hotel search and cost estimation
├── 💸 currency_module.py      # Handles exchange rate + conversion
├── 🧮 cost_module.py          # Total cost calculator
├── 📅 itinerary_module.py     # Day-wise trip planner
├── 📝 summary_module.py       # Final summary builder
└── 📄 README.md               # This file

