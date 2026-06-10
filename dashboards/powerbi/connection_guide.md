# Power BI Connection Guide & DAX Specifications
**Pharmacy Sales & Inventory Analytics System**

This guide provides step-by-step instructions on connecting Power BI to the SQLite database (or processed CSVs), establishing data relationships, and implementing required DAX measures for the 4-page dashboard.

---

## 1. Data Connection

### Option A: Connecting to SQLite via ODBC (Recommended)
1. **Install SQLite ODBC Driver**: Download and install the SQLite ODBC Driver (from [ch-werner.de](http://www.ch-werner.de/sqliteodbc/)).
2. **Configure DSN**:
   - Open **ODBC Data Source Administrator** (64-bit on Windows).
   - Go to **System DSN** and click **Add**.
   - Select **SQLite3 ODBC Driver** and click **Finish**.
   - Set **Data Source Name (DSN)** to `PharmacyDSN`.
   - Browse and select your database file: `d:\6th SEM\ANTIGRAVITY\Pharmacy_dashboard\pharmacy_analytics.db`.
3. **Power BI Get Data**:
   - Open Power BI Desktop.
   - Click **Get Data** -> **ODBC**.
   - Select `PharmacyDSN` as the DSN, then import the tables: `customers`, `products`, `inventory`, and `transactions`.

### Option B: Importing Clean CSVs
1. Click **Get Data** -> **Text/CSV**.
2. Import the processed CSVs from `data/processed/`:
   - `cleaned_customers.csv`
   - `cleaned_products.csv`
   - `cleaned_inventory.csv`
   - `processed_pharmacy_data.csv` (Transactions)

---

## 2. Table Relationships (Data Model)

Define the following relationships in the **Model View** of Power BI:

- **transactions** `[product_id]` (Many-to-One `* : 1`) -> **products** `[product_id]`
  - *Cross filter direction*: Single
- **transactions** `[customer_id]` (Many-to-One `* : 1`) -> **customers** `[customer_id]`
  - *Cross filter direction*: Single
- **inventory** `[product_id]` (One-to-One `1 : 1`) -> **products** `[product_id]`
  - *Cross filter direction*: Both

---

## 3. Key DAX Measures (15+ Measures)

Create these measures inside a dedicated measure table or within the `transactions` table:

### Financial & Sales Metrics
1. **Total Revenue**
   ```dax
   Total Revenue = SUM(transactions[sales_amount])
   ```
2. **Total Cost of Goods (COGS)**
   ```dax
   Total COGS = SUM(transactions[cogs])
   ```
3. **Total Profit**
   ```dax
   Total Profit = [Total Revenue] - [Total COGS]
   ```
4. **Profit Margin %**
   ```dax
   Profit Margin % = DIVIDE([Total Profit], [Total Revenue], 0)
   ```
5. **Total Orders (Transactions)**
   ```dax
   Total Orders = DISTINCTCOUNT(transactions[transaction_id])
   ```
6. **Average Order Value (AOV)**
   ```dax
   Average Order Value = DIVIDE([Total Revenue], [Total Orders], 0)
   ```

### Customer Metrics
7. **Total Customer Count**
   ```dax
   Total Customers = DISTINCTCOUNT(customers[customer_id])
   ```
8. **Repeat Customers Count**
   ```dax
   Repeat Customers = 
   COUNTROWS(
       FILTER(
           ADDCOLUMNS(
               VALUES(transactions[customer_id]),
               "OrderCount", [Total Orders]
           ),
           [OrderCount] > 1
       )
   )
   ```
9. **Repeat Purchase Rate %**
   ```dax
   Repeat Purchase Rate % = DIVIDE([Repeat Customers], [Total Customers], 0)
   ```
10. **Customer Lifetime Value (CLV)**
    ```dax
    Average CLV = DIVIDE([Total Profit], [Total Customers], 0)
    ```

### Inventory & Stock Health Metrics
11. **Total Inventory Stock Value**
    ```dax
    Inventory Stock Value = SUMX(inventory, inventory[current_stock] * inventory[cost_price])
    ```
12. **Critical SKUs Count** (Stock below Reorder Level)
    ```dax
    Critical SKUs = CALCULATE(COUNT(inventory[product_id]), inventory[current_stock] <= inventory[reorder_level])
    ```
13. **Stockout Risk %**
    ```dax
    Stockout Risk % = DIVIDE([Critical SKUs], COUNT(inventory[product_id]), 0)
    ```
14. **Average Days to Stockout**
    ```dax
    Avg Days to Stockout = AVERAGE(inventory[Days_to_Stockout])
    ```
15. **Category Inventory Turnover Ratio**
    ```dax
    Inv Turnover Ratio = DIVIDE([Total COGS], [Inventory Stock Value], 0)
    ```

---

## 4. Dashboard Page Visual Settings

### Color Palette (Modern Slate Theme)
- **Background**: `#0f172a` (Slate Dark)
- **Card Background**: `#1e293b` (Slate Light Card)
- **Primary Color**: `#00d2ff` (Vibrant Cyan)
- **Success Accent**: `#00ff88` (Vibrant Green)
- **Warning/Alert Accent**: `#ef4444` (Vibrant Red)
- **Text (Data Label)**: `#ffffff`
- **Text (Category Label)**: `#94a3b8`

### Navigation & Bookmarks
1. Set up a **Left-Navigation Pane** on each page using native Power BI page navigation buttons.
2. Group buttons inside a vertical container styled with glassmorphism (translucency: 15% opacity, blur: 15).
3. Create bookmarks for "Show/Hide Table view" on Pages 2 and 3 to allow visual toggle.

---

## 5. Mobile Optimization
- Rearrange visualizations into a single-column layout on the **Mobile Layout** canvas.
- Display the 4 main KPI Cards at the top of the mobile screen.
- Set font size for numeric values to `18pt` to ensure legibility on smaller mobile devices.
