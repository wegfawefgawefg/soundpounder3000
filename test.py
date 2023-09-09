import os

from playsound import playsound

from soundpounder3000 import fiddle_to_wav

"""     SONGS   """
twinkle_twinkle = "ttwinkle_twinkle s120 C C G G A A G r F F E E D D C r G G F F E E D r G G F F E E D r C C G G A A G r F F E E D D C"
something = "C E G C E G C E G C E G C E G C E G B B B B"
larrys_song = "tlarryssong Eb C C# D E F# A G D B G# A B C E D# D C C# D B A G F# D D D D D D D D D D D D D D D"
fiddle = "tMy_Fuckin_Song_Title s60 d1/16 C E G C E G C E G"
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
happy_birthday = (
    "tHappy_Birthday s120 "
    "C_o4 f0.1 D f0.1 E f0.1 C f0.1 C f0.1 D f0.1 E f0.1 C f0.1 E f0.1 G f0.1 E f0.1 G f0.1 A f0.1 G f0.1 E f0.1 C f0.1 C f0.1 D f0.1 E f0.1 C f0.1 G f0.1 E f0.1 C f0.1 C f0.1 D f0.1 E f0.1 C f0.1 E f0.1 G f0.1 E f0.1 G f0.1 A f0.1 G f0.1 E f0.1 C"
)
# simple test of every note from c to c_10
full_range_test = (
    "tFull_Range_Test s3200 "
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
    "tComplex_Test s480 "
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
# )

title = fiddle_to_wav(complex_test)
path = os.path.join("waves/", f"{title}.wav")
playsound(path)

# fiddle_to_wav(test)
# playsound("Test" + ".wav")
