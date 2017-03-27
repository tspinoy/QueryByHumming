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
    :return: typle (y, sr) ; y = an array with the audio time series & sr = sample rate
    """
    return librosa.load(music)


def get_frequencies(music):
    y, sr = load_file(music)
    frequencies = librosa.core.fft_frequencies(sr=sr, n_fft=5)
    print frequencies
    return frequencies


def convert_frequencies_to_midi(frequencies_array):
    midi = librosa.core.hz_to_midi(frequencies_array)
    return midi


def convert_frequencies_to_notes(frequencies_array):
    midi = librosa.core.hz_to_note(frequencies_array)
    return midi


def convert_music_to_midi(music):
    return convert_frequencies_to_midi(get_frequencies(music))

print convert_music_to_midi(librosa.util.example_audio_file())
#print convert_frequencies_to_notes(get_frequencies(librosa.util.example_audio_file()))


def get_onset_times(music):
    """
    :param music: a music file.
    :return: an array with the onset times.
    """
    y, sr = load_file(music)
    onsets = librosa.onset.onset_detect(y=y, sr=sr)
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

#print ioi(result)
#print log_ioi(result)

#pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
#print pitches
#print magnitudes

#print pitches[1]


#print(log_ioi([1, 2, 4, 8]))
#print np.log(1)
#print np.log(8)
#print np.log(10)


class RepresentationTestCase(unittest.TestCase):
    def test_ioi(self):
        self.assertTrue(np.all(ioi([1, 2, 4, 8])) == np.all([1, 2, 4]))

    def test_log_ioi(self):
        self.assertTrue(np.all(log_ioi([1, 2, 4, 8])) == np.all([0, 1, 2]))
