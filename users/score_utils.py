from django.contrib.auth.models import User

from lessons.models import Lesson
from users.models import Score, UserProgress


def update_score(username, score, lesson_id=None):
    user_obj = User.objects.get(username=username)
    user_score = Score.objects.filter(user=user_obj).first()
    if lesson_id is None:
        user_score = Score.objects.get(user=user_obj)

    if lesson_id is not None:
        lesson = Lesson.objects.get(pk=lesson_id)
        user_progress = UserProgress.objects.filter(user=user_obj, lesson=lesson).first()
        if user_progress is None:
            user_progress = UserProgress(user=user_obj, score=0, lesson=lesson)
        else:
            user_score = Score.objects.get(user=user_obj)
            user_score.score -= user_progress.score
            user_score.save()
        user_progress.score = score
        user_progress.save()
    user_score.score += score
    user_score.save()
