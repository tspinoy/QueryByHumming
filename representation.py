import math
import numpy as np
import unittest
import mido


# -------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------- Get information -------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
def get_messages(midi_file):
    """
    We only consider messages from the track Electric Piano 
    because this is the track where the music we want to compare is stored.
    :param midi_file: a loaded midi-file.
    :return: a sorted list of messages from the Electric Piano.
    """
    for i, track in enumerate(midi_file.tracks):
        if len(midi_file.tracks) == 1:
            track.sort(key=lambda message: message.time)  # very important to sort!!!
            return track
        elif track.name == "Electric Piano":
            track.sort(key=lambda message: message.time)  # very important to sort!!!
            return track


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

    return onsets_array


# -------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------- Measurements --------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
def ioi(messages_array):
    """
    :param messages_array: an array with the onset times.
    :return: a new array with the onset intervals computed by this function.
    """
    res = np.zeros(len(messages_array))

    for index in range(len(messages_array)):
        res[index-1] = messages_array[index].time - messages_array[index-1].time

    return res


def ioi_ratio(ioi_array):
    """
    :param ioi_array: an array with the onset times.
    :return: a new array with ratio's of the onset intervals computed by this function.
    """
    res = np.zeros(len(ioi_array)-1)

    for index in range(len(ioi_array)):
        if ioi_array[index] == 0:
            res[index-1] = float(0)
        else:
            res[index-1] = (ioi_array[index] / ioi_array[index-1])

    return res


def log_ioi_ratio(ioi_ratio_array):
    """
    :param ioi_ratio_array: an array with the onset times.
    :return: a new array with the logarithm of the ratio's of the onset intervals computed by this function.
    """

    for index in range(0, len(ioi_ratio_array)):
        ioi_ratio_array[index] = math.log(ioi_ratio_array[index], 2)

    return ioi_ratio_array


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
