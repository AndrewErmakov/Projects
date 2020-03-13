import wikipedia
import subprocess
import speech_recognition as sr
# import wikipedia.exceptions.DisambiguationError
# import pyaudio
import random
import sys
import subprocess


def speak_text(text):
    espeak = subprocess.Popen(['espeak-ng', '-v', 'ru'], stdin=subprocess.PIPE)
    espeak.stdin.write(text.encode())
    espeak.communicate()
    espeak.stdin.close()


def search_word(text):
    available_choices = wikipedia.search(query)

    return available_choices


def choose_option(available_choices):
    print('Список вариантов')
    # speak_text('Список вариантов')
    for index, option in enumerate(available_choices):
        print('{}. {}'.format(index + 1, option))
        # speak_text('{}. {}'.format(index + 1, option))

    is_chosen = False
    chosen_value = None

    while not is_chosen:
        message = 'Выбран вариант: %s '
        value = random.randint(1, len(available_choices))
        # value = 1
        print(message % value)
        speak_text(message % value)
        try:
            value = int(value)
        except ValueError:
            print('Your option is not a number')

        if value > len(available_choices) or value <= 0:
            print('Press option from 1 to {}'.format(len(available_choices)))
        is_chosen = True
        chosen_value = value - 1

    return available_choices[chosen_value]


def recognize():
    r = sr.Recognizer()
    # print(sr.Microphone.list_microphone_names())
    mic = sr.Microphone(device_index=0)
    number_uncertainties = 0
    print('Speak:')
    speak_text('Говорите:')
    have_listened = False
    while not have_listened:
        try:
            with mic as source:
                r.adjust_for_ambient_noise(source)
                print('Start listening')
                audio = r.listen(source)
                print('End of listening')
            output = r.recognize_google(audio, language="RU-ru")
            have_listened = True
        except sr.UnknownValueError:
            print('Your speech is not recognized. try again')
            speak_text('Ваша речь не распознана. Попробуйте еще раз')
            number_uncertainties += 1
            if number_uncertainties > 2:
                speak_text('Я устал вас распознавать. До свидания')
                return 'выход'

    print(output)

    return output


def read_option():
    while True:
        value = input('Keyboard or voice input [k/v]:')
        if value == 'k':
            query = input('Enter the word:')
            break
        elif value == 'v':
            print('Voice')
            query = recognize()  # голосом
            break
        else:
            print('Enter k or v')
            continue

    return query


def wikipedia_search(query):
    is_completed = False
    current_query = query
    available_choices = search_word(current_query)
    if len(available_choices) == 0:
        speak_text('Ничего не найдено')
        new_query = recognize()
        return new_query
    while not is_completed:
        found_query = choose_option(available_choices)
        try:
            text_page = wikipedia.summary(found_query, sentences=2)
            is_completed = True
        except wikipedia.exceptions.DisambiguationError as e:
            print('Disambiguation')
            available_choices = e.options

    return text_page


if __name__ == '__main__':
    wikipedia.set_lang('ru')

    while True:
        # query = input('Введите слово:')
        query = read_option()

        if query.lower() == 'выход':
            break
            exit

        text = wikipedia_search(query)
        if text == 'fail':
            break
        print(text)
        speak_text(text)
