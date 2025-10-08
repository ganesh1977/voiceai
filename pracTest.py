from pyspark.sql from SparkSession
from pyspakr.sql.function from col,sum

spark = SparkSession.builder.appName("Data Frame").getOrCreate()

data = [
    (1, "rama"),
    (2, "suresh"),
    (3, "sunil"),
    (4, "malli")
]
schema = ["id", "name"]

df = spark.createDataFrame(
    data,
    schema=schema
)
display(df)