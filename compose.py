import os
import time

from playsound import playsound

from soundpounder3000 import fiddle_to_wav

'''     SONGS   '''
twinkle_twinkle = 'ttwinkle_twinkle s120 C C G G A A G r F F E E D D C r G G F F E E D r G G F F E E D r C C G G A A G r F F E E D D C'
something = 'C E G C E G C E G C E G C E G C E G B B B B'
larrys_song = 'tlarryssong Eb C C# D E F# A G D B G# A B C E D# D C C# D B A G F# D D D D D D D D D D D D D D D'
fiddle = 'tMy_Fuckin_Song_Title s60 d1/16 C E G C E G C E G'
larrysshittysong = "tLarry's_Shitty_Song s60 C_o4_d1/16 o4 r r_d1/16 o4 d1/16 C [ C_d4 f1 E_d3 f1 G_d2 f1 B_d1_o+1 ] f1 b d1 [ C E_v0.5 G_v0.25 B_o+1 ]"
test = "tTest s120 C_o1 C_o2 C_o3 C_o4 C_o5 C_o6 C_o7 C_o8"
spirited_away_one_summers_day = (
    "tOne_Summer's_Day s60 "
    "[ F f0.1 G f0.1 A_o5 f0.1 C_o5 f0.1 E_o5 ] f-0.2 "
    "[ E f0.1 A_o5 f0.1 B_o5 ] "
    "[ D f0.1 G f0.1 A#_o5 ] "
    "[ C f0.1 D f0.1 F# f0.1 G f0.1 A_o5 f0.1 D_o6 ] r_d0.5 "

    "E_d2 d0.5 E_o5 E_o5 E_o5 E_o5 D_o5 E_o5 A_o5 E_o5 D_o5_d0.25 D_o5_d1 r_d0.5 "
    "D_o5 D_o5 D_o5 D_o5 C_o5 D_o5 G_o5 D_o5 C_o5 B_o4 C_o5_d1 "
)
interesting = (
    "tinteresting s60 "
    "[ F f0.1 G f0.1 A_o5 f0.1 C_o5 f0.1 E_o5 ] f-0.2 "
    "[ E f0.1 A_o5 f0.1 B_o5 ] "
    "[ D f0.1 G f0.1 A#_o5 ] "
    "[ C f0.1 D f0.1 F# f0.1 G f0.1 A_o5 f0.1 D_o6 ] r_d0.5 "

    # 2nd intro chord sequence, same as 1st, but 4 half steps higher
    "[ A f0.1 B f0.1 C#_o6 f0.1 E_o6 f0.1 G#_o6 ] f-0.2 "
    "[ G# f0.1 C#_o6 f0.1 D#_o6 ] "
    "d0.5 [ G# f0.1 C#_o6 f0.1 D#_o6 ] d1.0 "
    # a bunch of jazzy major seven chords
    # c major 7
    # "[ C# f0.1 E f0.1 G# f0.1 A f0.1 C#_o6 f0.1 E_o6 ] f-0.2 "
    # "[ E f0.1 G# f0.1 A f0.1 C#_o6 f0.1 E_o6 ] "
    # "[ G# f0.1 A f0.1 C#_o6 f0.1 E_o6 ] "
    # "[ A f0.1 C#_o6 f0.1 E_o6 ] "
    # the above section but down an octave
    "[ C#_o3 f0.1 E_o3 f0.1 G#_o3 f0.1 A_o3 f0.1 C#_o5 f0.1 E_o5 ] f-0.2 "
    "[ E_o3 f0.1 G#_o3 f0.1 A_o3 f0.1 C#_o5 f0.1 E_o5 ] "
    "[ G#_o3 f0.1 A_o3 f0.1 C#_o5 f0.1 E_o5 ] "
    "[ A_o3 f0.1 C#_o5 f0.1 E_o5 ] "
    # f major 7
    "[ F# f0.1 A f0.1 C#_o6 f0.1 D#_o6 f0.1 F#_o6 ] f-0.2 "
    "[ A f0.1 C#_o6 f0.1 D#_o6 f0.1 F#_o6 ] "
    # b flat major 7
    "[ B f0.1 D f0.1 F# f0.1 G# f0.1 B_o6 f0.1 D_o7 ] f-0.2 "
    "[ D f0.1 F# f0.1 G# f0.1 B_o6 f0.1 D_o7 ] "
    # a clean riff non chord
    "A f0.1 B f0.1 C#_o6 f0.1 E_o6 f0.1 G#_o6 "
    # resolve with a reference to the intro sequence, but descending
    "[ G# f0.1 C#_o5 f0.1 D#_o5 ] f-0.2 "
    "[ G# f0.1 C#_o5 f0.1 D#_o5 ] "
    "[ G# f0.1 C#_o5 f0.1 D#_o5 ] "
    # last chord
    "[ G# f0.1 C#_o6 f0.1 D#_o6 ] f-0.2 "
)

