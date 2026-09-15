from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    regexp_extract,
    regexp_replace,
    avg,
    count,
    when
)


# --------------------------------------------------
# 1. Start Spark
# --------------------------------------------------

spark = SparkSession.builder \
    .appName("Books WARC Assignment") \
    .master("local[*]") \
    .getOrCreate()


# --------------------------------------------------
# 2. Read CSV
# --------------------------------------------------

df = spark.read.csv(
    "clean-books-results.csv",
    header=True,
    inferSchema=True
)


# --------------------------------------------------
# 3. Show original data
# --------------------------------------------------

print("=" * 70)
print("BOOK DATA FROM CSV")
print("=" * 70)

df.show(10, truncate=False)


# --------------------------------------------------
# 4. Show DataFrame structure
# --------------------------------------------------

print("\nDATA STRUCTURE")
print("=" * 70)

df.printSchema()


# --------------------------------------------------
# 5. Count total book pages
# --------------------------------------------------

print("\nTOTAL BOOK PAGES")
print("=" * 70)

total_books = df.count()

print("Total book pages:", total_books)


# --------------------------------------------------
# 6. Convert price from string to number
# --------------------------------------------------

df = df.withColumn(
    "price_number",
    regexp_replace(col("price"), "£", "").cast("double")
)


# --------------------------------------------------
# 7. Extract available quantity
# --------------------------------------------------

df = df.withColumn(
    "available_books",
    regexp_extract(
        col("availability"),
        r"\((\d+) available\)",
        1
    )
)


# If the availability is simply "In stock",
# use 1 as the available quantity.
df = df.withColumn(
    "available_books",
    when(
        col("available_books") == "",
        1
    ).otherwise(
        col("available_books").cast("integer")
    )
)


# --------------------------------------------------
# 8. Show cleaned data
# --------------------------------------------------

print("\nCLEANED DATA")
print("=" * 70)

df.select(
    "page_title",
    "price_number",
    "available_books",
    "status",
    "url"
).show(10, truncate=False)


# --------------------------------------------------
# 9. Calculate average price
# --------------------------------------------------

print("\nAVERAGE BOOK PRICE")
print("=" * 70)

df.select(
    avg("price_number").alias("average_price")
).show()


# --------------------------------------------------
# 10. Group books by available quantity
# --------------------------------------------------

print("\nBOOKS BY AVAILABLE QUANTITY")
print("=" * 70)

df.groupBy("available_books") \
    .agg(count("*").alias("number_of_books")) \
    .orderBy("available_books") \
    .show()


# --------------------------------------------------
# 11. Count HTTP status codes
# --------------------------------------------------

print("\nHTTP STATUS CODES")
print("=" * 70)

df.groupBy("status") \
    .agg(count("*").alias("number_of_pages")) \
    .orderBy("status") \
    .show()


# --------------------------------------------------
# 12. Stop Spark
# --------------------------------------------------

spark.stop()

print("=" * 70)
print("Spark processing finished successfully!")
print("=" * 70)
