import wave
import pyaudio
import os


def concatenate_sounds(sounds, output_name):
    output = wave.open(output_name, 'wb')
    output.setparams(sounds[0][0])

    for sound in sounds:
        output.writeframes(sound[1])

    output.close()


def load_sounds(sound_names):
    files = []
    for name in sound_names:
        sound = wave.open(name, 'rb')
        files.append([sound.getparams(), sound.readframes(sound.getnframes())])
    return files


def play_sound(filename):
    chunk = 1024
    sound = wave.open(filename)
    player = pyaudio.PyAudio()
    stream = player.open(
        format=player.get_format_from_width(sound.getsampwidth()),
        channels=sound.getnchannels(),
        rate=sound.getframerate(),
        output=True
    )
    data = sound.readframes(chunk)

    while data:
        stream.write(data)
        data = sound.readframes(chunk)

    stream.stop_stream()
    stream.close()

    player.terminate()


def parse_below_1000(number):
    result = []
    first_digit = number % 1000 // 100
    if first_digit > 0:
        result.append(first_digit * 100)  # hundreds

    second_digit = number % 100 // 10

    if second_digit >= 2:
        result.append(second_digit * 10)
    elif second_digit == 1:
        result.append(number % 100)  # teens
        return result

    third_digit = number % 10
    if third_digit > 0:
        result.append(third_digit)

    return result


def detect_thousand_separator(number):
    low_part = number % 10
    high_part = number % 100 // 10

    if low_part >= 5 or high_part == 1:
        return 'tysyach'

    if low_part == 0:
        return 'tysyach'

    elif low_part == 1:
        return 'tysyacha'
    else:
        return 'tysyachi'


def parse_number(number):
    first_part = number // 1000
    result = []
    if first_part > 0:
        result += parse_below_1000(first_part)
        result.append(detect_thousand_separator(first_part))
    second_part = number % 1000
    if second_part > 0:  # if for 1000, 2000, 3000 and so on
        result += parse_below_1000(second_part)
    print(result)
    return result


def test_parse():
    assert parse_number(321) == [300, 20, 1]
    assert parse_number(109) == [100, 9]
    assert parse_number(15) == [15]
    assert parse_number(1000) == [1, 'tysyacha']
    assert parse_number(2000) == [2, 'tysyachi']
    assert parse_number(5000) == [5, 'tysyach']
    assert parse_number(11234) == [11, 'tysyach', 200, 30, 4]
    print()


def token_to_path(token, modified):
    string_token = str(token)
    if len(string_token) == 1:  # need for 01.wav
        string_token = '0' + string_token  # no append for 1.wav in result

    if token == 1 and modified:
        string_token = 'odna'

    if token == 2 and modified:
        string_token = 'dve'
    path = 'sounds/' + str(string_token) + '.wav'
    return path


def number_to_paths(number):
    tokens = parse_number(number)
    paths = []

    for index, token in enumerate(tokens):
        modified = False
        if index + 1 < len(tokens) and \
                isinstance(tokens[index + 1], str) and \
                tokens[index + 1].startswith('tysya') \
                and (token == 1 or token == 2):
            modified = True

        paths.append(token_to_path(token, modified))
    return paths


def do_you_want_to_continue():
    got_result = False

    while not got_result:
        value = input('Do you want to continue [y/n]: ')
        if value not in ['y', 'n']:
            print('Enter y or n')
            continue
        got_result = True
        if value == 'y':
            return True
        else:
            return False


def run_interface():
    is_played = True

    while is_played:
        input_number = int(input('Write the number: '))

        names = number_to_paths(input_number)

        sounds = load_sounds(names)

        saved_path = 'output/' + str(input_number) + '.wav'
        concatenate_sounds(sounds, saved_path)
        play_sound(saved_path)

        is_played = do_you_want_to_continue()


if __name__ == '__main__':
    test_parse()
    run_interface()

# os.system("321.wav")
