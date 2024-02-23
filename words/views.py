from django.contrib.auth.models import User
from django.shortcuts import render, redirect
import random
from django.views import View

from users.score_utils import update_score
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


def get_next_word(username):
    # get next random word
    current_user = User.objects.get(usrename=username)
    all_user_words = UserDict.objects.filter(user=current_user).all()
    random_word = random.choice(all_user_words)
    random_id = random_word.id
    return random_id


def word(request, word_id):
    if not request.user.is_authenticated:
        return redirect('/login')
    message = None
    if request.method == 'POST':
        # test user answer
        test_word_id = request.POST.get('word_id')
        test_translation = request.POST.get('translate')
        test_word_in_db = UserDict.objects.get(pk=test_word_id)
        if test_word_in_db.translation == test_translation:
            message = f'You are correct. Answer for {test_word_in_db.word} is {test_translation}'
            update_score(request.user.username, 1)
        else:
            message = f'You are wrong. Answer for {test_word_in_db.word} is {test_translation}. Should be {test_word_in_db.translation}'
            update_score(request.user.username, -1)

    next_word_id = get_next_word(request.user.username)

    # get current word
    current_word = UserDict.objects.get(pk=word_id)

    return render(request, 'word.html', {'word': current_word, 'random_id': random_id, 'message': message})


def random_word(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    next_word_id = get_next_word(request.user.username)
    return redirect("/words/" + str(next_word_id))
