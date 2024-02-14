from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def all_words(request):
    return HttpResponse("All words")


def specific_word(request, word_id):
    return HttpResponse("Word %s" % word_id)
