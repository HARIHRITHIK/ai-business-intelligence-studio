import os
import pandas as pd
import numpy as np

def create_retail_sales():
    np.random.seed(42)
    dates = pd.date_range(start='2023-01-01', end='2024-12-31', freq='M')
    regions = ['North', 'South', 'East', 'West']
    categories = ['Electronics', 'Clothing', 'Food', 'Home', 'Sports']
    
    data = []
    for date in dates:
        for region in regions:
            for category in categories:
                # North outperforms by ~35%
                base_units = np.random.randint(50, 200)
                if region == 'North':
                    base_units = int(base_units * 1.35)
                
                # Q4 spike
                if date.month in [10, 11, 12]:
                    base_units = int(base_units * 1.5)
                
                # 2024 growth (+18%)
                if date.year == 2024:
                    base_units = int(base_units * 1.18)
                
                # Electronics highest revenue, lowest margin
                if category == 'Electronics':
                    price = np.random.uniform(200, 800)
                    base_margin = np.random.uniform(0.1, 0.15)
                elif category == 'Clothing':
                    price = np.random.uniform(20, 100)
                    base_margin = np.random.uniform(0.3, 0.45)
                else:
                    price = np.random.uniform(10, 150)
                    base_margin = np.random.uniform(0.2, 0.35)
                
                discount = np.random.uniform(0, 0.3)
                margin = max(0.01, base_margin - discount * 0.8) # Discount negatively correlated with margin
                
                revenue = base_units * price * (1 - discount)
                
                data.append({
                    'Date': date,
                    'Region': region,
                    'Product_Category': category,
                    'Product_Name': f'{category}_Item_{np.random.randint(1, 20)}',
                    'Units_Sold': base_units,
                    'Unit_Price': round(price, 2),
                    'Revenue': round(revenue, 2),
                    'Discount_Rate': round(discount, 2),
                    'Profit_Margin': round(margin, 2)
                })
    
    df = pd.DataFrame(data)
    os.makedirs('data/samples', exist_ok=True)
    df.to_csv('data/samples/retail_sales.csv', index=False)
    print("Created retail_sales.csv")

def create_hr_analytics():
    np.random.seed(42)
    n = 400
    depts = ['Engineering', 'Sales', 'Marketing', 'Operations', 'HR']
    
    data = []
    for i in range(n):
        dept = np.random.choice(depts, p=[0.4, 0.25, 0.15, 0.15, 0.05])
        
        # Engineering low attrition, Sales high attrition
        if dept == 'Engineering':
            attrition_prob = 0.12
            salary = np.random.normal(90000, 15000)
        elif dept == 'Sales':
            attrition_prob = 0.35
            salary = np.random.normal(100000, 20000)
        else:
            attrition_prob = 0.22
            salary = np.random.normal(70000, 15000)
            
        tenure = np.random.uniform(0.1, 15)
        # Low tenure high attrition
        if tenure < 2:
            attrition_prob *= 1.5
            
        # Low salary high attrition
        if salary < 60000:
            attrition_prob *= 1.3
            
        attrition = 'Yes' if np.random.random() < attrition_prob else 'No'
        
        # Performance vs Overtime for attrited
        if attrition == 'Yes':
            overtime = np.random.uniform(20, 40)
            performance = np.random.randint(1, 4) # Lower performance
        else:
            overtime = np.random.uniform(0, 20)
            performance = np.random.randint(3, 6)
            
        data.append({
            'Employee_ID': f'EMP{i:04d}',
            'Department': dept,
            'Tenure_Years': round(tenure, 1),
            'Age': np.random.randint(22, 58),
            'Gender': np.random.choice(['Male', 'Female']),
            'Salary': round(salary, 2),
            'Performance_Score': performance,
            'Attrition': attrition,
            'Last_Promotion_Years': min(round(tenure), np.random.randint(0, 8)),
            'Overtime_Hours_Monthly': round(overtime, 1)
        })
        
    df = pd.DataFrame(data)
    df.to_csv('data/samples/hr_analytics.csv', index=False)
    print("Created hr_analytics.csv")

def create_customer_churn():
    np.random.seed(42)
    n = 700
    
    data = []
    for i in range(n):
        contract = np.random.choice(['Month-to-Month', 'One_Year', 'Two_Year'], p=[0.5, 0.3, 0.2])
        internet = np.random.choice(['DSL', 'Fiber_Optic', 'None'])
        
        churn_prob = 0.1
        
        if contract == 'Month-to-Month':
            churn_prob = 0.45
        elif contract == 'Two_Year':
            churn_prob = 0.05
            
        if internet == 'Fiber_Optic':
            churn_prob *= 1.3
            monthly_charge = np.random.uniform(80, 120)
        elif internet == 'DSL':
            monthly_charge = np.random.uniform(40, 80)
        else:
            monthly_charge = np.random.uniform(20, 40)
            
        support_tickets = np.random.randint(0, 9)
        if support_tickets > 3:
            churn_prob = 0.60
            
        tenure = np.random.randint(1, 73)
        if tenure < 6:
            churn_prob *= 1.5
            
        churn_prob = min(0.95, churn_prob)
        churn = 'Yes' if np.random.random() < churn_prob else 'No'
        
        data.append({
            'Customer_ID': f'CUST{i:04d}',
            'Tenure_Months': tenure,
            'Monthly_Charges': round(monthly_charge, 2),
            'Total_Charges': round(monthly_charge * tenure, 2),
            'Contract_Type': contract,
            'Internet_Service': internet,
            'Support_Tickets_Last_Year': support_tickets,
            'Churned': churn,
            'Payment_Method': np.random.choice(['Electronic', 'Mailed_Check', 'Bank_Transfer', 'Credit_Card']),
            'Age_Group': np.random.choice(['18-25', '26-35', '36-50', '51+'])
        })
        
    df = pd.DataFrame(data)
    df.to_csv('data/samples/customer_churn.csv', index=False)
    print("Created customer_churn.csv")

if __name__ == '__main__':
    create_retail_sales()
    create_hr_analytics()
    create_customer_churn()
