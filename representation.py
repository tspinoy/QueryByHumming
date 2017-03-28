import unittest

import librosa
import numpy as np

#y, sr = librosa.load(librosa.util.example_audio_file())
#onset_frames = librosa.onset.onset_detect(y=y, sr=sr)
#print onset_frames
#result = librosa.frames_to_time(onset_frames[:20], sr=sr)
#print result


def load_file(music):
    """
    :param music: a music file of any format
    :return: tuple (y, sr) ; y = an array with the audio time series & sr = sample rate
    """
    return librosa.load(music)


def get_frequencies(music):
    """
    Retrieve the frequencies of a music file
    :param music: a music file of any format
    :return: an array with the frequencies of the audio in the file
    """
    y, sr = load_file(music)
    frequencies = librosa.core.fft_frequencies(sr=sr, n_fft=5)
    print frequencies
    return frequencies


def convert_frequencies_to_midi(frequencies_array):
    midi = librosa.core.hz_to_midi(frequencies_array)
    return midi


def convert_frequencies_to_notes(frequencies_array):
    """
    Retrieve the notes with given frequencies
    :param frequencies_array: the frequencies of an audio file
    :return: the notes corresponding to the frequencies
    """
    notes = librosa.core.hz_to_note(frequencies_array)
    return notes


def convert_music_to_midi(music):
    return convert_frequencies_to_midi(get_frequencies(music))


def get_pitches(music):
    """
    Retrieve the pitches from a music file
    :param music: a music file of any format
    :return: an array with the pitches
    """
    y, sr = load_file(music)
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
    return pitches


#print convert_music_to_midi(librosa.util.example_audio_file())
#print convert_frequencies_to_notes(get_frequencies(librosa.util.example_audio_file()))
#print librosa.cqt_frequencies(128, fmin=librosa.note_to_hz('C2'))
#print get_pitches(librosa.util.example_audio_file())


def get_onset_times(music):
    """
    :param music: a music file.
    :return: an array with the onset times.
    """
    y, sr = load_file(music)
    onset_frames = librosa.onset.onset_detect(y=y, sr=sr)
    onsets = librosa.frames_to_time(onset_frames, sr=sr)
    return onsets


def ioi(onsets_array):
    """
    :param onsets_array: an array with the onset times.
    :return: a new array with the onset intervals computed by this function.
    """
    res = np.zeros(len(onsets_array)-1)

    for i in range(len(onsets_array)):
        res[i-1] = onsets_array[i] - onsets_array[i-1]

    return res


def log_ioi(onsets_array):
    """
    :param onsets_array: an array with the onset times.
    :return: a new array with the logarithm of the onset intervals computed by this function.
    """
    res = np.zeros(len(onsets_array)-1)

    for i in range(len(onsets_array)):
        res[i-1] = np.log2(onsets_array[i] - onsets_array[i-1])

    return res


def relative_pitch(pitch_array):
    """
    This function does exactly the same as ioi.
    We compute the interval between every note and its successor.
    :param pitch_array: an array with the pitches
    :return: a new array with the pitch intervals computed by this function
    """
    return ioi(pitch_array)

print ioi(get_onset_times(librosa.util.example_audio_file()))


class RepresentationTestCase(unittest.TestCase):
    """
    In this class we test the implementation of our methods to retrieve information from music files.
    We check whether we retrieve the result we expect.
    If not, we have to check the implementation to let this tests pass again!
    """
    def test_ioi(self):
        self.assertTrue(np.all(ioi([1, 2, 4, 8])) == np.all([1, 2, 4]))

    def test_log_ioi(self):
        self.assertTrue(np.all(log_ioi([1, 2, 4, 8])) == np.all([0, 1, 2]))

    def test_relative_pitch(self):
        self.assertTrue(np.all(relative_pitch([1, 2, 4, 8])) == np.all([1, 2, 4]))
