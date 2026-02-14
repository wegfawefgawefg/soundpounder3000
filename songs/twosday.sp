tTwosday_Quest s40

# 90s RPG-style layered arrangement using cursor stack.
# Structure: intro pad + pulse arp + lead + bass + noise hats + counter line.

{
  # Lead melody (square + pulse blend feel)
  ipulse:pw=0.22,atk=0.004,dec=0.06,sus=0.72,rel=0.10
  o5 d1/8 v0.78
  E B_o4 C D  E B_o4 C D
  F C_o5 D E  F E D C
  B_o4 F G A  B A G F
  E D C B_o4  A_o4 B_o4 C D

  G D E F#  G A B D_o6
  E_o6 D_o6 C_o6 B  A G F# E
  D A_o4 B_o4 C  D E F# A
  G_d1/4 E_d1/8 D C  B_o4 A_o4 G_o4 F#_o4
}

{
  # Warm string pad chords (slow harmonic bed)
  istring:harmonics=11,decay=6.8,detune=6,atk=0.015,rel=0.28,cut=2100,fenv=900,fatk=0.02,fdec=0.30,fsus=0.2,frel=0.24
  o4 d1/2 v0.52
  [ E G B ] [ C E G ] [ D F# A ] [ B_o3 D F# ]
  [ E G B ] [ C E G ] [ D F# A ] [ G B D_o5 ]
  [ C E G ] [ D F# A ] [ E G B ] [ B_o3 D F# ]
  [ C E G ] [ A_o3 C E ] [ B_o3 D F# ] [ G B D_o5 ]
}

{
  # Rhythmic pluck arpeggio
  ipluck:decay=0.991,bright=0.22,damp=0.30,atk=0.001,rel=0.07
  o4 d1/16 v0.43
  E B E_o5 B  C G C_o5 G  D A D_o5 A  B_o3 F# B F#
  E B E_o5 B  C G C_o5 G  D A D_o5 A  G D G_o5 D
  C G C_o5 G  D A D_o5 A  E B E_o5 B  B_o3 F# B F#
  C G C_o5 G  A_o3 E A E  B_o3 F# B F#  G D G_o5 D
}

{
  # Bass foundation
  isaw:atk=0.006,dec=0.08,sus=0.78,rel=0.11,cut=700,fenv=1900,fatk=0.01,fdec=0.18,fsus=0.0,frel=0.10
  o2 d1/8 v0.62
  E E E E  C C C C  D D D D  B_o1 B_o1 B_o1 B_o1
  E E E E  C C C C  D D D D  G_o1 G_o1 G_o1 G_o1
  C C C C  D D D D  E E E E  B_o1 B_o1 B_o1 B_o1
  C C C C  A_o1 A_o1 A_o1 A_o1  B_o1 B_o1 B_o1 B_o1  G_o1 G_o1 G_o1 G_o1
}

{
  # Noise hats + snare-ish accents
  inoise
  d1/16 v0.20
  C r C r  C r C C  C r C r  C C r C
  C r C r  C r C C  C r C r  C C r C
  C r C r  C r C C  C r C r  C C r C
  C r C r  C r C C  C r C r  C C r C
}

{
  # High sine counter melody enters later
  isine:atk=0.01,dec=0.08,sus=0.65,rel=0.14
  f16
  o6 d1/8 v0.36
  B A G E  F E D B_o5
  C D E G  F E D C
  A B C_o7 B  A G F# E
  D C B_o5 A_o5  G_o5 F#_o5 E_o5 D_o5
}
