from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, count

spark = SparkSession.builder \
    .appName("Optimization") \
    .config("spark.sql.shuffle.partitions", "8") \
    .getOrCreate()

print("="*60)
print("🔧 ОПТИМИЗАЦИЯ SPARK")
print("="*60)

df = spark.read.csv("big_data_10m.csv", header=True, inferSchema=True)

print(f"\n📊 Количество партиций до оптимизации: {df.rdd.getNumPartitions()}")

# Репартиционируем (распределяем данные по 8 ядрам)
df_optimized = df.repartition(8)
print(f"📊 Количество партиций после оптимизации: {df_optimized.rdd.getNumPartitions()}")

# Кешируем данные в память (для ускорения повторных запросов)
df_optimized.cache()

# Выполняем группировку
result = df_optimized.groupBy("segment").agg(
    count("*").alias("count"),
    avg("balance").alias("avg_balance")
)

result.show()

spark.stop()