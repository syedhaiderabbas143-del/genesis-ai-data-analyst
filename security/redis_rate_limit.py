"""Distributed rate limiter with Redis when configured; safe in-memory fallback for local development."""
import os, time
try:
    import redis
except ImportError: redis=None
class DistributedLimiter:
    def __init__(self, limit=60, window=60):
        self.limit=limit; self.window=window; self.local={}; self.r=None
        url=os.getenv('REDIS_URL')
        if url and redis:
            self.r=redis.from_url(url,decode_responses=True)
    def check(self,key):
        bucket=int(time.time()//self.window); k=f'genesis:rl:{key}:{bucket}'
        if self.r:
            n=self.r.incr(k)
            if n==1: self.r.expire(k,self.window+1)
        else:
            now=time.time(); item=self.local.get(k,[0,now]); item[0]+=1; self.local[k]=item; n=item[0]
            for old in list(self.local):
                if old != k and old.startswith(f'genesis:rl:{key}:') and now-self.local[old][1]>self.window: self.local.pop(old,None)
        if n>self.limit: raise RuntimeError('rate_limit_exceeded')
