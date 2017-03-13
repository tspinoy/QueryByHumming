from aubio import source, sink, digital_filter
from os.path import basename, splitext

def apply_filter(path):

    # open input file, get its samplerate
    s = source(path)
    samplerate = s.samplerate

    # create an A-weighting filter
    f = digital_filter(7)
    f.set_a_weighting(samplerate)
    # alternatively, apply another filter

    # create output file
    o = sink("filtered_" + splitext(basename(path))[0] + ".wav", samplerate)

    total_frames = 0
    while True:
        samples, read = s()
        filtered_samples = f(samples)
        o(filtered_samples, read)
        total_frames += read
        if read < s.hop_size: break

    duration = total_frames / float(samplerate)
    print ("read {:s}".format(s.uri))
    print ("applied A-weighting filtered ({:d} Hz)".format(samplerate))
    print ("wrote {:s} ({:.2f} s)".format(o.uri, duration))

#apply_filter("/Users/thijsspinoy/OneDrive/Muziek/2 Unlimited - No Limit.mp3")

import sys
from aubio import source, onset

win_s = 512                 # fft size
hop_s = win_s // 2          # hop size

if len(sys.argv) < 2:
    print("Usage: %s <filename> [samplerate]" % sys.argv[0])
    sys.exit(1)

filename = sys.argv[1]

samplerate = 0
if len( sys.argv ) > 2: samplerate = int(sys.argv[2])

s = source(filename, samplerate, hop_s)
samplerate = s.samplerate

o = onset("default", win_s, hop_s, samplerate)

# list of onsets, in samples
onsets = []

# total number of frames read
total_frames = 0
while True:
    samples, read = s()
    if o(samples):
        print("%f" % o.get_last_s())
        onsets.append(o.get_last())
    total_frames += read
    if read < hop_s:
        break

print len(onsets)