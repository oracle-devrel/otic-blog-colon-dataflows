#######################################################
# Description: This PySpark script is part of a demo for a blog in the "Behind the Scenes with OCI Engineering" series
# Github Repo: https://github.com/oracle-devrel/otic-blog-colon-dataflows
# Example scenario: You have a tenancy with OCI Audit logs in a bucket, you want to aggregate those logs over a 24hr period and store results in your bucket
# Run instructions: 
# 0. Change tenancy varibles in script
# 1. Script takes a date argument this may vary depending on format used e.g. YYYY-MM-DD
#######################################################
  
# configure spark variables
from pyspark.sql import functions
from pyspark.context import SparkContext
from pyspark.sql.context import SQLContext
from pyspark.sql.session import SparkSession
from pyspark.sql.functions import split, count, input_file_name, floor
from pyspark.sql import DataFrame
from datetime import datetime, timedelta
import sys
  
##Establish a Spark Context 
sc = SparkContext()
sqlContext = SQLContext(sc)
sqlContext.sql("set spark.sql.caseSensitive=true")
spark = SparkSession(sc)
spark.conf.set("spark.sql.files.ignoreCorruptFiles", "true")
  
#Inclusion of ColonFilesystem for objects with ":" character
spark._jsc.hadoopConfiguration().set('fs.oci.impl', 'com.oracle.bmc.hdfs.ColonFilesystem')

#Set tenancy variables
###Log Source tenancy
log_source_tenancy_bucket = '<insert_source_bucket_name>'
log_source_tenancy_namespace = '<insert_source_namespace_name>'
log_source_path_to_logs = '<insert_path_to_log_files>' # Example: '/path/to/logs/' 

#Log source path to load with date argument passed at runtime
#Example: oci://bucket@namespace/*/*/*/2023-09-28*.log.gz
log_source_full_path = "oci://" + log_source_tenancy_bucket + "@" + log_source_tenancy_namespace + "/" + log_source_path_to_logs + sys.argv[1] + "*.log.gz"

###DataFlow result tenancy
dataflow_result_bucket = '<insert_result_bucket_name>'
dataflow_result_namepsace = '<insert_result_namespace_name>'

#Read in objects to dataframe
audit_body = spark.read.option("multiline","false").format('json').load(log_source_full_path).withColumn("FILE_NAME", input_file_name())
   
### Split the File name to obtain the date from the path
filename_split = split(audit_body['FILE_NAME'],'/')

#Extract the region the logs are from from the file name
region = filename_split.getItem(4)
  
### Date Time Split
split_col = split(audit_body['time'], 'T')
audit_body = audit_body.withColumn('date', split_col.getItem(0))
audit_body = audit_body.withColumn('timestamp', split_col.getItem(1)).withColumn('region', filename_split.getItem(4))
  
#### Reduce the complex nested JSON into a high level summary that attempts to preserve items of interest
audit_summary_w_date = audit_body.groupby("date",\
                                          "region", \
                                          "eventSource", \
                                          "data.eventName", \
                                          "type", \
                                          "data.compartmentName", \
                                          "data.identity.userAgent", \
                                          "data.identity.principalName", \
                                          "oracle.tenantid", \
                                          "oracle.compartmentid", \
                                          "data.identity.principalId",\
                                          "data.request.path",\
                                          "data.identity.ipAddress", \
                                          "data.response.status") \
                                          .agg(floor(count('*')).alias('count'))

# Bucket to write files to
#Object storage file path for result output in format oci://<bucket_name>@<object_storage_namespace>/
bucket_result_path="oci://" + dataflow_result_bucket + "@" + dataflow_result_namepsace + "/"

### Get_A_TimeStamp_For_Naming
datestring = datetime.now()
current_date_yyyymmdd = datestring.strftime("%Y%m%d")

#Output results in append mode to the bucket you want with the key
audit_summary_w_date.write.mode("append").csv(bucket_result_path+"_aggregation_results_" + current_date_yyyymmdd)
  
# Stopping Spark Context
sc.stop()  
