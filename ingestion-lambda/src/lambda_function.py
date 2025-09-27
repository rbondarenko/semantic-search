import psycopg2
import requests
import re
import json
import boto3
import csv
import os
import urllib.parse
from io import StringIO
import logging
from typing import Dict, Any
from datetime import datetime

csv.field_size_limit(100000000)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

LLM_SECRET_ARN = os.environ["LLM_SECRET_ARN"]
DB_SECRET_ARN = os.environ["DB_SECRET_ARN"]
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    logger.info(f"Received S3 event: {json.dumps(event, indent=2)}")
    llm_secret = get_secret(LLM_SECRET_ARN)
    db_secret = get_secret(DB_SECRET_ARN)
    conn = psycopg2.connect(
        host=db_secret['host'],
        port=db_secret['port'],
        user=db_secret['username'],
        password=db_secret['password'],
        dbname=db_secret['dbname']
    )
    cursor = conn.cursor()
    results = []
    bucket_name = None
    object_key = None

    for record in event['Records']:
        try:
            event_name = record['eventName']
            bucket_name = record['s3']['bucket']['name']
            object_key = urllib.parse.unquote_plus(record['s3']['object']['key'])
            object_size = record['s3']['object']['size']
            logger.info(f"Processing: {event_name} - {bucket_name}/{object_key} ({object_size} bytes)")
            if not event_name.startswith('ObjectCreated:'):
                logger.info(f"Skipping non-creation event: {event_name}")
                continue
            if not object_key.lower().endswith('.csv'):
                logger.info(f"Skipping non-CSV file: {object_key}")
                continue
            cursor.execute("TRUNCATE TABLE products;") # exception
            result = process_csv_file(bucket_name, object_key, llm_secret["url"], cursor)
            results.append(result)
        except Exception as e:
            logger.error(f"Error processing record: {str(e)}")
            results.append({
                'bucket': bucket_name,
                'key': object_key,
                'status': 'error',
                'error': str(e)
            })

    conn.commit()
    cursor.close()
    conn.close()

    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': f'Processed {len(results)} files',
            'results': results
        })
    }

def get_secret(secret_arn):
    sm = boto3.client("secretsmanager")
    sec = sm.get_secret_value(SecretId=secret_arn)
    return json.loads(sec["SecretString"])

def process_csv_file(bucket_name: str, object_key: str, llm_service_url: str, cursor) -> Dict[str, Any]:
    try:
        logger.info(f"Starting to process CSV file: {bucket_name}/{object_key}")
        csv_content = download_csv_from_s3(bucket_name, object_key)
        processed_count, error_count = process_csv_records(csv_content, bucket_name, object_key, llm_service_url, cursor)
        logger.info(f"Successfully processed {processed_count} records from {object_key}")
        return {
            'bucket': bucket_name,
            'key': object_key,
            'status': 'success',
            'processed_records': processed_count,
            'error_records': error_count
        }
    except Exception as e:
        logger.error(f"Error processing CSV file {object_key}: {str(e)}")
        raise e

def download_csv_from_s3(bucket_name: str, object_key: str) -> str:
    try:
        logger.info(f"Downloading {object_key} from {bucket_name}")
        if os.getenv('TEST_RUN') == 'True':
            with open("../data/amazon-products.csv", "r", encoding="utf-8") as f:
                csv_content = f.read()
        else:
            response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
            csv_content = response['Body'].read().decode('utf-8')
        logger.info(f"Downloaded {len(csv_content)} characters from {object_key}")
        return csv_content
    except Exception as e:
        logger.error(f"Error downloading file from S3: {str(e)}")
        raise e

def process_csv_records(csv_content: str, bucket_name: str, object_key: str, llm_service_url: str, cursor) -> tuple:
    processed_count = 0
    error_count = 0
    try:
        csv_reader = csv.DictReader(StringIO(csv_content))
        logger.info(f"CSV headers: {csv_reader.fieldnames}")
        for row_number, row in enumerate(csv_reader, start=1):
            try:
                processed_record = process_single_record(row, row_number, bucket_name, object_key, llm_service_url, cursor)
                if processed_record:
                    processed_count += 1
            except Exception as e:
                logger.error(f"Error processing row {row_number}: {str(e)}")
                error_count += 1
                log_error_record(row, row_number, str(e), bucket_name, object_key)
        
        logger.info(f"Processed {processed_count} records, {error_count} errors")
        return processed_count, error_count
    except Exception as e:
        logger.error(f"Error parsing CSV: {str(e)}")
        raise e

