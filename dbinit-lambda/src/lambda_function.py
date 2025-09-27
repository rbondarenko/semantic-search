import json, boto3, psycopg2, os
try:
    import cfnresponse
except ImportError:
    print("[INFO] cfnresponse not available, using mock")
    
    class MockCfnResponse:
        SUCCESS = "SUCCESS"
        FAILED = "FAILED"
        
        @staticmethod
        def send(event, context, responseStatus, responseData, physicalResourceId=None, noEcho=False, reason=None):
            print(f"Mock cfnresponse.send called:")
            print(f"  Status: {responseStatus}")
            print(f"  Data: {responseData}")
            print(f"  Reason: {reason}")
            return True
   
    cfnresponse = MockCfnResponse()

def get_secret(secret_arn):
    sm = boto3.client("secretsmanager")
    sec = sm.get_secret_value(SecretId=secret_arn)
    return json.loads(sec["SecretString"])
def handler(event, context):
    if event["RequestType"] in ("Create","Update"):
        db_secret = get_secret(os.environ["DB_SECRET_ARN"])
        try:
            conn = psycopg2.connect(
              host=db_secret['host'],
              port=db_secret['port'],
              user=db_secret['username'],
              password=db_secret['password'],
              dbname=db_secret['dbname']
            )
            cur = conn.cursor()
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
            cur.execute("""
              CREATE TABLE IF NOT EXISTS products (
                asin  CHAR(10) PRIMARY KEY,
                title TEXT,
                department VARCHAR(255),
                description TEXT,
                embedding VECTOR(384)
              );
            """)
            # NOTE: embedding vector size depends on selected LLM model: check LLMModelName parameter in ecs.yaml
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            print("Error:", e)
            cfnresponse.send(event, context, cfnresponse.FAILED, {})
            return
    cfnresponse.send(event, context, cfnresponse.SUCCESS, {})
