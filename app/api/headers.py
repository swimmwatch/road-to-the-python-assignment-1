from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key")
