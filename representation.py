from mido import MidiFile
import numpy as np
import unittest
import mido

mid = MidiFile("/Users/thijsspinoy/Downloads/AUD_HTX0677.mid")

#print mid.filename


def get_messages(mid):
    for i, track in enumerate(mid.tracks):
        if track.name == "Vocal Guide":
            track.sort(key=lambda message: message.time) # very important to sort!!!
            return track

result = get_messages(mid)
for msg in result:
    print(msg)


def get_onsets(messages):
    """
    From the messages we consider, we take all the messages of type note_on.
    :param messages: all the messages from the Vocal Guide track.
    :return: an array with only the messages with onset information.
    """
    onsets_array = []
    for msg in messages:
        if msg.type == "note_on":
            onsets_array.append(msg)
    for onset in onsets_array:
        onset.time = mido.tick2second(tick=onset.time, ticks_per_beat=mid.ticks_per_beat, tempo=64)
    return onsets_array


def get_pitches(messages):
    """
    From the messages we consider, we take all the messages of type pitch.
    :param messages: all the messages from the Vocal Guide track.
    :return: an array with only the messages with pitch information.
    """
    pitches_array = []
    for msg in messages:
        if msg.type == "pitchwheel":
            pitches_array.append(msg)
    return pitches_array


def ioi(onsets_array):
    """
    :param onsets_array: an array with the onset times.
    :return: a new array with the onset intervals computed by this function.
    """
    res = np.zeros(len(onsets_array)-1)
    for index in range(len(onsets_array)):
        res[index-1] = onsets_array[index].time - onsets_array[index-1].time
    return res


def relative_pitch(pitch_array):
    """
    This function does exactly the same as ioi.
    We compute the interval between every note and its successor.
    :param pitch_array: an array with the pitches
    :return: a new array with the pitch intervals computed by this function
    """
    res = np.zeros(len(pitch_array) - 1)
    for index in range(len(pitch_array)):
        res[index - 1] = pitch_array[index].pitch - pitch_array[index - 1].pitch
    return res


def relative_note(note_array):
    """
    This function does exactly the same as ioi.
    We compute the interval between every note and its successor.
    :param note_array: an array with the pitches
    :return: a new array with the note intervals computed by this function
    """
    res = np.zeros(len(note_array) - 1)
    for index in range(len(note_array)):
        res[index - 1] = note_array[index].note - note_array[index - 1].note
    return res

onsets = get_onsets(result)
pitches = get_pitches(result)
print onsets
print pitches
print ioi(onsets)
print relative_pitch(pitches)
print relative_note(onsets)


#for i, track in enumerate(mid.tracks):
#    print('Track {}: {}'.format(i, track.name))

    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! #
    # !!!!!!!!!!!! DO NOT REMOVE !!!!!!!!!!!!!!! #
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! #
    #track.sort(key=lambda message: message.time) # Sort the information on time: very important
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! #
    # !!!!!!!!!!!! DO NOT REMOVE !!!!!!!!!!!!!!! #
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! #

#    print track
    # for msg in track:
    #    print(msg)


def midifile_to_dict(mid):
    tracks = []
    for track in mid.tracks:
        tracks.append([vars(msg).copy() for msg in track])

    return {
        'ticks_per_beat': mid.ticks_per_beat,
        'tracks': tracks,
    }
#print midifile_to_dict(mid)


class RepresentationTestCase(unittest.TestCase):
    """
    In this class we test the implementation of our methods to retrieve information from music files.
    We check whether we retrieve the result we expect.
    If not, we have to check the implementation to let this tests pass again!
    """
    def test_ioi(self):
        self.assertTrue(np.all(ioi([1, 2, 4, 8])) == np.all([1, 2, 4]))

    #def test_log_ioi(self):
    #    self.assertTrue(np.all(log_ioi([1, 2, 4, 8])) == np.all([0, 1, 2]))

    def test_relative_pitch(self):
        self.assertTrue(np.all(relative_pitch([1, 2, 4, 8])) == np.all([1, 2, 4]))
