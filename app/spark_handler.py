from pyspark.sql import SparkSession

def init_spark():
    spark = SparkSession.builder \
        .appName("VoiceCommandApp") \
        .config("spark.sql.shuffle.partitions", "2") \
        .getOrCreate()
    return spark
