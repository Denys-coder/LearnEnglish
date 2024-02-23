import copy
import random

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from lessons.models import Lesson, Question
from users.score_utils import update_score


# Create your views here.

@login_required(login_url='/login')
def all_lessons(request):
    all_lessons = Lesson.objects.all()
    return render(request, 'all_lessons.html', {'all_lessons': all_lessons})


class LessonView(View):

    def get(self, request, lesson_id):
        if not request.user.is_authenticated:
            return redirect('/login')
        lesson = Lesson.objects.get(pk=lesson_id)
        questions = Question.objects.filter(lesson=lesson).all()
        adjusted_questions = []
        for question in questions:
            current_question = {"question": question.question, "id": question.id}
            all_answers = [question.correct_answer] + question.wrong_answer.split('|')
            random.shuffle(all_answers)
            current_question['answers'] = all_answers
            adjusted_questions.append(copy.deepcopy(current_question))
        lesson_context = {'lesson': lesson, 'questions': adjusted_questions}
        return render(request, 'lesson.html', lesson_context)

    def post(self, request, lesson_id):
        if not request.user.is_authenticated:
            return redirect('/login')
        lesson = Lesson.objects.get(pk=lesson_id)
        questions = Question.objects.filter(lesson=lesson)
        results = []
        result_score = 0
        total_questions = len(questions)
        correct_answers = 0
        for question in questions:
            is_correct = True if request.POST[f'question_{question.id}'] == question.correct_answer else False
            if is_correct:
                correct_answers += 1
            result_text = f"{question.question}, your answer is: {request.POST[f'question_{question.id}']}, the correct answer is: {question.correct_answer}; {is_correct}"
            results.append(result_text)
        result_score = int(correct_answers / total_questions * 100)
        update_score(request.user.username, result_score, lesson_id)
        return render(request, 'lesson_answers.html', {"results": results, "lessons_score": result_score})
