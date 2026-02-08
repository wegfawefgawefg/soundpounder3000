# Instrument Showcase
# Exercises:
# - instruments: sine, square, noise, string, saw, triangle, pulse
# - instrument params: ipulse:pw=..., istring:harmonics=...,decay=...,detune=...
# - comments: full-line `#`, inline `;` and `//`
# - chords: [ ... ]

tinstrument_showcase
s180
o4
d1/8

; baseline: sine
isine
C D E F G A B C_o5
r

; bright: saw
isaw
C_o4_d1/16 E G C_o5  C_o5 B A G  F E D C_o4
r

; hollow: triangle
itriangle
[ C E G ] [ D F A ] [ E G B ] [ F A C_o5 ]
r

; punchy: square
isquare
d1/16
C C C C  G G G G  C_o5 C_o5 C_o5 C_o5  G G G G
r_d1/4

; pulse width: thin buzzy lead
ipulse:pw=0.2
d1/12
C_o5 D E F G A B C_o6
r_d1/6

; noise "hat" pattern (freq ignored)
inoise
d1/32
v0.35
{ r r r r  C r r C  r r r r  C r C r } // end hat loop
v1.0
r_d1/8

; string-ish pluck (additive + decay)
istring:harmonics=12,decay=6,detune=8
d1/8
[ C_o3 G_o3 C_o4 ] r [ D_o3 A_o3 D_o4 ] r [ E_o3 B_o3 E_o4 ] r [ F_o3 C_o4 F_o4 ] r
r_d1/4

; back to sine for a cadence
isine
d1/8
[ C E G ] r [ F A C_o5 ] r [ G B D_o5 ] r C_o5_d1

