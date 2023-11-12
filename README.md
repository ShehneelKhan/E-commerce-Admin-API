# E-commerce-Admin-API

**Technologies:**
1. FastAPI
2. MySQL

**Setup Instructions:**
1. Clone the repo
2. Create a database in MySQL
3. Create Virtual Environment:<br>
   **python -m venv venv**

4. Activate Virtual Environment:<br>
   **source venv/Scripts/activate**

5. Install dependencies using requirements.txt:<br>
   **pip install -r requirements.txt**
   
6. Edit the database.py, enter your username, password and database name:<br>
   **URL_DATABASE = 'mysql+pymysql://<username>:<password>@localhost:3306/<database_name>'**

7. Similarly, edit the insert_demo_data.py, enter your username, password and database name:<br>
   **URL_DATABASE = 'mysql+pymysql://<username>:<password>@localhost:3306/<database_name>'**

8. Run FastAPI:<br>
   **uvicorn main:app --reload<br>**
   (This will create tables in database)

9. Now, stop the server using **Ctrl+C**

10. Its time to insert the demo data into the database, so run insert_demo_data.py:<br>
    **python insert_demo_data.py**

Now, you can run the server again using **uvicorn main:app --reload** and start testing!

<br>
<br>

# Endpoints documentation:


### 1. **Create Sale Record**
- **Endpoint:** `/sales/create`
- **Method:** POST
- **Request Body:**
  - `product_id` (int)
  - `quantity_sold` (int)
  - `total_amount` (float)
  - `sale_date` (date)
- **Response Body:**
  - `product_id` (int)
  - `quantity_sold` (int)
  - `total_amount` (float)
  - `sale_date` (date)

---

### 2. **Get Revenue within Date Range**
- **Endpoint:** `/sales/revenue`
- **Method:** GET
- **Query Parameters:**
  - `start_date` (str)
  - `end_date` (str)
- **Response Body:**
  - `revenue` (float)

---

### 3. **Get Current Inventory**
- **Endpoint:** `/inventory`
- **Method:** GET
- **Query Parameter:**
  - `low_stock_threshold` (int, default=10, description="Low stock threshold")
- **Response Body:**
  - `inventory` (list)
  - `low_stock_alerts` (list) - if any products are below the low stock threshold

---

### 4. **Update Inventory**
- **Endpoint:** `/inventory/update`
- **Method:** PUT
- **Request Body:**
  - `product_id` (int)
  - `quantity` (int)
- **Response Body:**
  - `message` (str)

---

### 5. **Register Product**
- **Endpoint:** `/products/register`
- **Method:** POST
- **Request Body:**
  - `product_name` (str)
  - `price` (float)
- **Response Body:**
  - `product_id` (int)
  - `product_name` (str)
  - `price` (float)

---

### 6. **Get All Sales**
- **Endpoint:** `/sales`
- **Method:** GET
- **Response Body:** List of sale records

---

### 7. **Get Daily Sales**
- **Endpoint:** `/sales/daily`
- **Method:** GET
- **Response Body:** List of sale records for the current day

---

### 8. **Get Weekly Sales**
- **Endpoint:** `/sales/weekly`
- **Method:** GET
- **Response Body:** List of sale records for the current week

---

### 9. **Get Monthly Sales**
- **Endpoint:** `/sales/monthly`
- **Method:** GET
- **Response Body:** List of sale records for the current month

---

### 10. **Get Annual Sales**
- **Endpoint:** `/sales/annual`
- **Method:** GET
- **Response Body:** List of sale records for the current year

---

### 11. **Filter Sales**
- **Endpoint:** `/sales/filter`
- **Method:** GET
- **Query Parameters:**
  - `start_date` (optional)
  - `end_date` (optional)
  - `product_id` (optional)
  - `category` (optional)
  - `quantity_sold_min` (optional)
  - `quantity_sold_max` (optional)
  - `total_amount_min` (optional)
  - `total_amount_max` (optional)
- **Response Body:** List of filtered sale records

---

### 12. **Analyze Sales**
- **Endpoint:** `/sales/analysis`
- **Method:** GET
- **Query Parameters:**
  - (Same as "Filter Sales")
- **Response Body:**
  - `total_quantity_sold` (int)
  - `total_revenue` (float)

---

### 13. **Compare Sales**
- **Endpoint:** `/sales/compare`
- **Method:** GET
- **Query Parameters:**
  - `start_date_1` (str)
  - `end_date_1` (str)
  - `start_date_2` (str)
  - `end_date_2` (str)
- **Response Body:**
  - `revenue_comparison` (dict) with details for both date ranges

---

### 14. **Sales by Date Range**
- **Endpoint:** `/sales/bydate`
- **Method:** GET
- **Query Parameters:**
  - `start_date` (str)
  - `end_date` (str)
- **Response Body:** List of sale records within the specified date range

---

### 15. **Sales by Product**
- **Endpoint:** `/sales/byproduct`
- **Method:** GET
- **Query Parameters:**
  - `product_id` (int)
- **Response Body:** List of sale records for a specific product

---

### 16. **Sales by Category**
- **Endpoint:** `/sales/bycategory`
- **Method:** GET
- **Query Parameters:**
  - `category` (str)
- **Response Body:** List of sale records for a specific product category

---
<br>
<br>

# Database Documentation: 

## Product Table:

**Purpose:** Stores information about products.<br>

**Columns:** <br>
**product_id:** Primary key identifying each product uniquely.<br>
**product_name:** Name of the product.<br>
**price:** Price of the product.<br>
**inventory_id:** Foreign key referencing the Inventory table, indicating the associated inventory record.<br><br>

## Inventory Table:

**Purpose:** Keeps track of the quantity of each product in stock.<br>

**Columns:** <br>
**product_id:** Primary key, referencing the Product table, linking each inventory entry to a specific product.<br>
**quantity:** The quantity of the product in stock.<br><br>

## Sale Table:

**Purpose:** Records information about sales transactions.<br>

**Columns:** <br>
**sale_id:** Primary key uniquely identifying each sale.<br>
**product_id:** Foreign key referencing the Product table, indicating the product sold.<br>
**quantity_sold:** The quantity of the product sold.<br>
**total_amount:** The total amount of the sale.<br>
**sale_date:** The date when the sale occurred.<br><br>

## Relationships:

* The Product table has a one-to-one relationship with the Inventory table, meaning each product has a single corresponding inventory entry.<br><br>
* The Product table also has a one-to-many relationship with the Sale table, indicating that a product can be sold multiple times, and each sale is linked to a specific product.<br><br>
* The Inventory table has a one-to-one relationship with the Product table, establishing a link between a product and its inventory information.<br><br>
* The Sale table has a many-to-one relationship with the Product table, meaning multiple sales can be associated with a single product.
