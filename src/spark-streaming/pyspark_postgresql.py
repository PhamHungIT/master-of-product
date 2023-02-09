from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from pyspark.sql.types import StructType, StructField, StringType, StringType, TimestampType

spark = SparkSession.builder \
    .appName('process_laptop_data_from_kafka_to_postgresql') \
    .getOrCreate()

# Reduce logging verbosity
spark.sparkContext.setLogLevel("WARN")

KAFKA_BOOTSTRAP_SERVERS = "localhost:29092"
KAFKA_TOPIC = "testTopic1"

SCHEMA = StructType([
    StructField("Product", StringType()),
    StructField("Price", StringType()),
    StructField("Brand", StringType()),
    StructField("Core", StringType()),
    StructField("RAM", StringType()),
    StructField("ScrSize", StringType()),
    StructField("GraphicCard", StringType()),
    StructField("Drive_Type", StringType()),
    StructField("Capacity", StringType()),
    StructField("OperSystem", StringType()),
    StructField("Weight", StringType()),
    StructField("Madein", StringType()),
    StructField("Since", StringType()),
    StructField("Shop", StringType()),
    StructField("URL", StringType())
])

df_stream = spark \
    .readStream.format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS) \
    .option("subscribe", KAFKA_TOPIC) \
    .option("startingOffsets", "earliest") \
    .load()

db_target_properties = {"user":"postgres", "password":"password", "driver": "org.postgresql.Driver"} # change password before run

def write_to_function(df, epoch_id):
    dfwriter = df.write.mode('append')
    dfwriter.jdbc(url='jdbc:postgresql://localhost:5432/test_db',  table="laptops",  properties=db_target_properties)
    pass

# Write to MySQL Table
df_stream = df_stream \
    .select(
        F.from_json(
            F.decode(F.col('value'), 'iso-8859-1'),
            SCHEMA
        ).alias('value')
    ) \
    .select('value.Product', 'value.Price', 'value.Brand', 'value.Core', 'value.RAM', 'value.ScrSize', 'value.GraphicCard', 'value.Drive_Type', 'value.Capacity', 'value.OperSystem', 'value.Weight', 'value.Madein', 'value.Since', 'value.Shop', 'value.URL') \
    .writeStream \
    .foreachBatch(write_to_function) \
    .start() \
    .awaitTermination()
