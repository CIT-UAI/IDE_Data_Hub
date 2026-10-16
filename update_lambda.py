import json
import boto3
import zipfile
import io

session = boto3.Session(region_name='us-east-1')
lam = session.client('lambda')

code = """import json
import boto3
import time
import os
import uuid
from datetime import datetime, timezone

s3 = boto3.client('s3')
BUCKET = os.environ.get('BUCKET_NAME', 'ide.cit.uai.cl')

def handler(event, context):
    print('LAMBDA_INCOMING_EVENT:', json.dumps(event))
    method = event.get('requestContext', {}).get('http', {}).get('method', 'GET')
    
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': '*',
        'Access-Control-Allow-Headers': '*',
        'Content-Type': 'application/json'
    }
    
    if method == 'OPTIONS':
        return {'statusCode': 204, 'headers': headers, 'body': ''}
        
    try:
        body_raw = event.get('body', '{}')
        if event.get('isBase64Encoded', False):
            import base64
            body_raw = base64.b64decode(body_raw).decode('utf-8')
        payload = json.loads(body_raw) if body_raw else {}
    except Exception as e:
        payload = {'raw': str(event.get('body', '')), 'parse_error': str(e)}

    now = datetime.now(timezone.utc)
    http_ctx = event.get('requestContext', {}).get('http', {})
    req_headers = event.get('headers', {})
    
    source_ip = http_ctx.get('sourceIp', 'unknown')
    user_agent = http_ctx.get('userAgent', req_headers.get('user-agent', 'unknown'))
    country = req_headers.get('cloudfront-viewer-country', 'unknown')
    
    rec_id = str(uuid.uuid4())
    record = {
        'id': rec_id,
        'timestamp': now.isoformat(),
        'source_ip': source_ip,
        'country': country,
        'user_agent': user_agent,
        'payload': payload
    }
    
    prefix = f"telemetry/events/{now.strftime('%Y/%m/%d')}"
    key = f"{prefix}/{int(time.time()*1000)}_{rec_id[:8]}.json"
    try:
        s3.put_object(
            Bucket=BUCKET,
            Key=key,
            Body=json.dumps(record, ensure_ascii=False),
            ContentType='application/json'
        )
        print('SUCCESS_SAVED_S3:', key)
    except Exception as e:
        print(f'Error guardando en S3: {e}')
        
    return {
        'statusCode': 200,
        'headers': headers,
        'body': json.dumps({'status': 'ok', 'id': record['id']})
    }
"""

buf = io.BytesIO()
with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as z:
    z.writestr('lambda_function.py', code)
buf.seek(0)

lam.update_function_code(
    FunctionName='ide-cit-telemetry-collector',
    ZipFile=buf.read()
)
print('Lambda updated successfully!')
