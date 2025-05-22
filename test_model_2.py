from sqlalchemy import (
    Integer, String, Text, Boolean, Date, DateTime, Float, Numeric, Time,
    LargeBinary, Enum, JSON, Interval, BigInteger, SmallInteger, Unicode, UnicodeText
)
from sqlalchemy.orm import Mapped, mapped_column, declarative_base
import enum
import datetime
from sqlalchemy import create_engine

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

Base = declarative_base()

class MyEnum(enum.Enum):
    one = "one"
    two = "two"
    three = "three"

class EverythingTable(Base):
    __tablename__ = "everything"

    id: Mapped[int] = mapped_column(primary_key=True)

    # Integer types
    int_col: Mapped[int] = mapped_column(Integer)
    big_int_col: Mapped[int] = mapped_column(BigInteger)
    small_int_col: Mapped[int] = mapped_column(SmallInteger)

    # String types
    str_col: Mapped[str] = mapped_column(String(100))
    text_col: Mapped[str] = mapped_column(Text)
    unicode_col: Mapped[str] = mapped_column(Unicode(100))
    unicode_text_col: Mapped[str] = mapped_column(UnicodeText)

    # Boolean
    bool_col: Mapped[bool] = mapped_column(Boolean)

    # Date/time
    date_col: Mapped[datetime.date] = mapped_column(Date)
    time_col: Mapped[datetime.time] = mapped_column(Time)
    datetime_col: Mapped[datetime.datetime] = mapped_column(DateTime)
    interval_col: Mapped[datetime.timedelta] = mapped_column(Interval)

    # Float/Decimal
    float_col: Mapped[float] = mapped_column(Float)
    numeric_col: Mapped[float] = mapped_column(Numeric(10, 2))

    # Binary
    binary_col: Mapped[bytes] = mapped_column(LargeBinary)

    # JSON
    json_col: Mapped[dict] = mapped_column(JSON)

    # Enum
    enum_col: Mapped[MyEnum] = mapped_column(Enum(MyEnum))

    def __repr__(self):
        return f"<EverythingTable id={self.id}>"

Base.metadata.create_all(engine)