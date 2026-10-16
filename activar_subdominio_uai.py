#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de activación final y vinculación de CloudFront con ide.cit.uai.cl.
Monitorea la validación en ACM y, apenas pase a ISSUED, asocia el alias CNAME
y el certificado SSL a la distribución CloudFront E1POIT4JDVDUUO.
"""
import boto3
import time
import subprocess
import sys

import os
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
CERT_ARN = 'arn:aws:acm:us-east-1:192584119994:certificate/ba979f32-aa1c-44f4-817d-6c6c13e53d5d'
DIST_ID = 'E1POIT4JDVDUUO'
DOMAIN = 'ide.cit.uai.cl'

acm = boto3.client('acm', region_name='us-east-1')
cf = boto3.client('cloudfront', region_name='us-east-1')

print(f"[*] Comprobando estado del certificado ACM ({CERT_ARN})...")
cert = acm.describe_certificate(CertificateArn=CERT_ARN)['Certificate']
status = cert.get('Status')
print(f"    Estado actual: {status}")

if status != 'ISSUED':
    print(f"[-] El certificado aun no esta emitido (Status: {status}).")
    print(f"    Verificando si el registro DNS ya responde...")
    res = subprocess.run(['nslookup', f'_95cb03eea64ee26b0f3c80c823e8efc6.{DOMAIN}', '8.8.8.8'], capture_output=True, text=True)
    if 'wzccmgtwzk' in res.stdout:
        print("    [+] ¡El registro CNAME ya fue detectado en DNS! Esperando a que AWS valide...")
    else:
        print("    [-] El registro CNAME aun no se propaga en el DNS de uai.cl.")
    sys.exit(1)

print("[+] ¡Certificado SSL emitido exitosamente por Amazon!")
print(f"[*] Asociando el dominio '{DOMAIN}' y el certificado SSL a CloudFront ({DIST_ID})...")

res_cf = cf.get_distribution_config(Id=DIST_ID)
config = res_cf['DistributionConfig']
etag = res_cf['ETag']

# 1. Configurar Alias
config['Aliases'] = {
    'Quantity': 1,
    'Items': [DOMAIN]
}

# 2. Configurar Certificado SSL
config['ViewerCertificate'] = {
    'ACMCertificateArn': CERT_ARN,
    'SSLSupportMethod': 'sni-only',
    'MinimumProtocolVersion': 'TLSv1.2_2021',
    'Certificate': CERT_ARN,
    'CertificateSource': 'acm'
}

cf.update_distribution(
    Id=DIST_ID,
    DistributionConfig=config,
    IfMatch=etag
)

print(f"[OK] ¡CloudFront actualizado! El dominio https://{DOMAIN} ha sido vinculado exitosamente.")
print(f"[*] CloudFront esta propagando la configuracion en sus nodos edge...")
