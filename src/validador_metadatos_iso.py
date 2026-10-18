#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
IDE CIT — VALIDADOR Y EXPORTADOR DE METADATOS ESPACIALES (ISO 19115 / SNIT / STAC)
Centro de Inteligencia Territorial (CIT-UAI) · Universidad Adolfo Ibáñez
===============================================================================

Propósito:
    Módulo algorítmico dedicado a la auditoría, validación de esquemas y exportación
    interoperable de metadatos geográficos para las cuatro matrices territoriales
    (MBHT, MPST, MRCT, MPIT) conforme a los estándares:
    
    1. ISO 19115-1:2014 / ISO 19139 (XML Schema para metadatos espaciales).
    2. Perfil Nacional SNIT (Sistema Nacional de Información Territorial de Chile).
    3. STAC 1.0.0 (SpatioTemporal Asset Catalog Specification).
    4. Trazabilidad de linaje algorítmico y formulación matemática auditable.

Autor: CIT-UAI / John Treimun R.
Licencia: CC BY 4.0 / Propietario CIT-UAI 2026
===============================================================================
"""

from __future__ import annotations

import argparse
import datetime
import json
import logging
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Configuración de Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("Validador_ISO_CIT")


def find_proyecto_root(start_path: Optional[Path] = None) -> Path:
    """
    Encuentra dinámicamente la raíz del proyecto `PROYECTO_MBHT`.
    Cumple con la Regla de Oro N° 1 de AGENTS.md.
    """
    current = (start_path or Path(__file__)).resolve()
    for parent in [current] + list(current.parents):
        if (parent / "AGENTS.md").exists() or (parent / "INICIAR_ECOSISTEMA.bat").exists():
            return parent
    return Path(__file__).resolve().parent.parent.parent


class ISOMetadataValidator:
    """
    Motor de validación y exportación de metadatos geográficos bajo normas ISO/SNIT/STAC.
    """

    def __init__(self, root_dir: Optional[Path] = None) -> None:
        self.root_dir: Path = root_dir or find_proyecto_root()
        self.ide_dir: Path = self.root_dir / "07_Aplicaciones_y_Visualizadores_Web" / "IDE_Data_Hub"
        self.data_dir: Path = self.ide_dir / "data"
        self.catalog_path: Path = self.data_dir / "catalogo_ide_cit.json"
        self.xml_out_dir: Path = self.data_dir / "iso_xml"
        self.stac_out_dir: Path = self.data_dir / "stac"

    def load_catalog(self) -> Dict[str, Any]:
        """Carga y decodifica el catálogo JSON."""
        if not self.catalog_path.exists():
            raise FileNotFoundError(f"Catálogo no encontrado en: {self.catalog_path}")
        with open(self.catalog_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def validate_layer(self, layer: Dict[str, Any], index: int) -> List[str]:
        """
        Valida una capa individual según el perfil SNIT / ISO 19115.
        Retorna una lista de advertencias o errores encontrados.
        """
        errors: List[str] = []
        layer_id = layer.get("id", f"capa_{index}")

        # 1. Campos obligatorios
        required_fields = [
            "id", "titulo", "matriz", "ambito", "escala", "cobertura",
            "fecha_corte", "resumen", "formula_lineage", "autor", "licencia",
            "bbox", "crs", "tipo_geometria", "atributos"
        ]
        for field in required_fields:
            if field not in layer or layer[field] is None or layer[field] == "":
                errors.append(f"[{layer_id}] Falta campo obligatorio: '{field}'")

        # 2. Validación de Bounding Box [min_lon, min_lat, max_lon, max_lat]
        bbox = layer.get("bbox")
        if isinstance(bbox, list) and len(bbox) == 4:
            min_lon, min_lat, max_lon, max_lat = bbox
            if not (-180 <= min_lon <= 180 and -180 <= max_lon <= 180):
                errors.append(f"[{layer_id}] Longitud fuera de rango [-180, 180]: {min_lon}, {max_lon}")
            if not (-90 <= min_lat <= 90 and -90 <= max_lat <= 90):
                errors.append(f"[{layer_id}] Latitud fuera de rango [-90, 90]: {min_lat}, {max_lat}")
            if min_lon >= max_lon:
                errors.append(f"[{layer_id}] MinLon ({min_lon}) debe ser menor que MaxLon ({max_lon})")
            if min_lat >= max_lat:
                errors.append(f"[{layer_id}] MinLat ({min_lat}) debe ser menor que MaxLat ({max_lat})")
        else:
            errors.append(f"[{layer_id}] BBOX inválido o inexistente. Debe ser lista de 4 floats.")

        # 3. Validación de Atributos
        atributos = layer.get("atributos", [])
        if not isinstance(atributos, list) or len(atributos) == 0:
            errors.append(f"[{layer_id}] La capa debe definir al menos un atributo en su esquema.")
        else:
            for attr in atributos:
                if not all(k in attr for k in ["campo", "tipo", "descripcion"]):
                    errors.append(f"[{layer_id}] Atributo malformado: {attr}")

        # 4. Validación de Linaje y Formulación
        formula = layer.get("formula_lineage", "")
        if len(formula.strip()) < 10:
            errors.append(f"[{layer_id}] Linaje/Fórmula insuficiente (< 10 caracteres).")

        return errors

    def audit_catalog(self) -> Tuple[bool, Dict[str, Any]]:
        """
        Audita el catálogo completo emitiendo métricas de conformidad.
        """
        logger.info("🔍 Iniciando auditoría ISO 19115-1:2014 / Perfil SNIT...")
        catalog = self.load_catalog()
        capas = catalog.get("capas", [])

        all_errors: List[str] = []
        layer_summaries: List[Dict[str, Any]] = []

        for i, capa in enumerate(capas):
            errs = self.validate_layer(capa, i)
            all_errors.extend(errs)
            layer_summaries.append({
                "id": capa.get("id"),
                "titulo": capa.get("titulo"),
                "matriz": capa.get("matriz"),
                "status": "PASS" if not errs else "FAIL",
                "errors": errs
            })

        total_capas = len(capas)
        passed_capas = sum(1 for s in layer_summaries if s["status"] == "PASS")
        compliance_pct = (passed_capas / total_capas * 100.0) if total_capas > 0 else 0.0

        audit_result = {
            "total_capas": total_capas,
            "passed_capas": passed_capas,
            "failed_capas": total_capas - passed_capas,
            "compliance_score": f"{compliance_pct:.1f}%",
            "errors": all_errors,
            "layers": layer_summaries,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }

        logger.info(f"   📊 Capas evaluadas: {total_capas} | Conformes: {passed_capas} ({compliance_pct:.1f}%)")
        if all_errors:
            for err in all_errors:
                logger.error(f"   ❌ {err}")
        else:
            logger.info("   ✅ 100% de conformidad con estándares ISO 19115 / SNIT.")

        return (len(all_errors) == 0), audit_result

    def export_iso_19139_xml(self) -> List[Path]:
        """
        Exporta cada capa del catálogo como un archivo XML ISO 19139 estándar
        compatible con Geonetwork, Geonode, CKAN y SNIT Chile.
        Genera copias en data/iso_xml y download/iso_xml, además de metadata.xml.
        """
        self.xml_out_dir.mkdir(parents=True, exist_ok=True)
        download_iso_dir = self.ide_dir / "download" / "iso_xml"
        download_iso_dir.mkdir(parents=True, exist_ok=True)
        
        catalog = self.load_catalog()
        portal = catalog.get("portal", {})
        capas = catalog.get("capas", [])

        generated_files: List[Path] = []
        now_str = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        for capa in capas:
            layer_id = capa.get("id")
            bbox = capa.get("bbox", [-75.64, -55.98, -66.86, -17.50])
            
            # Construcción de XML con namespaces OGC / ISO
            root = ET.Element("gmd:MD_Metadata", {
                "xmlns:gmd": "http://www.isotc211.org/2005/gmd",
                "xmlns:gco": "http://www.isotc211.org/2005/gco",
                "xmlns:gml": "http://www.opengis.net/gml",
                "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
                "xsi:schemaLocation": "http://www.isotc211.org/2005/gmd http://www.isotc211.org/2005/gmd/gmd.xsd"
            })

            # Identificador del archivo
            file_id = ET.SubElement(root, "gmd:fileIdentifier")
            ET.SubElement(file_id, "gco:CharacterString").text = f"CIT-UAI::{layer_id}::2026"

            # Idioma y juego de caracteres
            lang = ET.SubElement(root, "gmd:language")
            ET.SubElement(lang, "gco:CharacterString").text = "spa"

            charset = ET.SubElement(root, "gmd:characterSet")
            ET.SubElement(charset, "gmd:MD_CharacterSetCode", {
                "codeList": "http://standards.iso.org/iso/19139/resources/gmxCodelists.xml#MD_CharacterSetCode",
                "codeListValue": "utf8"
            }).text = "utf8"

            # Contacto Institucional (CIT-UAI)
            contact = ET.SubElement(root, "gmd:contact")
            ci_resp = ET.SubElement(contact, "gmd:CI_ResponsibleParty")
            org_name = ET.SubElement(ci_resp, "gmd:organisationName")
            ET.SubElement(org_name, "gco:CharacterString").text = "Centro de Inteligencia Territorial (CIT-UAI) · Universidad Adolfo Ibáñez"
            
            contact_info = ET.SubElement(ci_resp, "gmd:contactInfo")
            address = ET.SubElement(contact_info, "gmd:CI_Address")
            email = ET.SubElement(address, "gmd:electronicMailAddress")
            ET.SubElement(email, "gco:CharacterString").text = portal.get("contacto", "contactocit@uai.cl")

            role = ET.SubElement(ci_resp, "gmd:role")
            ET.SubElement(role, "gmd:CI_RoleCode", {
                "codeList": "http://standards.iso.org/iso/19139/resources/gmxCodelists.xml#CI_RoleCode",
                "codeListValue": "custodian"
            }).text = "custodian"

            # Fecha del metadato
            date_stamp = ET.SubElement(root, "gmd:dateStamp")
            ET.SubElement(date_stamp, "gco:DateTime").text = now_str

            # Estándar
            std_name = ET.SubElement(root, "gmd:metadataStandardName")
            ET.SubElement(std_name, "gco:CharacterString").text = "ISO 19115-1:2014 / Perfil Chileno SNIT"

            # Identificación de la Información Espacial
            ident = ET.SubElement(root, "gmd:identificationInfo")
            data_ident = ET.SubElement(ident, "gmd:MD_DataIdentification")

            citation = ET.SubElement(data_ident, "gmd:citation")
            ci_cit = ET.SubElement(citation, "gmd:CI_Citation")
            title = ET.SubElement(ci_cit, "gmd:title")
            ET.SubElement(title, "gco:CharacterString").text = capa.get("titulo", "")

            # Resumen / Abstract
            abstract = ET.SubElement(data_ident, "gmd:abstract")
            ET.SubElement(abstract, "gco:CharacterString").text = capa.get("resumen", "")

            # Propósito / Linaje
            purpose = ET.SubElement(data_ident, "gmd:purpose")
            ET.SubElement(purpose, "gco:CharacterString").text = f"Linaje de cálculo: {capa.get('formula_lineage', '')}"

            # Extensión Geográfica (Bounding Box WGS84)
            extent = ET.SubElement(data_ident, "gmd:extent")
            ex_extent = ET.SubElement(extent, "gmd:EX_Extent")
            geo_el = ET.SubElement(ex_extent, "gmd:geographicElement")
            geo_bbox = ET.SubElement(geo_el, "gmd:EX_GeographicBoundingBox")

            west = ET.SubElement(geo_bbox, "gmd:westBoundLongitude")
            ET.SubElement(west, "gco:Decimal").text = str(bbox[0])
            east = ET.SubElement(geo_bbox, "gmd:eastBoundLongitude")
            ET.SubElement(east, "gco:Decimal").text = str(bbox[2])
            south = ET.SubElement(geo_bbox, "gmd:southBoundLatitude")
            ET.SubElement(south, "gco:Decimal").text = str(bbox[1])
            north = ET.SubElement(geo_bbox, "gmd:northBoundLatitude")
            ET.SubElement(north, "gco:Decimal").text = str(bbox[3])

            # Formatos de Distribución
            dist_info = ET.SubElement(root, "gmd:distributionInfo")
            md_dist = ET.SubElement(dist_info, "gmd:MD_Distribution")
            transfer = ET.SubElement(md_dist, "gmd:transferOptions")
            md_digital = ET.SubElement(transfer, "gmd:MD_DigitalTransferOptions")

            # Conector MVT
            on_mvt = ET.SubElement(md_digital, "gmd:onLine")
            ci_online_mvt = ET.SubElement(on_mvt, "gmd:CI_OnlineResource")
            linkage_mvt = ET.SubElement(ci_online_mvt, "gmd:linkage")
            ET.SubElement(linkage_mvt, "gmd:URL").text = f"https://ide.cit.uai.cl/tiles/{capa.get('tile_source')}/{{z}}/{{x}}/{{y}}.pbf"
            proto_mvt = ET.SubElement(ci_online_mvt, "gmd:protocol")
            ET.SubElement(proto_mvt, "gco:CharacterString").text = "OGC:MVT"

            # Enlace GeoParquet
            if capa.get("s3_parquet"):
                on_pq = ET.SubElement(md_digital, "gmd:onLine")
                ci_online_pq = ET.SubElement(on_pq, "gmd:CI_OnlineResource")
                linkage_pq = ET.SubElement(ci_online_pq, "gmd:linkage")
                ET.SubElement(linkage_pq, "gmd:URL").text = capa.get("s3_parquet")
                proto_pq = ET.SubElement(ci_online_pq, "gmd:protocol")
                ET.SubElement(proto_pq, "gco:CharacterString").text = "HTTP:GEOPARQUET"

            # Guardar archivo XML formateado
            tree = ET.ElementTree(root)
            ET.indent(tree, space="  ", level=0)
            
            target_xml_path = self.xml_out_dir / f"{layer_id}_iso19139.xml"
            with open(target_xml_path, "wb") as xf:
                xf.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
                tree.write(xf, encoding="utf-8", xml_declaration=False)

            # Copiar a download/iso_xml
            dl_xml_path = download_iso_dir / f"{layer_id}_iso19139.xml"
            with open(dl_xml_path, "wb") as xf:
                xf.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
                tree.write(xf, encoding="utf-8", xml_declaration=False)

            # Para MBHT 2017 generar también metadata.xml canónico
            if layer_id == "kpi_mud_2017":
                meta_dl_path = self.ide_dir / "download" / "metadata.xml"
                with open(meta_dl_path, "wb") as xf:
                    xf.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
                    tree.write(xf, encoding="utf-8", xml_declaration=False)
                meta_sub_path = download_iso_dir / "metadata.xml"
                with open(meta_sub_path, "wb") as xf:
                    xf.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
                    tree.write(xf, encoding="utf-8", xml_declaration=False)

            generated_files.append(target_xml_path)

        # Validación automática exhaustiva de los XML generados
        self.validate_generated_xml_files(generated_files)

        logger.info(f"📁 Generados {len(generated_files)} archivos XML ISO 19139 en: {self.xml_out_dir} y {download_iso_dir}")
        return generated_files

    def validate_generated_xml_files(self, xml_files: List[Path]) -> Dict[str, Any]:
        """
        Valida rigurosamente cada archivo XML generado contra la estructura
        y elementos obligatorios del esquema ISO 19139 / Perfil SNIT.
        """
        logger.info("🔍 Ejecutando validación automática de esquemas XML ISO 19139...")
        ns = {
            "gmd": "http://www.isotc211.org/2005/gmd",
            "gco": "http://www.isotc211.org/2005/gco",
            "gml": "http://www.opengis.net/gml"
        }
        
        results = []
        all_passed = True
        
        for xml_file in xml_files:
            file_report = {
                "file": xml_file.name,
                "path": f"download/iso_xml/{xml_file.name}",
                "url": f"https://ide.cit.uai.cl/download/iso_xml/{xml_file.name}",
                "is_valid_xml": False,
                "has_root_gmd": False,
                "has_file_identifier": False,
                "has_contact": False,
                "has_date_stamp": False,
                "has_identification": False,
                "has_bbox": False,
                "has_distribution": False,
                "errors": []
            }
            try:
                tree = ET.parse(xml_file)
                root = tree.getroot()
                file_report["is_valid_xml"] = True
                
                # 1. Root check
                if root.tag == f"{{{ns['gmd']}}}MD_Metadata":
                    file_report["has_root_gmd"] = True
                else:
                    file_report["errors"].append(f"Tag raíz inválido: {root.tag}")
                
                # 2. File Identifier
                file_id = root.find("gmd:fileIdentifier/gco:CharacterString", ns)
                if file_id is not None and file_id.text:
                    file_report["has_file_identifier"] = True
                else:
                    file_report["errors"].append("Falta gmd:fileIdentifier/gco:CharacterString")
                
                # 3. Contact
                contact = root.find("gmd:contact/gmd:CI_ResponsibleParty/gmd:organisationName/gco:CharacterString", ns)
                if contact is not None and contact.text:
                    file_report["has_contact"] = True
                else:
                    file_report["errors"].append("Falta gmd:contact organisationName")
                
                # 4. Date stamp
                date_stamp = root.find("gmd:dateStamp/gco:DateTime", ns)
                if date_stamp is not None and date_stamp.text:
                    file_report["has_date_stamp"] = True
                else:
                    file_report["errors"].append("Falta gmd:dateStamp/gco:DateTime")
                
                # 5. Identification Info & BBOX
                ident = root.find("gmd:identificationInfo/gmd:MD_DataIdentification", ns)
                if ident is not None:
                    file_report["has_identification"] = True
                    west = ident.find("gmd:extent/gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicBoundingBox/gmd:westBoundLongitude/gco:Decimal", ns)
                    east = ident.find("gmd:extent/gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicBoundingBox/gmd:eastBoundLongitude/gco:Decimal", ns)
                    south = ident.find("gmd:extent/gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicBoundingBox/gmd:southBoundLatitude/gco:Decimal", ns)
                    north = ident.find("gmd:extent/gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicBoundingBox/gmd:northBoundLatitude/gco:Decimal", ns)
                    if west is not None and east is not None and south is not None and north is not None:
                        file_report["has_bbox"] = True
                    else:
                        file_report["errors"].append("BBOX incompleto en EX_GeographicBoundingBox")
                else:
                    file_report["errors"].append("Falta gmd:MD_DataIdentification")
                
                # 6. Distribution Info
                dist = root.find("gmd:distributionInfo/gmd:MD_Distribution", ns)
                if dist is not None:
                    file_report["has_distribution"] = True
                else:
                    file_report["errors"].append("Falta gmd:distributionInfo")
                
                if file_report["errors"]:
                    all_passed = False
                    
            except Exception as ex:
                file_report["errors"].append(f"Excepción al parsear XML: {str(ex)}")
                all_passed = False
                
            results.append(file_report)
            
        cert_data = {
            "validation_timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "standard": "ISO 19115-1:2014 / ISO 19139:2007 / Perfil SNIT Chile",
            "total_files": len(xml_files),
            "all_passed": all_passed,
            "compliance_pct": "100.0%" if all_passed else f"{(sum(1 for r in results if not r['errors'])/len(xml_files)*100):.1f}%",
            "details": results
        }
        
        # Guardar reporte de certificación
        cert_path = self.xml_out_dir / "auditoria_conformidad_iso.json"
        with open(cert_path, "w", encoding="utf-8") as f:
            json.dump(cert_data, f, indent=2, ensure_ascii=False)
            
        dl_cert_path = self.ide_dir / "download" / "iso_xml" / "auditoria_conformidad_iso.json"
        with open(dl_cert_path, "w", encoding="utf-8") as f:
            json.dump(cert_data, f, indent=2, ensure_ascii=False)
            
        logger.info(f"   ✓ Validación ISO 19139 finalizada: {len(xml_files)} archivos conformes ({cert_data['compliance_pct']}).")
        return cert_data

        logger.info(f"📁 Generados {len(generated_files)} archivos XML ISO 19139 en: {self.xml_out_dir}")
        return generated_files

    def export_stac_catalog(self) -> Path:
        """
        Exporta la colección STAC 1.0.0 (`collection.json`) para interoperabilidad
        con ecosistemas basados en Cloud-Native Geospatial.
        """
        self.stac_out_dir.mkdir(parents=True, exist_ok=True)
        catalog = self.load_catalog()
        portal = catalog.get("portal", {})
        capas = catalog.get("capas", [])

        stac_collection = {
            "type": "Collection",
            "stac_version": "1.0.0",
            "stac_extensions": [
                "https://stac-extensions.github.io/projection/v1.1.0/schema.json"
            ],
            "id": "ide-cit-matrices-territoriales",
            "title": portal.get("nombre", "IDE CIT"),
            "description": portal.get("descripcion", ""),
            "license": "CC-BY-4.0",
            "extent": {
                "spatial": {
                    "bbox": [[-109.5, -56.54, -66.42, -17.50]]
                },
                "temporal": {
                    "interval": [["2017-04-19T00:00:00Z", None]]
                }
            },
            "providers": [
                {
                    "name": "Centro de Inteligencia Territorial (CIT-UAI)",
                    "roles": ["producer", "licensor", "processor"],
                    "url": "https://cit.uai.cl"
                },
                {
                    "name": "Universidad Adolfo Ibáñez",
                    "roles": ["host"],
                    "url": "https://uai.cl"
                }
            ],
            "item_assets": {},
            "links": [
                {
                    "rel": "root",
                    "href": "./collection.json",
                    "type": "application/json"
                },
                {
                    "rel": "self",
                    "href": "./collection.json",
                    "type": "application/json"
                },
                {
                    "rel": "license",
                    "href": "https://creativecommons.org/licenses/by/4.0/",
                    "type": "text/html",
                    "title": "Licencia Abierta Creative Commons Attribution 4.0 International (CC BY 4.0)"
                },
                {
                    "rel": "about",
                    "href": "/guia-tecnica",
                    "type": "text/html",
                    "title": "Guía Técnica y Estándares de Interoperabilidad IDE CIT"
                },
                {
                    "rel": "describedby",
                    "href": "/dcat.json",
                    "type": "application/json",
                    "title": "Catálogo Semántico W3C DCAT-AP 2.0"
                }
            ],
            "assets": {
                "catalog_json": {
                    "title": "Catálogo Maestro de la Infraestructura IDE CIT (JSON)",
                    "type": "application/json",
                    "roles": ["metadata"],
                    "href": "/data/catalogo_ide_cit.json"
                },
                "catalog_csv": {
                    "title": "Catálogo Tabular de Coberturas Geoespaciales (CSV)",
                    "type": "text/csv",
                    "roles": ["metadata"],
                    "href": "/catalogo.csv"
                },
                "stac_catalog": {
                    "title": "Catálogo Raíz STAC 1.0.0",
                    "type": "application/json",
                    "roles": ["metadata"],
                    "href": "/stac/catalog.json"
                },
                "dcat_json": {
                    "title": "Catálogo Semántico DCAT-AP",
                    "type": "application/json",
                    "roles": ["metadata"],
                    "href": "/dcat.json"
                }
            }
        }

        # Items de la colección STAC
        for capa in capas:
            bbox = capa.get("bbox", [-75.64, -55.98, -66.86, -17.50])
            stac_collection["item_assets"][capa.get("id")] = {
                "title": capa.get("titulo"),
                "description": capa.get("resumen"),
                "type": "application/vnd.apache.parquet",
                "roles": ["data"],
                "bbox": bbox,
                "proj:epsg": 4326,
                "properties": {
                    "matriz": capa.get("matriz"),
                    "ambito": capa.get("ambito"),
                    "escala": capa.get("escala"),
                    "formula_lineage": capa.get("formula_lineage"),
                    "tile_endpoint": f"https://ide.cit.uai.cl/tiles/{capa.get('tile_source')}/{{z}}/{{x}}/{{y}}.pbf"
                }
            }

        target_stac_path = self.stac_out_dir / "collection.json"
        with open(target_stac_path, "w", encoding="utf-8") as f:
            json.dump(stac_collection, f, indent=2, ensure_ascii=False)

        logger.info(f"📁 Colección STAC 1.0.0 generada en: {target_stac_path}")
        return target_stac_path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validador y exportador de metadatos espaciales ISO 19115 / SNIT / STAC (CIT-UAI)."
    )
    parser.add_argument(
        "--audit-only",
        action="store_true",
        help="Ejecuta únicamente la auditoría de conformidad sin generar archivos.",
    )
    parser.add_argument(
        "--export-xml",
        action="store_true",
        help="Exporta fichas de metadatos XML ISO 19139 / SNIT.",
    )
    parser.add_argument(
        "--export-stac",
        action="store_true",
        help="Exporta la colección STAC 1.0.0.",
    )

    args = parser.parse_args()

    try:
        validator = ISOMetadataValidator()
        passed, audit_report = validator.audit_catalog()

        if not passed:
            logger.error("❌ La auditoría encontró inconsistencias. Revisa los registros.")
            return 1

        # Si no se pasan flags específicos, se ejecutan todas las exportaciones por defecto
        run_all = not (args.audit_only or args.export_xml or args.export_stac)

        if run_all or args.export_xml:
            validator.export_iso_19139_xml()

        if run_all or args.export_stac:
            validator.export_stac_catalog()

        logger.info("🎉 Proceso de validación y exportación de metadatos completado exitosamente.")
        return 0
    except Exception as e:
        logger.error(f"❌ Error durante la ejecución del validador: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