happy_birthday = (
    "tHappy_Birthday s120 "
    "C_o4 f0.1 D f0.1 E f0.1 C f0.1 C f0.1 D f0.1 E f0.1 C f0.1 E f0.1 G f0.1 E f0.1 G f0.1 A f0.1 G f0.1 E f0.1 C f0.1 C f0.1 D f0.1 E f0.1 C f0.1 G f0.1 E f0.1 C f0.1 C f0.1 D f0.1 E f0.1 C f0.1 E f0.1 G f0.1 E f0.1 G f0.1 A f0.1 G f0.1 E f0.1 C"

)
# simple test of every note from c to c_10
full_range_test = (
    "tFull_Range_Test s800 "
    # lower octaves
    "C_o1 C#_o1 D_o1 D#_o1 E_o1 F_o1 F#_o1 G_o1 G#_o1 A_o1 A#_o1 B_o1 "
    "C_o2 C#_o2 D_o2 D#_o2 E_o2 F_o2 F#_o2 G_o2 G#_o2 A_o2 A#_o2 B_o2 "
    "C_o3 C#_o3 D_o3 D#_o3 E_o3 F_o3 F#_o3 G_o3 G#_o3 A_o3 A#_o3 B_o3 "
    "C C# D D# E F F# G G# A A# B "
    "C_o5 C#_o5 D_o5 D#_o5 E_o5 F_o5 F#_o5 G_o5 G#_o5 A_o5 A#_o5 B_o5 "
    "C_o6 C#_o6 D_o6 D#_o6 E_o6 F_o6 F#_o6 G_o6 G#_o6 A_o6 A#_o6 B_o6 "
    "C_o7 C#_o7 D_o7 D#_o7 E_o7 F_o7 F#_o7 G_o7 G#_o7 A_o7 A#_o7 B_o7 "
    "C_o8 C#_o8 D_o8 D#_o8 E_o8 F_o8 F#_o8 G_o8 G#_o8 A_o8 A#_o8 B_o8 "
    "C_o9 C#_o9 D_o9 D#_o9 E_o9 F_o9 F#_o9 G_o9 G#_o9 A_o9 A#_o9 B_o9 "
    "C_o10 "
)
# "[ G B D F ] "
# "[ B D F A ] "
# "[ D F A C ] "
# "[ F A C E ] "
# "[ A C E G ] "

# note order for major chords is half steps of 4, 3, 4, 3 repeating
#   TODO
#   auto chording
#   itterative chords from root, major or minor
#   seemlessly chain them into the song
#   being able to shift the octave up
#   being able to variabalize sections of the song, as note objects
#       then script on those

