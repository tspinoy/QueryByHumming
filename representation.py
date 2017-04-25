from mido import MidiFile
import numpy as np
import unittest
import mido

mid = MidiFile("/Users/thijsspinoy/Downloads/AUD_HTX0677.mid")
# print mid
# for i, track in enumerate(mid.tracks):
#    for msg in track:
#        print(msg)


# -------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------- Get information -------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
def get_messages(midi_file):
    """
    We only consider messages from the track Vocal Guide because this is the track where people's voice is stored.
    :param midi_file: a loaded midi-file.
    :return: a sorted list of messages from the Vocal Guide.
    """
    for i, track in enumerate(midi_file.tracks):
        if track.name == "Vocal Guide":
            track.sort(key=lambda message: message.time)  # very important to sort!!!
            return track

# result = get_messages(mid)
# for msg in result:
#     print(msg)


def get_onset_and_note_messages(midi_file):
    """
    From the messages we consider, we take all the messages of type note_on.
    :param midi_file: all the messages from the Vocal Guide track.
    :return: an array with only the messages with onset information.
    """
    messages = get_messages(midi_file)
    onsets_array = []
    for msg in messages:
        if msg.type == "note_on":
            onsets_array.append(msg)
    # for onset in onsets_array:
    #     onset.time = mido.tick2second(tick=onset.time, ticks_per_beat=mid.ticks_per_beat, tempo=64)
    return onsets_array


# -------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------- Measurements --------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
def ioi(messages_array):
    """
    :param messages_array: an array with the onset times.
    :return: a new array with the onset intervals computed by this function.
    """
    res = np.zeros(len(messages_array)-1)
    for index in range(len(messages_array)):
        res[index-1] = messages_array[index].time - messages_array[index-1].time
    return res


def relative_note(messages_array):
    """
    This function does exactly the same as ioi.
    We compute the interval between every note and its successor.
    :param messages_array: an array with the pitches
    :return: a new array with the note intervals computed by this function
    """
    res = np.zeros(len(messages_array)-1)
    for index in range(len(messages_array)):
        res[index-1] = messages_array[index].note - messages_array[index-1].note
    return res


def midifile_to_dict(mid):
    tracks = []
    for track in mid.tracks:
        tracks.append([vars(msg).copy() for msg in track])

    return {
        'ticks_per_beat': mid.ticks_per_beat,
        'tracks': tracks,
    }


# -------------------------------------------------------------------------------------------------------------------- #
# ----------------------------------------------------- Testing ------------------------------------------------------ #
# -------------------------------------------------------------------------------------------------------------------- #
class RepresentationTestCase(unittest.TestCase):
    """
    In this class we test the implementation of our methods to retrieve information from music files.
    We check whether we retrieve the result we expect.
    If not, we have to check the implementation to let this tests pass again!
    """
    def test_ioi(self):
        self.assertTrue(ioi([mido.Message('note_on', note=100, velocity=3, time=3.1),
                             mido.Message('note_on', note=100, velocity=3, time=6.2)]) == 3.1)

    def test_relative_note(self):
        self.assertTrue(relative_note([mido.Message('note_on', note=50, velocity=3, time=3.1),
                                       mido.Message('note_on', note=100, velocity=3, time=6.2)]) == 50)
