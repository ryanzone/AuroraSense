USE WAREHOUSE COMPUTE_WH;
CREATE OR REPLACE DATABASE AURORA_INVENTORY;
USE DATABASE AURORA_INVENTORY;

CREATE OR REPLACE SCHEMA MAIN;
USE SCHEMA MAIN;

CREATE OR REPLACE TABLE DAILY_STOCK (
    date              DATE,
    location_id       STRING,
    location_name     STRING,
    item_id           STRING,
    item_name         STRING,
    opening_stock     NUMBER,
    received          NUMBER,
    issued            NUMBER,
    closing_stock     NUMBER,
    lead_time_days    NUMBER,
    min_stock_level   NUMBER
);


CREATE OR REPLACE VIEW STOCK_HEALTH AS
SELECT
    date,
    location_id,
    location_name,
    item_id,
    item_name,
    opening_stock,
    received,
    issued,
    closing_stock,
    lead_time_days,
    min_stock_level,

    (opening_stock + received - closing_stock) AS daily_consumption,

    IFF((opening_stock + received - closing_stock) = 0,
        NULL,
        closing_stock / NULLIF((opening_stock + received - closing_stock), 0)
    ) AS days_of_cover,

    CASE
        WHEN closing_stock <= min_stock_level THEN 'CRITICAL'
        WHEN closing_stock <= min_stock_level + 20 THEN 'WARNING'
        ELSE 'OK'
    END AS risk_level

FROM DAILY_STOCK;


CREATE OR REPLACE VIEW STOCK_ALERTS AS
SELECT *
FROM STOCK_HEALTH
WHERE risk_level IN ('CRITICAL', 'WARNING')
ORDER BY date DESC;

INSERT INTO DAILY_STOCK VALUES
-- Paracetamol
('2024-12-01','LOC1','Hospital A','ITM1','Paracetamol',120,30,80,70,3,50),
('2024-12-02','LOC1','Hospital A','ITM1','Paracetamol',70,20,60,30,3,50),
('2024-12-03','LOC1','Hospital A','ITM1','Paracetamol',30,10,30,10,3,50),

('2024-12-01','LOC2','Clinic B','ITM1','Paracetamol',200,40,100,140,4,80),
('2024-12-02','LOC2','Clinic B','ITM1','Paracetamol',140,30,110,60,4,80),
('2024-12-03','LOC2','Clinic B','ITM1','Paracetamol',60,20,70,10,4,80),

-- Amoxicillin
('2024-12-01','LOC1','Hospital A','ITM2','Amoxicillin',90,20,60,50,5,40),
('2024-12-02','LOC1','Hospital A','ITM2','Amoxicillin',50,10,40,20,5,40),
('2024-12-03','LOC1','Hospital A','ITM2','Amoxicillin',20,0,15,5,5,40),

('2024-12-01','LOC3','Rural Health Center','ITM2','Amoxicillin',60,10,20,50,6,30),
('2024-12-02','LOC3','Rural Health Center','ITM2','Amoxicillin',50,20,30,40,6,30),
('2024-12-03','LOC3','Rural Health Center','ITM2','Amoxicillin',40,20,25,35,6,30),

-- Insulin
('2024-12-01','LOC4','City Hospital','ITM3','Insulin',40,20,25,35,2,25),
('2024-12-02','LOC4','City Hospital','ITM3','Insulin',35,10,20,25,2,25),
('2024-12-03','LOC4','City Hospital','ITM3','Insulin',25,0,20,5,2,25),

('2024-12-01','LOC2','Clinic B','ITM3','Insulin',50,10,30,30,2,20),
('2024-12-02','LOC2','Clinic B','ITM3','Insulin',30,10,20,20,2,20),
('2024-12-03','LOC2','Clinic B','ITM3','Insulin',20,5,15,10,2,20),

-- ORS Packets
('2024-12-01','LOC1','Hospital A','ITM4','ORS Packets',300,50,80,270,7,150),
('2024-12-02','LOC1','Hospital A','ITM4','ORS Packets',270,50,100,220,7,150),
('2024-12-03','LOC1','Hospital A','ITM4','ORS Packets',220,40,90,170,7,150),

-- Surgical Gloves
('2024-12-01','LOC3','Rural Health Center','ITM5','Surgical Gloves',500,100,200,400,10,250),
('2024-12-02','LOC3','Rural Health Center','ITM5','Surgical Gloves',400,0,150,250,10,250),
('2024-12-03','LOC3','Rural Health Center','ITM5','Surgical Gloves',250,0,120,130,10,250),

-- IV Fluids
('2024-12-01','LOC4','City Hospital','ITM6','IV Fluids',150,30,70,110,3,100),
('2024-12-02','LOC4','City Hospital','ITM6','IV Fluids',110,20,80,50,3,100),
('2024-12-03','LOC4','City Hospital','ITM6','IV Fluids',50,10,40,20,3,100),

