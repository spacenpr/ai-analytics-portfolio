from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, count, sum as spark_sum

# Создаем сессию Spark
spark = SparkSession.builder.appName("BankChurnAnalysis").getOrCreate()

# Загружаем CSV (убедись, что файл лежит в папке D:\AIAGENT)
df = spark.read.csv("bank_churn_dataset.csv", header=True, inferSchema=True)

# Показываем схему данных (типы колонок)
print("Схема данных:")
df.printSchema()

# Считаем количество записей
print(f"\nВсего записей: {df.count()}")

# Группировка по сегменту клиентов
segment_stats = df.groupBy("customer_segment").agg(
    count("*").alias("count"),
    avg("balance").alias("avg_balance"),
    avg("credit_sco").alias("avg_creditscore")
)

print("\nСтатистика по сегментам клиентов:")
segment_stats.show()

# Останавливаем Spark
spark.stop()