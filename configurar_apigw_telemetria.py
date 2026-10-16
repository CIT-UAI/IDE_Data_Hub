#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuración de API Gateway HTTP API para telemetría IDE CIT.
"""
import boto3
import os
import json
import urllib.request

session_kwargs = {"region_name": "us-east-1"}
if os.environ.get("AWS_ACCESS_KEY_ID") and os.environ.get("AWS_SECRET_ACCESS_KEY"):
    session_kwargs["aws_access_key_id"] = os.environ.get("AWS_ACCESS_KEY_ID")
    session_kwargs["aws_secret_access_key"] = os.environ.get("AWS_SECRET_ACCESS_KEY")
session = boto3.Session(**session_kwargs)
apigw = session.client("apigatewayv2")
lam = session.client("lambda")

api_id = "jhq5vvt0de"
fn_arn = "arn:aws:lambda:us-east-1:192584119994:function:ide-cit-telemetry-collector"

# 1. Obtener o crear integracion
integrations = apigw.get_integrations(ApiId=api_id)
if integrations.get("Items"):
    int_id = integrations["Items"][0]["IntegrationId"]
    print(f"Integración existente: {int_id}")
else:
    integ = apigw.create_integration(
        ApiId=api_id,
        IntegrationType="AWS_PROXY",
        IntegrationUri=fn_arn,
        PayloadFormatVersion="2.0"
    )
    int_id = integ["IntegrationId"]
    print(f"Integración creada: {int_id}")

# 2. Crear o verificar ruta
routes = apigw.get_routes(ApiId=api_id)
has_route = any(r.get("RouteKey") == "$default" for r in routes.get("Items", []))
if not has_route:
    route = apigw.create_route(
        ApiId=api_id,
        RouteKey="$default",
        Target=f"integrations/{int_id}"
    )
    print("Ruta $default creada.")

# 3. Crear o verificar stage $default
stages = apigw.get_stages(ApiId=api_id)
has_stage = any(s.get("StageName") == "$default" for s in stages.get("Items", []))
if not has_stage:
    stage = apigw.create_stage(
        ApiId=api_id,
        StageName="$default",
        AutoDeploy=True
    )
    print("Stage $default creado con AutoDeploy.")

# 4. Asignar permiso de invocación
try:
    lam.add_permission(
        FunctionName="ide-cit-telemetry-collector",
        StatementId="apigateway-invoke-perm-2",
        Action="lambda:InvokeFunction",
        Principal="apigateway.amazonaws.com",
        SourceArn=f"arn:aws:execute-api:us-east-1:192584119994:{api_id}/*/*"
    )
    print("Permiso asignado a Lambda.")
except Exception as e:
    print(f"Permiso nota: {e}")

endpoint = f"https://{api_id}.execute-api.us-east-1.amazonaws.com"
print(f"\n[OK] API Endpoint listo: {endpoint}")

# 5. Probar con un POST
payload = {
    "type": "test_ping",
    "mensaje": "Probando colector de telemetría CIT",
    "timestamp": "2026-09-24T15:48:00Z"
}
req = urllib.request.Request(
    f"{endpoint}/telemetry",
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json"},
    method="POST"
)
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        print("Status test:", resp.status)
        print("Body test:", resp.read().decode("utf-8"))
except Exception as e:
    print("Error test:", e)