complex_test = (
    "tComplex_Test s240 "
    "[ C E G B ] "
    "[ E G B D_o5 ] "
    "[ G B D_o5 F#_o5 ] "
    "[ B D_o5 F#_o5 A_o5 ] "
    "d2 [ D_o5 F#_o5 A_o5 C#_o6 ] "
    "d1 "

    # shift forward by 4 half steps
    "[ E G B D_o5 ] "
    "[ G B D_o5 F#_o5 ] "
    "[ B D_o5 F#_o5 A_o5 ] "
    "[ D_o5 F#_o5 A_o5 C#_o6 ] "
    "d2 [ F#_o5 A_o5 C#_o6 E_o6 ] "
    "d1 "

    # final chirp
    "d2 [ F#_o5 A_o5 C#_o6 E_o6 ] "
    "d1 [ F#_o5 A_o5 C#_o6 E_o6 ] "
    # go up a half step
    "d6 [ G_o5 B_o5 D_o6 F#_o6 ] "
)

    # "d4 [ A_o5 C#_o6 E_o6 G#_o6 ] "

    # "[ C#_o6 E_o6 G#_o6 B_o6 ] "
    # "[ E_o6 G#_o6 B_o6 D_o7 ] "
    # "[ G#_o6 B_o6 D_o7 F#_o7 ] "
    # "[ B_o6 D_o7 F#_o7 A_o7 ] "
    # "[ D_o7 F#_o7 A_o7 C#_o8 ] "
    # "[ F#_o7 A_o7 C#_o8 E_o8 ] "
    # "[ A_o7 C#_o8 E_o8 G#_o8 ] "
    # "[ C#_o8 E_o8 G#_o8 B_o8 ] "

complex_test = (
    "tSimple_Test s400 "
    " C E G "
    " C E G "
    " C F A "
    " C F A "
    " C G B "
    " C G B "
    " C E G "
    " C E G "
    " C B D_o5 "
    " C B D_o5 "
    " C A C#_o5 "
    " C A C#_o5 "
    " C G B "
    " C E B "
    " C E G C_o5_d4 "
)

simple_test = (
    "tSimple_Test s600 "
    " C "
)

computer_polka = (
    # a simple polka in c major. 4/4 time. 80 bpm
    "tComputer_Polka s80 "

    # rumpatum drum beat
    " inoise "
    "d0.125 "
    " { "
    " r r r r r r r r r r r r "
    " r r r r r r r r r r r r "
    " C r r r C r r r C r C r "
    " C r r r C r r r C r C r "
    " C r r r C r C r C r C r "
    " C r r r C r C r C r C r "
    " C r C C C r C r C C C r "
    " C r C C C r C r C C C r "
    " C "
    " } "


    # simple polka baseline in C major
    " isquare "
    " d0.5 "
    " v0.75 "
    " { "
    # " C_o4 G_o3 C_o4 G_o3 C_o4 G_o3 C_o4 G_o3 "
    " r r r r r r r r"
    " C_o4 r C_o4 r C_o4 G_o3 C_o4 G_o3 "
    " C_o4 G_o3 C_o4 G_o3 C_o4 G_o3 C_o4 "
    " C_o3_d4 "
    " } "

    # simple polka rhythm
    " isquare "
    " v1.0 "
    " d0.25 "
    " { "
    " r r r " 
    " C_o5 E_o5 G_o5 " 
    " C_o5 F_o5 A_o5 " 
    " C_o5 F_o5 A_o5 " 

    " C_o5 G_o5 B_o5 " 
    " C_o5 G_o5 B_o5 " 
    " C_o5 E_o5 G_o5 " 
    " C_o5 E_o5 G_o5 " 

    " C_o5 B_o4 D_o5 " 
    " C_o5 B_o4 D_o5 " 
    " C_o5 A_o4 C_o5 " 
    " C_o5 A_o4 C_o5 " 

    " C_o5 G_o4 B_o4 " 
    " C_o5 G_o4 B_o4 " 
    " C_o5 E_o5 B_o4 " 
    " C_o6_d4 " 
    " } "

    # # high fast twinkly notes
    " v0.75"
    " isine "
    " d0.25 "
    " C_o7 r G_o6 r A_o6 r E_o6 r "
    " A_o6 r E_o6 r G_o6 r C_o6 r "

    " C_o7 r G_o6 r A_o6 r E_o6 r "
    " A_o6 r E_o6 r G_o6 r C_o6 r "

    " C_o7 r G_o6 r A_o6 r E_o6 r "
    " A_o6 r B_o6 "
    " G_o6_d4 "
)

title = fiddle_to_wav(computer_polka)
path = os.path.join("waves/", f"{title}.wav")
playsound(path)

# fiddle_to_wav(test)
# playsound("Test" + ".wav")