-- PostgreSQL 확장 설치 (PostGIS 지원)
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS postgis_topology;

-- 한국어 지원을 위한 설정
SET client_encoding = 'UTF8';

-- 한국 시간대 설정
SET timezone = 'Asia/Seoul';

-- 스포츠 시설 데이터를 위한 기본 설정
COMMENT ON DATABASE kspon IS 'KSPON Contest Platform Database - Sports Data Lab';