"""
Redis Cache Helper for Budget-Performance API
Redis 캐시 헬퍼
"""
import json
import hashlib
from typing import Any, Optional, Dict
from datetime import timedelta
import redis.asyncio as redis
from redis.exceptions import RedisError
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)


class CacheManager:
    """Redis 캐시 매니저"""
    
    def __init__(self):
        self.redis_client: Optional[redis.Redis] = None
        self.enabled = settings.REDIS_ENABLED if hasattr(settings, 'REDIS_ENABLED') else False
        self.default_ttl = 300  # 5분
        
    async def connect(self):
        """Redis 연결"""
        if not self.enabled:
            logger.info("Redis 캐싱이 비활성화되어 있습니다")
            return
            
        try:
            redis_url = settings.REDIS_URL if hasattr(settings, 'REDIS_URL') else "redis://localhost:6379"
            self.redis_client = redis.from_url(
                redis_url,
                encoding="utf-8",
                decode_responses=True
            )
            await self.redis_client.ping()
            logger.info("Redis 연결 성공")
        except (RedisError, ConnectionError) as e:
            logger.warning(f"Redis 연결 실패: {e}. 캐싱 없이 계속 진행합니다.")
            self.enabled = False
            self.redis_client = None
    
    async def disconnect(self):
        """Redis 연결 해제"""
        if self.redis_client:
            await self.redis_client.close()
            logger.info("Redis 연결 해제")
    
    def _generate_cache_key(
        self, 
        prefix: str, 
        params: Dict[str, Any], 
        run_id: Optional[int] = None
    ) -> str:
        """캐시 키 생성"""
        # 파라미터를 정렬하여 일관된 키 생성
        sorted_params = sorted(params.items())
        param_str = json.dumps(sorted_params, sort_keys=True, default=str)
        
        # 해시 생성
        param_hash = hashlib.md5(param_str.encode()).hexdigest()
        
        # run_id 포함
        if run_id:
            return f"bp:{prefix}:{param_hash}:r{run_id}"
        return f"bp:{prefix}:{param_hash}"
    
    async def get(
        self, 
        key: str, 
        params: Optional[Dict[str, Any]] = None,
        run_id: Optional[int] = None
    ) -> Optional[Any]:
        """캐시에서 데이터 조회"""
        if not self.enabled or not self.redis_client:
            return None
        
        try:
            # 전체 키 생성
            if params is not None:
                cache_key = self._generate_cache_key(key, params, run_id)
            else:
                cache_key = key
            
            # Redis에서 조회
            cached_data = await self.redis_client.get(cache_key)
            
            if cached_data:
                logger.debug(f"캐시 히트: {cache_key}")
                return json.loads(cached_data)
            
            logger.debug(f"캐시 미스: {cache_key}")
            return None
            
        except (RedisError, json.JSONDecodeError) as e:
            logger.error(f"캐시 조회 실패: {e}")
            return None
    
    async def set(
        self,
        key: str,
        value: Any,
        params: Optional[Dict[str, Any]] = None,
        run_id: Optional[int] = None,
        ttl: Optional[int] = None
    ) -> bool:
        """캐시에 데이터 저장"""
        if not self.enabled or not self.redis_client:
            return False
        
        try:
            # 전체 키 생성
            if params is not None:
                cache_key = self._generate_cache_key(key, params, run_id)
            else:
                cache_key = key
            
            # JSON 직렬화
            json_value = json.dumps(value, default=str)
            
            # TTL 설정 (기본 5분)
            ttl = ttl or self.default_ttl
            
            # Redis에 저장
            await self.redis_client.setex(
                cache_key,
                ttl,
                json_value
            )
            
            logger.debug(f"캐시 저장: {cache_key} (TTL: {ttl}초)")
            return True
            
        except (RedisError, json.JSONEncodeError) as e:
            logger.error(f"캐시 저장 실패: {e}")
            return False
    
    async def delete(
        self,
        key: str,
        params: Optional[Dict[str, Any]] = None,
        run_id: Optional[int] = None
    ) -> bool:
        """캐시 삭제"""
        if not self.enabled or not self.redis_client:
            return False
        
        try:
            # 전체 키 생성
            if params is not None:
                cache_key = self._generate_cache_key(key, params, run_id)
            else:
                cache_key = key
            
            # Redis에서 삭제
            result = await self.redis_client.delete(cache_key)
            
            if result:
                logger.debug(f"캐시 삭제: {cache_key}")
            
            return bool(result)
            
        except RedisError as e:
            logger.error(f"캐시 삭제 실패: {e}")
            return False
    
    async def delete_pattern(self, pattern: str) -> int:
        """패턴에 맞는 캐시 삭제"""
        if not self.enabled or not self.redis_client:
            return 0
        
        try:
            # 패턴에 맞는 키 조회
            keys = []
            async for key in self.redis_client.scan_iter(match=pattern):
                keys.append(key)
            
            # 키들 삭제
            if keys:
                deleted = await self.redis_client.delete(*keys)
                logger.info(f"캐시 삭제: {pattern} 패턴 {deleted}개 키")
                return deleted
            
            return 0
            
        except RedisError as e:
            logger.error(f"캐시 패턴 삭제 실패: {e}")
            return 0
    
    async def invalidate_run(self, old_run_id: int):
        """특정 run_id의 모든 캐시 무효화"""
        pattern = f"bp:*:r{old_run_id}"
        deleted = await self.delete_pattern(pattern)
        logger.info(f"Run ID {old_run_id} 캐시 무효화: {deleted}개 키 삭제")
        return deleted
    
    def generate_etag(self, data: Any, run_id: Optional[int] = None) -> str:
        """ETag 생성"""
        # 데이터를 JSON 문자열로 변환
        json_str = json.dumps(data, sort_keys=True, default=str)
        
        # run_id 포함
        if run_id:
            json_str = f"{json_str}:{run_id}"
        
        # MD5 해시 생성
        etag = hashlib.md5(json_str.encode()).hexdigest()
        
        return f'W/"{etag}"'  # Weak ETag


# 싱글톤 인스턴스
cache_manager = CacheManager()