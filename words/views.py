from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from words.models import UserDict


class Words(View):
    def get(self, request):

        if not request.user.is_authenticated:
            return redirect('/login')

        current_user = User.objects.get(username=request.user.username)
        all_words = UserDict.objects.filter(user=current_user)
        return render(request, 'user-dict.html', {'all_words': all_words})

    def post(self, request):

        if not request.user.is_authenticated:
            return redirect('/login')

        current_user = User.objects.get(username=request.user.username)
        word = request.POST.get("word")
        translation = request.POST.get("translation")
        transcription = request.POST.get("transcription")
        transliteration = request.POST.get("transliteration")
        db_word = UserDict(user=current_user, word=word, translation=translation, transcription=transcription,
                           transliteration=transliteration)
        db_word.save()

        all_words = UserDict.objects.filter(user=current_user)
        return render(request, 'user-dict.html', {'all_words': all_words})


# Create your views here.

def specific_word(request, word_id):
    return HttpResponse("Word %s" % word_id)
