import json
from sqlalchemy.orm import Session
from app.models.drug import Drug
from app.core.database import SessionLocal

def import_medical_data(file_path: str):
    db = SessionLocal()
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        count = 0
        for item in data:
            # Check if drug already exists
            exists = db.query(Drug).filter(Drug.name == item["ten_thuoc"]).first()
            if not exists:
                new_drug = Drug(
                    name=item["ten_thuoc"],
                    generic_name=item["nhom_thuoc"], # Using group as generic for this dataset
                    category=item["nhom_benh"],
                    description=item["doi_tuong_thich_hop"],
                    indications=", ".join(item["benh_nen_chi_dinh"]),
                    contraindications=item["chong_chi_dinh"],
                    side_effects="Not specified in dataset"
                )
                db.add(new_drug)
                count += 1
        
        db.commit()
        print(f"Successfully imported {count} new drugs from {file_path}")
    except Exception as e:
        print(f"Error importing data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        import_medical_data(sys.argv[1])
    else:
        print("Please provide the path to the JSON file.")
