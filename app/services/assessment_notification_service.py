from sqlalchemy.orm import Session
from app.models.notification import Notification
from app.services.notification_service import create_notification
from app.services.assessment_service import analyze_patient_symptoms

def notify_assessment_result(db: Session, user_id: int):
    \"\"\"
    Triggers a notification when a medical assessment is completed.
    This function would be called after the assessment logic in assessment_service.
    \"\"\"
    # 1. Run assessment logic to get the result
    result = analyze_patient_symptoms(db, user_id)
    
    # 2. Create a notification based on the risk level
    title = "Kết quả đánh giá bệnh nền"
    if result.risk_level == "Severe":
        message = f"CẢNH BÁO: Kết quả đánh giá cho thấy mức độ rủi ro CAO. Vui lòng liên hệ bác sĩ ngay lập tức. {result.recommendations[0]}"
    elif result.risk_level == "High":
        message = f"Thông báo: Kết quả đánh giá có rủi ro đáng kể. Bạn nên đặt lịch hẹn khám sớm. {result.recommendations[0]}"
    else:
        message = f"Kết quả đánh giá bệnh nền của bạn đã sẵn sàng. Mức độ rủi ro: {result.risk_level}. {result.recommendations[0]}"
        
    from app.schemas.notification import NotificationCreate
    notification_data = NotificationCreate(title=title, message=message)
    
    return create_notification(db, user_id, notification_data)
