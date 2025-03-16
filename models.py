class Track(models.Model):
    # существующий код...
    
    def duration_formatted(self):
        """Возвращает длительность в формате мм:сс"""
        if not self.duration:
            return "0:00"
        
        minutes = self.duration // 60
        seconds = self.duration % 60
        return f"{minutes}:{seconds:02d}" 