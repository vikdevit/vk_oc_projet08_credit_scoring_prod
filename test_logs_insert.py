from app.database.session import SessionLocal

from app.models.api_log import ApiLog
from app.models.system_health_log import SystemHealthLog


db = SessionLocal()


# Test API log

api_log = ApiLog(
    endpoint="/predict",
    status_code=200,
    response_time=125.5
)


db.add(api_log)


# Test santé serveur

health_log = SystemHealthLog(
    cpu_usage=0.5,
    memory_usage=3.0,
    response_time=125.5
)


db.add(health_log)


db.commit()


db.close()


print("Logs insérés dans Neon")
