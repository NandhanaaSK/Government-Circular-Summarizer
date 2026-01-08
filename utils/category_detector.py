def detect_category(text):
    text = text.lower()

    if any(word in text for word in [
        "school", "college", "exam", "student", "education", "teacher"
    ]):
        return "🎓 Education"

    if any(word in text for word in [
        "hospital", "health", "medical", "doctor", "covid", "vaccine"
    ]):
        return "🏥 Health"

    if any(word in text for word in [
        "finance", "budget", "tax", "salary", "fund", "allowance"
    ]):
        return "💰 Finance"

    if any(word in text for word in [
        "law", "act", "court", "legal", "regulation", "rule"
    ]):
        return "⚖️ Legal / Administrative"

    return "📄 General"
