from models import Performance, Syllabus

def generate_study_plan(user_id):
    syllabus = Syllabus.query.all()
    performance = Performance.query.filter_by(user_id=user_id).all()
    
    # Simple logic: prioritize weak topics
    plan = []
    for topic in syllabus:
        score = next((p.score for p in performance if p.topic == topic.topic), None)
        if score is None or score < 50:
            plan.append(f"Focus on {topic.topic} today")
        else:
            plan.append(f"Review {topic.topic}")
    return plan
