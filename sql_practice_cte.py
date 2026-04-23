import sqlite3
import pandas as pd

conn = sqlite3.connect('sales.db')

print("=" * 60)
print("ПРАКТИКА SQL: CTE и ОКОННЫЕ ФУНКЦИИ")
print("=" * 60)

# --------------------------------------------------------------
# ЗАПРОС 1: CTE — топ-менеджеры и их средний чек
# --------------------------------------------------------------
print("\n1. CTE: Топ-менеджеры (продажи > 100000) и их средний чек")

query_cte = """
WITH топ_менеджеры AS (
    SELECT DISTINCT manager 
    FROM sales 
    WHERE amount > 100000
)
SELECT 
    s.manager, 
    ROUND(AVG(s.amount), 2) as средний_чек,
    COUNT(*) as кол_во_продаж
FROM sales s
WHERE s.manager IN (SELECT manager FROM топ_менеджеры)
GROUP BY s.manager
ORDER BY средний_чек DESC;
"""

df = pd.read_sql_query(query_cte, conn)
print(df)

# --------------------------------------------------------------
# ЗАПРОС 2: Ранжирование продаж (ROW_NUMBER)
# --------------------------------------------------------------
print("\n2. Ранжирование продаж по сумме (топ-10)")

query_row_number = """
SELECT 
    id,
    manager,
    amount,
    ROW_NUMBER() OVER (ORDER BY amount DESC) as рейтинг
FROM sales
ORDER BY amount DESC
LIMIT 10;
"""

df = pd.read_sql_query(query_row_number, conn)
print(df)

# --------------------------------------------------------------
# ЗАПРОС 3: LAG — разница с предыдущей продажей по дням
# --------------------------------------------------------------
print("\n3. Динамика продаж по дням (разница с предыдущим днем)")

query_lag = """
WITH daily_sales AS (
    SELECT 
        date,
        SUM(amount) as total_sales
    FROM sales
    GROUP BY date
)
SELECT 
    date,
    total_sales,
    LAG(total_sales, 1) OVER (ORDER BY date) as prev_day_sales,
    ROUND((total_sales - LAG(total_sales, 1) OVER (ORDER BY date)) * 100.0 / 
          LAG(total_sales, 1) OVER (ORDER BY date), 2) as growth_pct
FROM daily_sales
ORDER BY date
LIMIT 20;
"""

df = pd.read_sql_query(query_lag, conn)
print(df)

# --------------------------------------------------------------
# ЗАПРОС 4: Доля продаж менеджера в общих продажах
# --------------------------------------------------------------
print("\n4. Доля каждого менеджера в общих продажах")

query_share = """
SELECT 
    manager,
    ROUND(SUM(amount), 2) as total_sales,
    ROUND(SUM(amount) * 100.0 / SUM(SUM(amount)) OVER (), 2) as share_pct
FROM sales
GROUP BY manager
ORDER BY total_sales DESC;
"""

df = pd.read_sql_query(query_share, conn)
print(df)

# --------------------------------------------------------------
# ЗАПРОС 5: LEAD — продажи на следующий день
# --------------------------------------------------------------
print("\n5. Прогноз: продажи сегодня и ожидание завтра (LEAD)")

query_lead = """
WITH daily_sales AS (
    SELECT 
        date,
        SUM(amount) as total_sales
    FROM sales
    GROUP BY date
)
SELECT 
    date,
    total_sales as sales_today,
    LEAD(total_sales, 1) OVER (ORDER BY date) as sales_tomorrow
FROM daily_sales
ORDER BY date
LIMIT 20;
"""

df = pd.read_sql_query(query_lead, conn)
print(df)

# --------------------------------------------------------------
# ЗАПРОС 6: Сложный — топ-3 продажи каждого менеджера
# --------------------------------------------------------------
print("\n6. Топ-3 продажи каждого менеджера")

query_top3 = """
WITH ranked_sales AS (
    SELECT 
        manager,
        amount,
        date,
        ROW_NUMBER() OVER (PARTITION BY manager ORDER BY amount DESC) as rn
    FROM sales
)
SELECT 
    manager,
    amount,
    date,
    rn as место_в_рейтинге
FROM ranked_sales
WHERE rn <= 3
ORDER BY manager, rn;
"""

df = pd.read_sql_query(query_top3, conn)
print(df.head(20))

conn.close()

print("\n" + "=" * 60)
print("✅ Практика завершена! Все запросы выполнены.")