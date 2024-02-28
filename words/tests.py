import re

from django.contrib.auth.models import User
from django.test import TestCase, Client

from words.models import UserDict


class WordsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testusername', email='<EMAIL>', password='<PASSWORD>')
        self.user.save()

    def test_words(self):
        c = Client()
        c.login(username='testusername', password='<PASSWORD>')
        response = c.post('/words/', {'word': 'word1', 'translation': 'translation1',
                                      'transcription': 'transcription1', 'transliteration': 'transliteration1',
                                      'audio': 'audio1'})
        self.assertEqual(response.status_code, 200)
        saved_words = UserDict.objects.filter(word='word1').first()
        self.assertEqual(saved_words.word, 'word1')
        self.assertEqual(saved_words.translation, 'translation1')
        self.assertEqual(saved_words.transcription, 'transcription1')
        self.assertEqual(saved_words.transliteration, 'transliteration1')

        response = c.post('/words/', {'word': 'word2', 'translation': 'translation2',
                                      'transcription': 'transcription2', 'transliteration': 'transliteration2',
                                      'audio': 'audio2'})
        self.assertEqual(response.status_code, 200)
        saved_words = UserDict.objects.filter(user=self.user).all()
        self.assertEqual(len(saved_words), 2)
        self.assertEqual(saved_words[0].user, self.user)
        self.assertEqual(saved_words[1].user, self.user)

        saved_words = UserDict.objects.filter(word='word2').first()
        self.assertEqual(saved_words.word, 'word2')
        self.assertEqual(saved_words.translation, 'translation2')
        self.assertEqual(saved_words.transcription, 'transcription2')
        self.assertEqual(saved_words.transliteration, 'transliteration2')
        self.assertEqual(saved_words.user, self.user)

    def test_words_get(self):
        c = Client()
        c.login(username='testusername', password='<PASSWORD>')
        response = c.get('/words/')
        self.assertEqual(response.status_code, 200)


class RandomWordsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testusername', email='<EMAIL>', password='<PASSWORD>')
        self.user.save()
        self.word1 = UserDict(word='word1', translation='translation1',
                              transcription='transcription1', transliteration='transliteration1',
                              audio='audio1', user=self.user)
        self.word2 = UserDict(word='word2', translation='translation2',
                              transcription='transcription2', transliteration='transliteration2',
                              audio='audio2', user=self.user)
        self.word1.save()
        self.word2.save()

    def test_random_words(self):
        c = Client()
        c.login(username='test/username', password='<PASSWORD>')
        for i in range(100):
            response = c.get('/words/random/', follow=True)
            self.assertEqual(response.status_code, 200)
            r_chain = response.redirect_chain
            redirect_path, redirect_code = r_chain[0]
            words_ids = [str(self.word1.id), str(self.word2.id)]
            cleared_path = redirect_path.replace('/words/', '')
            self.assertIn(cleared_path, words_ids)


class CheckAnswersTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testusername', email='<EMAIL>', password='<PASSWORD>')
        self.user.save()
        self.word1 = UserDict(word='word1', translation='translation1',
                              transcription='transcription1', transliteration='transliteration1',
                              audio='audio1', user=self.user)
        self.word2 = UserDict(word='word2', translation='translation2',
                              transcription='transcription2', transliteration='transliteration2', audio='audio2',
                              user=self.user)
        self.word1.save()
        self.word2.save()

    def test_answer_check(self):
        c = Client()
        c.login(username='testusername', password='<PASSWORD>')
        response = c.post(f'/words/{self.word1.id}/', {'word_id': str(self.word1.id), 'translate': 'word1'},
                          follow=True)
        self.assertEqual(response.status_code, 200)
        html_data = str(response.content)
        results = re.findall(r'form action="/words/\d+/" method="post">', html_data)
        form_string = results[0]
        form_string = form_string.replace('form action="/words/', '')
        form_string = form_string.replace('/" method="post">', '')
        self.assertEquals(form_string, str(self.word2.id))
