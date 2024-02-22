import copy
import random

from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from lessons.models import Lesson, Question


# Create your views here.

def all_lessons(request):
    all_lessons = Lesson.objects.all()
    return render(request, 'all_lessons.html', {'all_lessons': all_lessons})


class LessonView(View):
    def get(self, request, lesson_id):
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
        lesson = Lesson.objects.get(pk=lesson_id)
        questions = Question.objects.filter(lesson=lesson)
        results = []
        for question in questions:
            is_correct = True if request.POST[f'question_{question.id}'] == question.correct_answer else False
            result_text = f"{question.question}, your answer is: {request.POST[f'question_{question.id}']}, the correct answer is: {question.correct_answer}"
            results.append(result_text)
        return render(request, 'lesson_answers.html', {"results": results})