from sqlalchemy import create_engine, text
import pandas as pd

# ================================================================
# ПОДКЛЮЧЕНИЕ
# ================================================================
PASSWORD = "TBILISI"
engine = create_engine(f"postgresql://postgres:{PASSWORD}@localhost:5432/bank_churn")

print("=" * 60)
print("📊 SQL АНАЛИТИКА НА POSTGRESQL")
print("=" * 60)

# ================================================================
# 1. БАЗОВАЯ СТАТИСТИКА
# ================================================================
print("\n1. ОБЩАЯ СТАТИСТИКА ПО КЛИЕНТАМ")
query_stats = """
SELECT 
    COUNT(*) as total_clients,
    ROUND(AVG(credit_sco)::numeric, 0) as avg_credit_score,
    ROUND(AVG(balance)::numeric, 0) as avg_balance,
    ROUND(AVG(age)::numeric, 0) as avg_age,
    ROUND(AVG(engagement_score)::numeric, 1) as avg_engagement
FROM clients;
"""
df = pd.read_sql_query(query_stats, engine)
print(df)

# ================================================================
# 2. CTE: АНАЛИЗ РИСКА ПО СЕГМЕНТАМ
# ================================================================
print("\n2. CTE: АНАЛИЗ РИСКА ПО СЕГМЕНТАМ")
query_cte = """
WITH risk_analysis AS (
    SELECT 
        customer_segment,
        COUNT(*) as client_count,
        ROUND(AVG(risk_score)::numeric, 4) as avg_risk,
        ROUND(AVG(balance)::numeric, 0) as avg_balance
    FROM clients
    GROUP BY customer_segment
)
SELECT 
    customer_segment,
    client_count,
    avg_risk,
    avg_balance,
    ROUND(client_count * 100.0 / SUM(client_count) OVER (), 1) as segment_share
FROM risk_analysis
ORDER BY avg_risk DESC;
"""
df = pd.read_sql_query(query_cte, engine)
print(df)

# ================================================================
# 3. ОКОННАЯ ФУНКЦИЯ: ТОП-5 КЛИЕНТОВ ПО БАЛАНСУ В КАЖДОМ СЕГМЕНТЕ
# ================================================================
print("\n3. ТОП-5 КЛИЕНТОВ ПО БАЛАНСУ В КАЖДОМ СЕГМЕНТЕ")
query_top5 = """
WITH ranked_clients AS (
    SELECT 
        customer_segment,
        age,
        balance,
        ROW_NUMBER() OVER (PARTITION BY customer_segment ORDER BY balance DESC) as rank
    FROM clients
)
SELECT 
    customer_segment,
    age,
    balance,
    rank
FROM ranked_clients
WHERE rank <= 5
ORDER BY customer_segment, rank;
"""
df = pd.read_sql_query(query_top5, engine)
print(df)

# ================================================================
# 4. ОКОННАЯ ФУНКЦИЯ LAG: РАЗНИЦА МЕЖДУ СОСЕДНИМИ КЛИЕНТАМИ
# ================================================================
print("\n4. РАЗНИЦА В КРЕДИТНОМ СКОРЕ МЕЖДУ СОСЕДНИМИ КЛИЕНТАМИ")
query_lag = """
WITH sorted_clients AS (
    SELECT 
        age,
        credit_sco,
        LAG(credit_sco) OVER (ORDER BY credit_sco DESC) as prev_credit_sco
    FROM clients
    LIMIT 20
)
SELECT 
    age,
    credit_sco,
    prev_credit_sco,
    credit_sco - prev_credit_sco as diff
FROM sorted_clients;
"""
df = pd.read_sql_query(query_lag, engine)
print(df)

# ================================================================
# 5. ГРУППИРОВКА ПО ВОЗРАСТНЫМ КАТЕГОРИЯМ
# ================================================================
print("\n5. АНАЛИЗ ПО ВОЗРАСТНЫМ ГРУППАМ")
query_age_groups = """
SELECT 
    CASE 
        WHEN age < 30 THEN 'До 30'
        WHEN age BETWEEN 30 AND 45 THEN '30-45'
        WHEN age BETWEEN 46 AND 60 THEN '46-60'
        ELSE '60+'
    END as age_group,
    COUNT(*) as client_count,
    ROUND(AVG(balance)::numeric, 0) as avg_balance,
    ROUND(AVG(credit_sco)::numeric, 0) as avg_credit
FROM clients
GROUP BY age_group
ORDER BY age_group;
"""
df = pd.read_sql_query(query_age_groups, engine)
print(df)

print("\n" + "=" * 60)
print("✅ Анализ завершен!")
print("=" * 60)