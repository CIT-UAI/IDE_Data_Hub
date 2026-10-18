-- ===============================================================================
-- IDE CIT — CONSULTAS AMAZON ATHENA PARA AUDITORÍA FORENSE DE LOGS CLOUDFRONT
-- Centro de Inteligencia Territorial (CIT-UAI) · Universidad Adolfo Ibáñez
-- ===============================================================================

-- 1. Creación de la Tabla Externa en Athena para los Logs de CloudFront
CREATE EXTERNAL TABLE IF NOT EXISTS default.ide_cit_cloudfront_logs (
  `date` DATE,
  `time` STRING,
  `location` STRING,
  `bytes` BIGINT,
  `request_ip` STRING,
  `method` STRING,
  `host` STRING,
  `uri_stem` STRING,
  `status` INT,
  `referrer` STRING,
  `user_agent` STRING,
  `uri_query` STRING,
  `cookie` STRING,
  `x_edge_result_type` STRING,
  `x_edge_request_id` STRING,
  `x_host_header` STRING,
  `cs_protocol` STRING,
  `cs_bytes` BIGINT,
  `time_taken` FLOAT,
  `x_forwarded_for` STRING,
  `ssl_protocol` STRING,
  `ssl_cipher` STRING,
  `x_edge_response_result_type` STRING,
  `cs_protocol_version` STRING,
  `fle_status` STRING,
  `fle_encrypted_fields` INT,
  `c_port` INT,
  `time_to_first_byte` FLOAT,
  `x_edge_detailed_result_type` STRING,
  `sc_content_type` STRING,
  `sc_content_len` BIGINT,
  `sc_range_start` BIGINT,
  `sc_range_end` BIGINT
)
ROW FORMAT DELIMITED 
FIELDS TERMINATED BY '\t'
LOCATION 's3://ide-cit-access-logs-us-east-1/cloudfront/'
TBLPROPERTIES ( 'skip.header.line.count'='2' );

-- 2. Top 20 IPs con mayor volumen de peticiones (Detección de Scrapers)
SELECT 
  request_ip, 
  count(*) AS total_requests,
  sum(bytes) / (1024 * 1024) AS total_mb_downloaded,
  count(DISTINCT uri_stem) AS unique_paths
FROM default.ide_cit_cloudfront_logs
WHERE `date` >= CURRENT_DATE - INTERVAL '7' DAY
GROUP BY request_ip
ORDER BY total_requests DESC
LIMIT 20;

-- 3. Top 15 Archivos Binarios más Descargados y Consumo de Egress
SELECT 
  uri_stem,
  count(*) AS download_count,
  sum(bytes) / (1024 * 1024 * 1024) AS total_gb_served,
  count(DISTINCT request_ip) AS unique_users
FROM default.ide_cit_cloudfront_logs
WHERE uri_stem LIKE '/download/%'
GROUP BY uri_stem
ORDER BY total_gb_served DESC
LIMIT 15;

-- 4. Peticiones Bloqueadas por Rate-Limiting WAF (HTTP 429)
SELECT 
  `date`,
  `time`,
  request_ip,
  uri_stem,
  status,
  user_agent
FROM default.ide_cit_cloudfront_logs
WHERE status = 429
ORDER BY `date` DESC, `time` DESC
LIMIT 50;

-- 5. Auditoría de Errores 404 (Detección de Rutas Rotas o Escaneo de Vulnerabilidades)
SELECT 
  uri_stem,
  count(*) AS occurrences,
  count(DISTINCT request_ip) AS unique_ips
FROM default.ide_cit_cloudfront_logs
WHERE status = 404
GROUP BY uri_stem
ORDER BY occurrences DESC
LIMIT 25;
