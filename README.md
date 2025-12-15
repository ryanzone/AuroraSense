
# AuroraSense:–  AI Inventory Health Dashboard

AuroraSense is a real-time inventory monitoring and forecasting dashboard built using **Snowflake Streamlit**, providing instant visibility into stock levels, health status, consumption trends, and risk alerts across multiple locations.

The dashboard identifies **critical shortages**, predicts **stockout dates**, and provides **actionable insights** to support fast and informed supply-chain decisions.

---

## Live Working Prototype (Snowflake Streamlit)

Click below to open the hosted working model:

https://app.snowflake.com/nnvfrzc/vl98936/#/streamlit-apps/AURORA_INVENTORY.PUBLIC.HS83MDTAYG8W3429

---

## **Key Features**

### **1. Real-Time Inventory Health**

* Highlights **Critical**, **Warning**, and **Healthy** items
* KPI cards summarizing global stock status
* Automatic risk categorization using Days of Cover

### **2. High-Risk Alerts**

* Dedicated alert section for items nearing stockout
* Filterable by **location** and **item**

### **3. Forecasted Stockout Dates**

* Predicts estimated stockout based on:

  * Days of cover
  * Daily consumption
  * Current movement trends

### **4. Multi-Layered Visual Analytics**

* **Heatmap** for stock availability across locations
* **Bar charts** for comparing Days of Cover
* **Trend line charts** for historical stock movement

### **5. Interactive Filters**

* Filter by **location**, **item**, and **chart type**
* Dashboard auto-updates dynamically

### **6. AI-Generated Inventory Summary**

* Summarizes critical risks
* Lists actionable recommendations
* Uses Snowflake Cortex with fallback logic

---

## **Tech Stack**

### **Backend & Data Layer**

* **Snowflake Data Cloud**
* Snowflake Tables:

  * `DAILY_STOCK`
  * `STOCK_HEALTH`
  * `STOCK_ALERTS`

### **Frontend / App Layer**

* **Streamlit for Snowflake**
* **Python (Pandas, Altair, datetime)**
* **Snowpark** for data access
* **Altair** for interactive charts



## **Screenshots**



![Dashboard Overview](https://github.com/ryanzone/AuroraSense/blob/main/ss/Screenshot%202025-12-06%20010200.png)

![Dashboard Overview](https://github.com/ryanzone/AuroraSense/blob/main/ss/Screenshot%202025-12-06%20010215.png)

![Dashboard Overview](https://github.com/ryanzone/AuroraSense/blob/main/ss/Screenshot%202025-12-06%20010233.png)

![Dashboard Overview](https://github.com/ryanzone/AuroraSense/blob/main/ss/Screenshot%202025-12-06%20010255.png)

## **How to Use**

1. Open the Snowflake app using the link above
2. Select a **location** and **item** from the sidebar
3. Navigate through:

   * Stock health KPIs
   * Top-risk items
   * Stockout forecast table
   * Alerts
   * Charts
     
4. Click **Generate Summary** for AI insights



## 🛠️ **Setup (If Running Locally)**

```bash
pip install streamlit pandas altair snowflake-snowpark-python
streamlit run app.py
```

Snowflake credentials required for live data.


## 🧠 **AI Summary Logic**

The app uses:

1. **Snowflake Cortex GPT-4o-mini**
2. Custom fallback summarizer if AI query fails
