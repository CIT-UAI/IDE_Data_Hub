#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Creación y despliegue del colector serverless de telemetría para IDE CIT.
"""
import boto3
import json
import os
import time
import zipfile
import io

session_kwargs = {"region_name": "us-east-1"}
if os.environ.get("AWS_ACCESS_KEY_ID") and os.environ.get("AWS_SECRET_ACCESS_KEY"):
    session_kwargs["aws_access_key_id"] = os.environ.get("AWS_ACCESS_KEY_ID")
    session_kwargs["aws_secret_access_key"] = os.environ.get("AWS_SECRET_ACCESS_KEY")
session = boto3.Session(**session_kwargs)

lam = session.client("lambda")
role_arn = "arn:aws:iam::192584119994:role/IdeCitTelemetryLambdaRole"

lambda_code = '''import json
import boto3
import time
import os
import uuid
from datetime import datetime, timezone

s3 = boto3.client('s3')
BUCKET = os.environ.get('BUCKET_NAME', 'ide.cit.uai.cl')

def handler(event, context):
    method = event.get('requestContext', {}).get('http', {}).get('method', 'GET')
    
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
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

    # Enriquecer con metadatos
    now = datetime.now(timezone.utc)
    http_ctx = event.get('requestContext', {}).get('http', {})
    req_headers = event.get('headers', {})
    
    source_ip = http_ctx.get('sourceIp', 'unknown')
    user_agent = http_ctx.get('userAgent', req_headers.get('user-agent', 'unknown'))
    country = req_headers.get('cloudfront-viewer-country', 'unknown')
    
    record = {
        'id': str(uuid.uuid4()),
        'timestamp': now.isoformat(),
        'source_ip': source_ip,
        'country': country,
        'user_agent': user_agent,
        'payload': payload
    }
    
    # Escribir en S3 particionado por fecha
    prefix = f"telemetry/events/{now.strftime('%Y/%m/%d')}"
    key = f"{prefix}/{int(time.time()*1000)}_{record['id'][:8]}.json"
    try:
        s3.put_object(
            Bucket=BUCKET,
            Key=key,
            Body=json.dumps(record, ensure_ascii=False),
            ContentType='application/json'
        )
    except Exception as e:
        print(f"Error guardando en S3: {e}")
        
    return {
        'statusCode': 200,
        'headers': headers,
        'body': json.dumps({'status': 'ok', 'id': record['id']})
    }
'''

buf = io.BytesIO()
with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("lambda_function.py", lambda_code)
zip_bytes = buf.getvalue()

print("[*] Desplegando Lambda ide-cit-telemetry-collector...")
try:
    fn = lam.create_function(
        FunctionName="ide-cit-telemetry-collector",
        Runtime="python3.11",
        Role=role_arn,
        Handler="lambda_function.handler",
        Code={"ZipFile": zip_bytes},
        Description="Colector serverless de telemetría y consultas del copiloto para IDE CIT",
        Timeout=10,
        MemorySize=128,
        Environment={"Variables": {"BUCKET_NAME": "ide.cit.uai.cl"}}
    )
    print(f"[OK] Lambda creada: {fn['FunctionArn']}")
except lam.exceptions.ResourceConflictException:
    lam.update_function_code(FunctionName="ide-cit-telemetry-collector", ZipFile=zip_bytes)
    print("[OK] Lambda actualizada.")

# Crear o verificar Function URL
try:
    url_cfg = lam.create_function_url_config(
        FunctionName="ide-cit-telemetry-collector",
        AuthType="NONE",
        Cors={
            "AllowOrigins": ["*"],
            "AllowMethods": ["*"],
            "AllowHeaders": ["content-type"]
        }
    )
    function_url = url_cfg["FunctionUrl"]
    print(f"[OK] Function URL creada: {function_url}")
except lam.exceptions.ResourceConflictException:
    url_cfg = lam.get_function_url_config(FunctionName="ide-cit-telemetry-collector")
    function_url = url_cfg["FunctionUrl"]
    print(f"[OK] Function URL existente: {function_url}")

# Permiso público para invocar la Function URL
try:
    lam.add_permission(
        FunctionName="ide-cit-telemetry-collector",
        StatementId="FunctionURLAllowPublicAccess",
        Action="lambda:InvokeFunctionUrl",
        Principal="*",
        FunctionUrlAuthType="NONE"
    )
    print("[OK] Permiso público asignado.")
except Exception as e:
    print(f"[INFO] Permiso ya configurado: {e}")

print(f"\nEndpoint público listo: {function_url}")
