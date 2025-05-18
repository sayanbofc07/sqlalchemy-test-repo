from sqlalchemy import create_engine, text

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

with engine.connect() as connection:
    result = connection.execute(text("SELECT * FROM users LIMIT 1"))
    row = result.fetchone()
    print(row)