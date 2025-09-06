"""
Data normalization utilities for ETL pipeline
"""
import re
from typing import Optional, Dict, Tuple
from datetime import datetime


class DataNormalizer:
    """데이터 정규화 유틸리티 클래스"""
    
    # 기관명 정규화 매핑
    INSTITUTION_MAPPING = {
        "대한체육회": "대한체육회",
        "대한올림픽위원회": "대한체육회",
        "KOC": "대한체육회",
        "대한장애인체육회": "대한장애인체육회",
        "KOSAD": "대한장애인체육회",
        "국민체육진흥공단": "국민체육진흥공단",
        "KSPO": "국민체육진흥공단",
        "한국스포츠정책과학원": "한국스포츠정책과학원",
        "KISS": "한국스포츠정책과학원",
        "태릉선수촌": "태릉선수촌",
        "진천선수촌": "진천선수촌",
    }
    
    # 지역코드 정규화 (행정동 기준)
    REGION_CODE_MAPPING = {
        # 서울특별시
        "11": "11000",  # 서울특별시
        "1100": "11000",
        "서울": "11000",
        "서울시": "11000",
        "서울특별시": "11000",
        
        # 부산광역시
        "26": "26000",
        "2600": "26000",
        "부산": "26000",
        "부산시": "26000",
        "부산광역시": "26000",
        
        # 대구광역시
        "27": "27000",
        "2700": "27000",
        "대구": "27000",
        "대구시": "27000",
        "대구광역시": "27000",
        
        # 인천광역시
        "28": "28000",
        "2800": "28000",
        "인천": "28000",
        "인천시": "28000",
        "인천광역시": "28000",
        
        # 광주광역시
        "29": "29000",
        "2900": "29000",
        "광주": "29000",
        "광주시": "29000",
        "광주광역시": "29000",
        
        # 대전광역시
        "30": "30000",
        "3000": "30000",
        "대전": "30000",
        "대전시": "30000",
        "대전광역시": "30000",
        
        # 울산광역시
        "31": "31000",
        "3100": "31000",
        "울산": "31000",
        "울산시": "31000",
        "울산광역시": "31000",
        
        # 세종특별자치시
        "36": "36000",
        "3600": "36000",
        "세종": "36000",
        "세종시": "36000",
        "세종특별자치시": "36000",
        
        # 경기도
        "41": "41000",
        "4100": "41000",
        "경기": "41000",
        "경기도": "41000",
        
        # 강원도
        "42": "42000",
        "4200": "42000",
        "강원": "42000",
        "강원도": "42000",
        
        # 충청북도
        "43": "43000",
        "4300": "43000",
        "충북": "43000",
        "충청북도": "43000",
        
        # 충청남도
        "44": "44000",
        "4400": "44000",
        "충남": "44000",
        "충청남도": "44000",
        
        # 전라북도
        "45": "45000",
        "4500": "45000",
        "전북": "45000",
        "전라북도": "45000",
        
        # 전라남도
        "46": "46000",
        "4600": "46000",
        "전남": "46000",
        "전라남도": "46000",
        
        # 경상북도
        "47": "47000",
        "4700": "47000",
        "경북": "47000",
        "경상북도": "47000",
        
        # 경상남도
        "48": "48000",
        "4800": "48000",
        "경남": "48000",
        "경상남도": "48000",
        
        # 제주특별자치도
        "50": "50000",
        "5000": "50000",
        "제주": "50000",
        "제주도": "50000",
        "제주특별자치도": "50000",
    }
    
    # 스포츠 종목 코드 매핑
    SPORT_CODE_MAPPING = {
        # 하계 종목
        "축구": "SOCCER",
        "야구": "BASEBALL",
        "농구": "BASKETBALL",
        "배구": "VOLLEYBALL",
        "테니스": "TENNIS",
        "탁구": "TABLE_TENNIS",
        "배드민턴": "BADMINTON",
        "골프": "GOLF",
        "수영": "SWIMMING",
        "육상": "ATHLETICS",
        "체조": "GYMNASTICS",
        "태권도": "TAEKWONDO",
        "유도": "JUDO",
        "레슬링": "WRESTLING",
        "복싱": "BOXING",
        "양궁": "ARCHERY",
        "사격": "SHOOTING",
        "펜싱": "FENCING",
        "역도": "WEIGHTLIFTING",
        "사이클": "CYCLING",
        "조정": "ROWING",
        "카누": "CANOE",
        "요트": "SAILING",
        "승마": "EQUESTRIAN",
        "근대5종": "MODERN_PENTATHLON",
        "트라이애슬론": "TRIATHLON",
        
        # 동계 종목
        "스키": "SKI",
        "스노보드": "SNOWBOARD",
        "스케이팅": "SKATING",
        "피겨스케이팅": "FIGURE_SKATING",
        "아이스하키": "ICE_HOCKEY",
        "컬링": "CURLING",
        "봅슬레이": "BOBSLEIGH",
        "루지": "LUGE",
        "스켈레톤": "SKELETON",
        "바이애슬론": "BIATHLON",
        
        # 기타 종목
        "e스포츠": "ESPORTS",
        "당구": "BILLIARDS",
        "볼링": "BOWLING",
        "댄스스포츠": "DANCESPORT",
        "족구": "JOKGU",
        "씨름": "SSIREUM",
    }
    
    @classmethod
    def normalize_institution_name(cls, name: str) -> str:
        """기관명 정규화"""
        if not name:
            return ""
        
        # 공백 및 특수문자 제거
        name = re.sub(r'\s+', '', name.strip())
        name = re.sub(r'[^\w가-힣]', '', name)
        
        # 매핑 테이블에서 찾기
        for key, value in cls.INSTITUTION_MAPPING.items():
            if key in name:
                return value
        
        return name
    
    @classmethod
    def normalize_region_code(cls, code_or_name: str) -> Optional[str]:
        """지역코드 정규화 (행정동 코드 반환)"""
        if not code_or_name:
            return None
        
        # 공백 제거
        code_or_name = code_or_name.strip()
        
        # 매핑 테이블에서 찾기
        return cls.REGION_CODE_MAPPING.get(code_or_name)
    
    @classmethod
    def normalize_sport_code(cls, name: str) -> Tuple[str, str]:
        """종목명을 코드와 카테고리로 정규화
        Returns: (code, category)
        """
        if not name:
            return ("UNKNOWN", "기타")
        
        # 공백 제거
        name = name.strip()
        
        # 매핑 테이블에서 찾기
        code = cls.SPORT_CODE_MAPPING.get(name, f"SPORT_{name.upper()}")
        
        # 카테고리 결정
        if code in ["SOCCER", "BASEBALL", "BASKETBALL", "VOLLEYBALL"]:
            category = "단체구기"
        elif code in ["TENNIS", "TABLE_TENNIS", "BADMINTON", "GOLF"]:
            category = "라켓"
        elif code in ["SWIMMING", "ATHLETICS", "GYMNASTICS"]:
            category = "기초체육"
        elif code in ["TAEKWONDO", "JUDO", "WRESTLING", "BOXING"]:
            category = "격투"
        elif code in ["ARCHERY", "SHOOTING"]:
            category = "표적"
        elif code in ["SKI", "SNOWBOARD", "SKATING", "FIGURE_SKATING", "ICE_HOCKEY", "CURLING"]:
            category = "동계"
        else:
            category = "기타"
        
        return (code, category)
    
    @classmethod
    def normalize_project_name(cls, name: str) -> str:
        """사업명 정규화"""
        if not name:
            return ""
        
        # 불필요한 접두사/접미사 제거
        name = re.sub(r'^\d{4}년?_?', '', name)  # 연도 제거
        name = re.sub(r'사업$', '', name)  # '사업' 접미사 제거
        name = name.strip()
        
        return name
    
    @classmethod
    def parse_budget_amount(cls, amount_str: str) -> float:
        """예산 금액 문자열을 숫자로 변환
        '1,234,567원' -> 1234567.0
        '12.5억원' -> 1250000000.0
        """
        if not amount_str:
            return 0.0
        
        # 문자열 정리
        amount_str = amount_str.strip()
        amount_str = re.sub(r'[,\s]', '', amount_str)  # 콤마와 공백 제거
        
        # 단위 처리
        multiplier = 1
        if '조' in amount_str:
            multiplier = 1_000_000_000_000
            amount_str = re.sub(r'조.*', '', amount_str)
        elif '억' in amount_str:
            multiplier = 100_000_000
            amount_str = re.sub(r'억.*', '', amount_str)
        elif '천만' in amount_str:
            multiplier = 10_000_000
            amount_str = re.sub(r'천만.*', '', amount_str)
        elif '백만' in amount_str:
            multiplier = 1_000_000
            amount_str = re.sub(r'백만.*', '', amount_str)
        elif '만' in amount_str:
            multiplier = 10_000
            amount_str = re.sub(r'만.*', '', amount_str)
        elif '천' in amount_str:
            multiplier = 1_000
            amount_str = re.sub(r'천.*', '', amount_str)
        
        # 원 제거
        amount_str = re.sub(r'원.*', '', amount_str)
        
        try:
            return float(amount_str) * multiplier
        except ValueError:
            return 0.0
    
    @classmethod
    def determine_institution_type(cls, name: str) -> str:
        """기관명으로부터 기관 유형 결정"""
        name = name.upper()
        
        if any(word in name for word in ["부", "처", "청", "위원회"]):
            return "중앙정부"
        elif any(word in name for word in ["도", "시", "군", "구"]):
            return "지방자치단체"
        elif any(word in name for word in ["공단", "공사", "진흥원"]):
            return "공공기관"
        elif any(word in name for word in ["체육회", "연맹", "협회"]):
            return "체육단체"
        else:
            return "기타"
    
    @classmethod
    def determine_project_type(cls, name: str) -> str:
        """사업명으로부터 사업 유형 결정"""
        if any(word in name for word in ["육성", "양성", "교육", "훈련"]):
            return "육성"
        elif any(word in name for word in ["지원", "보조", "후원"]):
            return "지원"
        elif any(word in name for word in ["시설", "건립", "개보수", "인프라"]):
            return "시설"
        elif any(word in name for word in ["연구", "개발", "R&D", "분석"]):
            return "연구"
        elif any(word in name for word in ["대회", "경기", "리그", "이벤트"]):
            return "대회운영"
        else:
            return "기타"
    
    @classmethod
    def infer_region_from_institution(cls, institution_name: str) -> Optional[str]:
        """기관명으로부터 지역 추론"""
        # 지역명이 포함된 경우
        for region_name, region_code in cls.REGION_CODE_MAPPING.items():
            if len(region_name) >= 2 and region_name in institution_name:
                return region_code
        
        # 중앙 기관인 경우 서울로 추론
        if cls.determine_institution_type(institution_name) == "중앙정부":
            return "11000"  # 서울
        
        return None