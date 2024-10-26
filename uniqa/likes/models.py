from django.db import models
from users.models import CustomUser
from questions.models import Question, Answer

class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True, related_name='likes')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, blank=True, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        target = self.question if self.question else self.answer
        return f"Like by {self.user.display_name} on {target}"

