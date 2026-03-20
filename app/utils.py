def format_percentage(value):
    if value is None:
        return 'N/A'
    return f"{value * 100:.1f}%"
