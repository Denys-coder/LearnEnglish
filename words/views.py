from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from words.forms import PartialWordForm
from words.models import UserDict


class Words(View):
    def get(self, request):

        if not request.user.is_authenticated:
            return redirect('/login')

        current_user = User.objects.get(username=request.user.username)
        all_words = UserDict.objects.filter(user=current_user)
        article_form = PartialWordForm()
        return render(request, 'user-dict.html', {'all_words': all_words, 'article_form': article_form})

    def post(self, request):

        if not request.user.is_authenticated:
            return redirect('/login')

        current_user = User.objects.get(username=request.user.username)

        new_word = UserDict(user=current_user)
        word_form = PartialWordForm(request.POST, instance=new_word)
        if word_form.is_valid():
            word_form.save()

        all_words = UserDict.objects.filter(user=current_user)
        article_form = PartialWordForm()
        return render(request, 'user-dict.html', {'all_words': all_words, 'article_form': article_form})


# Create your views here.

def specific_word(request, word_id):
    return HttpResponse("Word %s" % word_id)
