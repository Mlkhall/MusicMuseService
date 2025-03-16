from django import template

register = template.Library()

@register.filter
def format_duration(seconds):
    """
    Форматирует длительность в секундах в формат мм:сс
    """
    if seconds is None:
        return "0:00"
    
    # Преобразование в целое число
    try:
        seconds = int(seconds)
    except (ValueError, TypeError):
        return "0:00"
    
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    return f"{minutes}:{remaining_seconds:02d}" 