def process_single_record(row: Dict[str, str], row_number: int, bucket_name: str, object_key: str, llm_service_url: str, cursor) -> Dict[str, Any]:
    # data format:
    #   timestamp,title,seller_name,brand,description,initial_price,final_price,currency,availability,reviews_count,
    #   categories,asin,buybox_seller,number_of_sellers,root_bs_rank,answered_questions,domain,images_count,url,
    #   video_count,image_url,item_weight,rating,product_dimensions,seller_id,date_first_available,discount,model_number,
    #   manufacturer,department,plus_content,upc,video,top_review,variations,delivery,features,format,buybox_prices,
    #   parent_asin,input_asin,ingredients,origin_url,bought_past_month,is_available,root_bs_category,bs_category,
    #   bs_rank,badge,subcategory_rank,amazon_choice,images,product_details,prices_breakdown,country_of_origin
    try:
        logger.debug(f"Processing record {row_number}")
        # Check required fields
        required_fields = ['title', 'seller_name', 'brand', 'description', 'reviews_count', 'categories', 'asin',
                           'url', 'rating', 'model_number', 'manufacturer', 'department', 'features', 'amazon_choice',
                           'product_details', 'country_of_origin']

        for field in required_fields:
            if row.get(field) is None:
                raise ValueError(f"Missing required field: {field}")
            if field == 'asin' and not is_valid_asin(row[field].strip()):
                raise ValueError(f"Missing required field: {field}")

        # extract data
        asin = normalize_asin(row['asin'].strip())
        title = row.get('title', '').strip()
        dept = row.get('department', '').strip()
        desc = row.get('description', '').strip()

        # get vector
        text = asin + " " + " ".join(filter(None, [row.get(f, '').strip() for f in required_fields if f != 'asin' and f]))
        r = requests.post(llm_service_url + '/embed', json={"text": text}) # exception
        emb = r.json()["embedding"]

        # store
        cursor.execute("""
            INSERT INTO products (asin, title, department, description, embedding)
            VALUES (%s, %s, %s, %s, %s);
            """, (asin, title, dept, desc, emb)) # exception

        processed_record = {
            'asin': asin,
            'title': title,
            'department': dept,
            'source_file': f"{bucket_name}/{object_key}",
            'row_number': row_number,
            'processed_at': datetime.utcnow().isoformat(),
            'status': 'processed'
        }
        logger.debug(f"Processed record {row_number}: {asin}")
        return processed_record
    except Exception as e:
        logger.error(f"Error processing record {row_number}: {str(e)}")
        raise e

def is_valid_asin(asin):
    """
    Validate ASIN format
    - Exactly 10 characters
    - Alphanumeric only
    - Usually starts with B for non-books
    """
    if not asin or len(asin) != 10:
        return False
    if not re.match(r'^[A-Z0-9]{10}$', asin.upper()):
        return False
    return True

def normalize_asin(asin):
    if not asin:
        return None
    normalized = asin.strip().upper()
    if is_valid_asin(normalized):
        return normalized
    return None

def log_error_record(row: Dict[str, str], row_number: int, error: str, bucket_name: str, object_key: str):
    error_record = {
        'source_file': f"{bucket_name}/{object_key}",
        'row_number': row_number,
        'error': error,
        'raw_data': row,
        'timestamp': datetime.utcnow().isoformat()
    }
    logger.error(f"Error record: {json.dumps(error_record)}")

def main():
    test_event = {
        "Records": [
            {
                "eventVersion": "2.1",
                "eventSource": "aws:s3",
                "awsRegion": "us-east-1",
                "eventTime": "2024-01-15T10:30:45.123Z",
                "eventName": "ObjectCreated:Put",
                "s3": {
                    "s3SchemaVersion": "1.0",
                    "configurationId": "csv-upload-event",
                    "bucket": {"name": "test", "arn": "arn:aws:s3:::test"},
                    "object": {"key": "test.csv", "size": 85286}
                }
            }
        ]
    }
    lambda_handler(test_event, None)

if __name__ == '__main__':
    main()