from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import uuid

def get_windows_host_ip():
    try:
        with open("/etc/resolv.conf") as f:
            for line in f:
                if "nameserver" in line:
                    return line.strip().split()[1]
    except Exception as e:
        raise RuntimeError(f"Could not determine Windows host IP: {e}")

windows_ip = get_windows_host_ip()
db_user = "wsl_user"
db_pass = "Ams_12345"
db_name = "test_db"

engine = create_engine(f"mysql+pymysql://{db_user}:{db_pass}@{windows_ip}:3306/{db_name}")
# id_ = "06e06d09-9c41-44b6-bb07-611646817c9e"
id_ = "1' OR '1'='1" ## sql injection
name = "zuu"

## for core
with engine.connect() as connection:
    # result = result = connection.execute(text(f"SELECT * FROM users where id = '{id_}'"))
    result = connection.execute(text("SELECT * FROM users WHERE id = :id and name = :name"), {"id": id_, "name":name})
    results = result.mappings().all()
    if not results:
        connection.execute(
            text("INSERT INTO users (id, name, email) VALUES (:id, :name, :email)"),
            [{"id": str(uuid.uuid4()), "name": 'abc3', "email": "test@abc.com"}, {"id": str(uuid.uuid4()), "name": 'abc4', "email": "test2@abc.com"}],
        )
        connection.commit()
        print("data inserted...")

## for orm
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

result = session.execute(text("SELECT * FROM users WHERE id = :id and name = :name"), {"id": id_, "name":name})
results = result.mappings().all()

session.execute(
            text("INSERT INTO users (id, name, email) VALUES (:id, :name, :email)"),
            [{"id": str(uuid.uuid4()), "name": 'abc7', "email": "test@abc.com"}, {"id": str(uuid.uuid4()), "name": 'abc8', "email": "test2@abc.com"}],
        )
session.commit()
session.close()
print("data inserted...")