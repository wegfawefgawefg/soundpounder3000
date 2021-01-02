import os

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
    "[ F f0.1 G f0.1 A_o5 f0.1 C_o5 f0.1 E_o5 ] "
    "[ E f0.1 A_o5 f0.1 B_o5 ] "
    "[ D f0.1 G f0.1 A#_o5 ] "
    "[ C f0.1 D f0.1 F# f0.1 G f0.1 A_o5 f0.1 D_o6 ] r_d0.5 "
    "E_d2 d0.5 E_o5 E_o5 E_o5 E_o5 D_o5 E_o5 A_o5 E_o5 D_o5_d0.25 D_o5_d1 r_d0.5 "
    "D_o5 D_o5 D_o5 D_o5 C_o5 D_o5 G_o5 D_o5 C_o5 B_o4 C_o5_d1 "
)

fiddle_to_wav(spirited_away_one_summers_day)
path = os.path.join("waves/", "One_Summer's_Day" + ".wav")
playsound(path)

# fiddle_to_wav(test)
# playsound("Test" + ".wav")