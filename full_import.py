
import json
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
class Drug(Base):
    __tablename__ = "drugs"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    generic_name = Column(String, index=True)
    category = Column(String)
    description = Column(Text)
    indications = Column(Text)
    contraindications = Column(Text)
    side_effects = Column(Text)

SQLALCHEMY_DATABASE_URL = "sqlite:///C:/Users/HP/Downloads/CNPM/2526HK2B-C5-23DTHD1-23DTHD2-CNPM/Backend/sql_app.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def import_data():
    db = SessionLocal()
    try:
        with open("C:/Users/HP/Downloads/medical_demo_100.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
        count = 0
        for item in data:
            exists = db.query(Drug).filter(Drug.name == item["ten_thuoc"]).first()
            if not exists:
                new_drug = Drug(
                    name=item["ten_thuoc"],
                    generic_name=item["nhom_thuoc"],
                    category=item["nhom_benh"],
                    description=item["doi_tuong_thich_hop"],
                    indications=", ".join(item["benh_nen_chi_dinh"]),
                    contraindications=item["chong_chi_dinh"],
                    side_effects="Not specified in dataset"
                )
                db.add(new_drug)
                count += 1
        db.commit()
        return f"Successfully imported {count} drugs"
    except Exception as e:
        return f"Error: {e}"
    finally:
        db.close()

print(import_data())