-- Vitamin Tablets
('2024-12-01','LOC2','Clinic B','ITM7','Vitamin Tablets',250,40,100,190,5,120),
('2024-12-02','LOC2','Clinic B','ITM7','Vitamin Tablets',190,20,80,130,5,120),
('2024-12-03','LOC2','Clinic B','ITM7','Vitamin Tablets',130,20,70,80,5,120),

-- Antiseptic Liquid
('2024-12-01','LOC1','Metro Hospital','I100','Antiseptic Liquid',180,40,90,130,4,100),
('2024-12-02','LOC1','Metro Hospital','I100','Antiseptic Liquid',130,20,70,80,4,100),
('2024-12-03','LOC1','Metro Hospital','I100','Antiseptic Liquid',80,10,60,30,4,100),

('2024-12-01','LOC2','Community Clinic','I100','Antiseptic Liquid',120,30,50,100,5,80),
('2024-12-02','LOC2','Community Clinic','I100','Antiseptic Liquid',100,20,40,80,5,80),
('2024-12-03','LOC2','Community Clinic','I100','Antiseptic Liquid',80,10,30,60,5,80),

-- Doxycycline
('2024-12-01','LOC3','Tribal Health Post','I200','Doxycycline',60,15,20,55,6,40),
('2024-12-02','LOC3','Tribal Health Post','I200','Doxycycline',55,10,25,40,6,40),
('2024-12-03','LOC3','Tribal Health Post','I200','Doxycycline',40,10,20,30,6,40),

('2024-12-01','LOC4','Women & Child Care Center','I200','Doxycycline',100,20,40,80,5,50),
('2024-12-02','LOC4','Women & Child Care Center','I200','Doxycycline',80,15,35,60,5,50),
('2024-12-03','LOC4','Women & Child Care Center','I200','Doxycycline',60,10,30,40,5,50),

-- Glucose Drip
('2024-12-01','LOC1','Metro Hospital','I300','Glucose Drip',150,50,80,120,3,90),
('2024-12-02','LOC1','Metro Hospital','I300','Glucose Drip',120,30,70,80,3,90),
('2024-12-03','LOC1','Metro Hospital','I300','Glucose Drip',80,20,60,40,3,90),

('2024-12-01','LOC3','Tribal Health Post','I300','Glucose Drip',90,20,40,70,4,60),
('2024-12-02','LOC3','Tribal Health Post','I300','Glucose Drip',70,10,30,50,4,60),
('2024-12-03','LOC3','Tribal Health Post','I300','Glucose Drip',50,10,25,35,4,60),

-- Bandages
('2024-12-01','LOC2','Community Clinic','I400','Bandages',300,60,120,240,7,150),
('2024-12-02','LOC2','Community Clinic','I400','Bandages',240,40,110,170,7,150),
('2024-12-03','LOC2','Community Clinic','I400','Bandages',170,30,100,100,7,150),

('2024-12-01','LOC4','Women & Child Care Center','I400','Bandages',200,50,80,170,7,120),
('2024-12-02','LOC4','Women & Child Care Center','I400','Bandages',170,20,60,130,7,120),
('2024-12-03','LOC4','Women & Child Care Center','I400','Bandages',130,20,50,100,7,120),

-- Nebulizer Kits
('2024-12-01','LOC1','Metro Hospital','I500','Nebulizer Kits',40,10,20,30,5,25),
('2024-12-02','LOC1','Metro Hospital','I500','Nebulizer Kits',30,5,15,20,5,25),
('2024-12-03','LOC1','Metro Hospital','I500','Nebulizer Kits',20,5,10,15,5,25),

('2024-12-01','LOC3','Tribal Health Post','I500','Nebulizer Kits',25,5,10,20,6,15),
('2024-12-02','LOC3','Tribal Health Post','I500','Nebulizer Kits',20,5,10,15,6,15),
('2024-12-03','LOC3','Tribal Health Post','I500','Nebulizer Kits',15,5,10,10,6,15),

-- Pain Relief Spray
('2024-12-01','LOC2','Community Clinic','I600','Pain Relief Spray',90,20,30,80,4,50),
('2024-12-02','LOC2','Community Clinic','I600','Pain Relief Spray',80,15,35,60,4,50),
('2024-12-03','LOC2','Community Clinic','I600','Pain Relief Spray',60,10,40,30,4,50),

-- Zinc Supplements
('2024-12-01','LOC4','Women & Child Care Center','I700','Zinc Supplements',200,30,80,150,6,120),
('2024-12-02','LOC4','Women & Child Care Center','I700','Zinc Supplements',150,20,70,100,6,120),
('2024-12-03','LOC4','Women & Child Care Center','I700','Zinc Supplements',100,10,50,60,6,120);

