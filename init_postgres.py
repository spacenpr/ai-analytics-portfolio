import pandas as pd
from sqlalchemy import create_engine, text

# ================================================================
# НАСТРОЙКИ ПОДКЛЮЧЕНИЯ
# ================================================================
# Пароль — тот, который ты установил в PostgreSQL
PASSWORD = "TBILISI"  # Замени на свой!

# Подключение к стандартной базе 'postgres' для создания новой БД
engine_default = create_engine(f"postgresql://postgres:{PASSWORD}@localhost:5432/postgres")

# ================================================================
# 1. СОЗДАЕМ НОВУЮ БАЗУ ДАННЫХ 'bank_churn'
# ================================================================
print("1. Создание базы данных 'bank_churn'...")
try:
    with engine_default.connect() as conn:
        # Закрываем все активные подключения (для Windows)
        conn.execute(text("""
            SELECT pg_terminate_backend(pid)
            FROM pg_stat_activity
            WHERE datname = 'bank_churn' AND pid <> pg_backend_pid();
        """))
        conn.execute(text("COMMIT"))
        # Создаем базу
        conn.execute(text("CREATE DATABASE bank_churn"))
        print("   ✅ База данных 'bank_churn' создана")
except Exception as e:
    if 'already exists' in str(e):
        print("   ✅ База данных 'bank_churn' уже существует")
    else:
        print(f"   ⚠️ Ошибка: {e}")

# ================================================================
# 2. ПОДКЛЮЧАЕМСЯ К НОВОЙ БАЗЕ И СОЗДАЕМ ТАБЛИЦЫ
# ================================================================
engine = create_engine(f"postgresql://postgres:{PASSWORD}@localhost:5432/bank_churn")

print("\n2. Создание таблиц...")

# Читаем CSV файл
df = pd.read_csv('bank_churn_dataset.csv')
print(f"   ✅ Загружено {len(df)} строк из CSV")

# Отправляем данные в PostgreSQL
df.to_sql('clients', engine, if_exists='replace', index=False)
print("   ✅ Таблица 'clients' создана и заполнена")

# ================================================================
# 3. ПРОВЕРЯЕМ, ЧТО ВСЕ ЗАГРУЗИЛОСЬ
# ================================================================
print("\n3. Проверка данных...")

with engine.connect() as conn:
    result = conn.execute(text("SELECT COUNT(*) FROM clients"))
    count = result.scalar()
    print(f"   ✅ В таблице 'clients' {count} записей")

    result = conn.execute(text("SELECT * FROM clients LIMIT 5"))
    print("\n   Первые 5 строк:")
    for row in result:
        print(f"      {row}")

print("\n" + "=" * 60)
print("✅ PostgreSQL готов к работе!")
print("=" * 60)