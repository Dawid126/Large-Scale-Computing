import boto3
import time

    
s3 = boto3.client('s3')

bucket = 'dawid126bucket'
filename = 'file.txt'
with open(filename, 'rb') as f:
    file = f.read()
measurements = []
for i in range(6):
    print("Measurement: ", i)
    start = time.time()
    s3.put_object(Body=file, Bucket=bucket, Key=filename)
    end = time.time()
    measurements.append(end - start)

avg_upload_time = sum(measurements) / 6
    
measurements = []
for i in range(6):
    print("Measurement", i)
    start = time.time()
    response = s3.get_object(Bucket=bucket, Key=filename)
    content = response['Body'].read()
    end = time.time()
    measurements.append(end - start)

avg_download_time = sum(measurements) / 6

print("Upload: ", avg_upload_time)
print("Download: ", avg_download_time)
    
    