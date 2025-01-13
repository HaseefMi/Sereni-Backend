from rest_framework.throttling import SimpleRateThrottle

class Throttle_1_Sec(SimpleRateThrottle):
    scope = 'throttle_1/sec'
    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            return self.cache_format.format(user=request.user.id)
        return self.cache_format.format(ip=request.META.get('REMOTE_ADDR'))

class Throttle_100_Sec(SimpleRateThrottle):
    scope = 'throttle_100/sec'
    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            return self.cache_format.format(user=request.user.id)
        return self.cache_format.format(ip=request.META.get('REMOTE_ADDR'))
