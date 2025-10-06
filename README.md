# Flask Inventory Management App

A simple Flask web app to manage products, locations, and product movements using SQLite.

## Features
- Add, view, and edit products  
- Add, view, and edit locations  
- Add, view, and edit product movements  
- View report of product quantities in each location  

## Database Tables
Product(product_id, name)  
Location(location_id, name)  
ProductMovement(movement_id, timestamp, from_location, to_location, product_id, qty)  

## How to Run
1. Install Flask → `pip install flask`  
2. Run → `python app.py`  
3. Open → `http://127.0.0.1:5000`

## Example Data
Products: Laptop, Mouse, Keyboard, Monitor  
Locations: Warehouse A, Warehouse B, Showroom, Repair Center  
Movements: 10 Laptops to Warehouse A, 5 Laptops to Showroom, 2 Monitors to Warehouse B, 1 Laptop to Repair Center  

<img width="950" height="492" alt="image" src="https://github.com/user-attachments/assets/c33b0ad2-e3c0-4ad0-a9f6-6a93b2305a3e" />
<img width="953" height="558" alt="image" src="https://github.com/user-attachments/assets/b1a6795a-af5f-4ff7-8ba2-7d3da46cd44d" />
<img width="949" height="553" alt="image" src="https://github.com/user-attachments/assets/a541347e-0fe8-4483-b38b-38833f55a1a5" />
<img width="954" height="704" alt="image" src="https://github.com/user-attachments/assets/4da66af0-e8e8-4f2f-8ae5-b9af9fc4a9a4" />
<img width="452" height="926" alt="image" src="https://github.com/user-attachments/assets/ddea1741-6584-439a-bb2e-93972955c53f" />
