import hashlib

from .models import URLMap


class URLShortenerService:
    def generate_hash(self, url: str, counter: int = 0) -> str:
        hash_input = f"{url}{counter}"
        hash_hex = hashlib.sha256(hash_input.encode()).hexdigest()
        base_hash = hash_hex[:6]
        return f"{base_hash}{counter if counter else ''}"

    def create(self, original_url: str) -> URLMap:
        counter = 0
        while True:
            hash_value = self.generate_hash(original_url, counter)
            if not URLMap.objects.filter(hash=hash_value).exists():
                return URLMap.objects.create(original_url=original_url, hash=hash_value)
            counter += 1

    def get(self, hash_value: str) -> URLMap | None:
        return URLMap.objects.filter(hash=hash_value).first()

    def delete(self, hash_value: str) -> bool:
        url_map = self.get(hash_value)
        if url_map:
            url_map.delete()
            return True
        return False
