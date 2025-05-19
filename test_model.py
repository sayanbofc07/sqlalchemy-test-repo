from sqlalchemy import MetaData,Table, Column, Integer, String, Boolean, JSON, create_engine, text, ForeignKey
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
    Column("status", Boolean, nullable=False, default=True),
    Column("json_val", JSON)
)

address_table = Table(
    "address",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user_id", ForeignKey("user.user_id"), nullable=False),
    Column("address", String(255), nullable=True),
 )

# Insert type - 1
with engine.connect() as conn:
    insert_stmt = user.insert().values(
        user_id = 1,
        user_name="bob",
        email_address="bob@example.com",
        nickname="Bobby",
        # status=True  # or 1
    )
    conn.execute(insert_stmt)
    conn.execute(address_table.insert().values(
        id=1,
        user_id=1,
        address="123 Main St"
    ))
    conn.commit()
    print("done")

## Insert type - 2
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

# insert_stmt = user.insert().values(
#         user_id = 4,
#         user_name="sayan 4",
#         email_address="sayan@example.com",
#         nickname="rivu",
#         json_val = [1,2,3]
#         # status=True  # or 1
#     )
# # print(insert_stmt)
# session.execute(insert_stmt)
# session.commit()
# session.close()
# print("done")

## fetch saved data
id_ = 4
result = session.execute(text("SELECT * FROM user WHERE user_id = :id"), {"id": id_})
results = result.mappings().all()
print(results)
# print(user.__dict__)
# print(metadata_obj.__dict__)
# print(metadata_obj.sorted_tables)
# for t in metadata_obj.sorted_tables:
#     print(t)

# print(user.c.user_name)
# print(user.c.keys())
# print(user.primary_key)