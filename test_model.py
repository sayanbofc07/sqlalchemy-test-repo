from sqlalchemy import MetaData,Table, Column, Integer, String, Boolean, create_engine, text
from sqlalchemy.orm import sessionmaker

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
metadata_obj = MetaData()

user = Table(
    "user",
    metadata_obj,
    Column("user_id", Integer, primary_key=True),
    Column("user_name", String(16), nullable=False),
    Column("email_address", String(60)),
    Column("nickname", String(50), nullable=False),
    Column("status", Boolean, nullable=False, default=True)
)

## Insert type - 1
# with engine.connect() as conn:
#     insert_stmt = user.insert().values(
#         user_id = 2,
#         user_name="bob",
#         email_address="bob@example.com",
#         nickname="Bobby",
#         # status=True  # or 1
#     )
#     conn.execute(insert_stmt)
#     conn.commit()
#     print("done")

## Insert type - 2
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

insert_stmt = user.insert().values(
        user_id = 3,
        user_name="sayan",
        email_address="sayan@example.com",
        nickname="rivu",
        # status=True  # or 1
    )
# print(insert_stmt)
session.execute(insert_stmt)
session.commit()
session.close()
print("done")

# print(user.__dict__)
# print(metadata_obj.__dict__)
# print(metadata_obj.sorted_tables)
# for t in metadata_obj.sorted_tables:
#     print(t)

# print(user.c.user_name)
# print(user.c.keys())
# print(user.primary_key)