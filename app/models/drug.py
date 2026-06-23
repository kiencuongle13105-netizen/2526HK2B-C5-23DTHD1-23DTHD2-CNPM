from sqlalchemy import Column, Integer, String, Text
from app.core.database import Base

class Drug(Base):
    __tablename__ = "drugs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    generic_name = Column(String, index=True) # Thành phần hoạt chất
    category = Column(String) # Nhóm thuốc (ví dụ: Giảm đau, Kháng sinh)
    description = Column(Text)
    indications = Column(Text) # Chỉ định
    contraindications = Column(Text) # Chống chỉ định
    side_effects = Column(Text) # Tác dụng phụ
