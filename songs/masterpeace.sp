tMasterpeace_Chronicles_III s70

# Iteration v3
# I   s70  : 4 bars   intro
# II  s92  : 8 bars   theme + response
# III s66  : 16 bars  development arc
# IV  s108 : 8 bars   finale

{
  # Harmonic bed
  istring:harmonics=13,decay=7.8,detune=8,atk=0.03,rel=0.46,cut=1850,fenv=950,fatk=0.03,fdec=0.36,fsus=0.2,frel=0.30
  o4 v0.44

  s70 d4
  [ E G B D_o5 ] [ C E G B ] [ A C E G ] [ B D F# A ]

  s92 d4
  [ E G B D_o5 ] [ C E G B ] [ D F# A C_o5 ] [ G B D_o5 F#_o5 ]
  [ C E G B ] [ A C E G ] [ B D F# A ] [ E G B D_o5 ]

  s66 d4
  [ A C E G ] [ G B D_o5 F#_o5 ] [ F# A C#_o5 E_o5 ] [ B D F# A ]
  [ C E G B ] [ G B D_o5 F#_o5 ] [ A C E G ] [ E G B D_o5 ]
  [ F A C E ] [ C E G B ] [ D F# A C_o5 ] [ B D F# A ]
  [ C E G B ] [ A C E G ] [ B D F# A ] [ D F# A C_o5 ]

  s108 d4
  [ E G B D_o5 ] [ G B D_o5 F#_o5 ] [ A C E G ] [ C E G B ]
  [ D F# A C_o5 ] [ B D F# A ] [ C E G B ] [ E G B E_o5 ]
}

{
  # Bass with passing tones
  isaw:atk=0.008,dec=0.09,sus=0.78,rel=0.11,cut=720,fenv=1700,fatk=0.01,fdec=0.14,fsus=0.0,frel=0.10
  o2 v0.60

  s70 d1
  E B E D  C G C B_o1  A E A G_o1  B F# B A_o1

  s92 d1
  E B E G  C G C E  D A D F#  G D G B
  C G C E  A E A C  B F# B D  E B E D

  s66 d1
  A E A C  G D G B  F# C# F# A  B F# B D
  C G C E  G D G B  A E A C  E B E G
  F C F A  C G C E  D A D F#  B F# B D
  C G C E  A E A C  B F# B D  D A D F#

  s108 d1
  E B E G  G D G B  A E A C  C G C E
  D A D F#  B F# B D  C G C E  E B E B
}

{
  # Percussive engine
  inoise
  o4 v0.16

  s70 d1/2
  C r C r  C r C r
  C r C C  C r C r
  C r C r  C C r C
  C r C r  C r C C

  s92 d1/2
  C r C C  C r C r
  C r C r  C C r C
  C r C C  C r C r
  C C r C  C r C C
  C r C C  C r C r
  C r C r  C C r C
  C r C C  C r C r
  C C C r  C r C C

  s66 d1/2
  C r r r  C r r r
  C r C r  r r C r
  C r C r  C r C r
  C C r C  C r C r
  C r C C  C r C r
  C r C r  C C r C
  C r C C  C r C r
  C C r C  C r C C
  C r C r  C r C C
  C C r C  C r C r
  C r C C  C C r C
  C r C r  C C r C
  C C r C  C r C C
  C r C C  C C r C
  C C C r  C r C C
  C C r C  C r C C

  s108 d1/2
  C C r C  C r C C
  C r C C  C C r C
  C C r C  C r C C
  C r C C  C C r C
  C C r C  C r C C
  C r C C  C C r C
  C C C r  C C r C
  C C r C  C r C C
}

{
  # Triplet/compound engine
  ipluck:decay=0.992,bright=0.24,damp=0.30,atk=0.001,rel=0.06
  o4 v0.31

  s70 d1
  f16

  s92 d2/3
  E B E_o5 G_o5 E_o5 B
  C G C_o5 E_o5 C_o5 G
  D A D_o5 F#_o5 D_o5 A
  G D G_o5 B_o5 G_o5 D
  C G E_o5 G_o5 C_o5 G
  A E C_o5 E_o5 A_o4 E
  B F# B_o5 D_o6 B_o5 F#
  E B E_o5 G_o5 B_o5 G_o5

  s66 d1
  A E C_o5 A  G D B_o4 G  F# C# A_o4 F#  B F# D_o5 B
  C G E_o5 C  G D B_o4 G  A E C_o5 A  E B G_o4 E
  F C A_o4 F  C G E_o5 C  D A F#_o4 D  B F# D_o5 B
  C G E_o5 C  A E C_o5 A  B F# D_o5 B  D A F#_o4 D

  s108 d2/3
  E B E_o5 G_o5 E_o5 B
  G D G_o5 B_o5 G_o5 D
  A E A_o5 C_o6 A_o5 E
  C G C_o5 E_o5 C_o5 G
  D A D_o5 F#_o5 D_o5 A
  B F# B_o5 D_o6 B_o5 F#
  C G E_o5 G_o5 C_o5 G
  E B E_o5 G_o5 B_o5 E_o6
}

{
  # Main lead
  ipulse:pw=0.21,atk=0.007,dec=0.09,sus=0.72,rel=0.15
  o5 v0.79

  s70 d1
  f16

  s92 d1/2
  E F# G B  A G E D
  E F# G A  B A G E
  D E F# A  G F# D C
  D E F# G  A G F# D
  C D E G  F# E D B_o4
  C D E F#  G A B A
  B_o4 D E G  A G E D
  E G B E_o6  D_o6 B A G

  s66 d1
  A G E C
  D E F# A
  G F# E D
  C D E G
  F# E D C#
  B_o4 C# D F#
  E D B_o4 A_o4
  B_o4 D E F#
  G F# E D
  C D E C
  A_o4 B_o4 C D
  E D C A_o4
  B_o4 D E G
  F# E D B_o4
  A_o4 C B_o4 A_o4
  G F# E D

  s108 d1/2
  E F# G A  B A G E
  D E F# G  A G F# D
  G A B D_o6  C_o6 B A G
  F# G A B  A G F# E
  C D E G  F# E D C
  B_o4 C D E  F# E D B_o4
  E G B E_o6  D_o6 B A G
  F# E D B_o4  E_d1 r_d1
}

{
  # Countermelody
  itriangle:atk=0.01,dec=0.09,sus=0.66,rel=0.16
  o6 v0.34

  s70 d1/2
  f8
  B A G E  D E F# G
  A G F# E  D C B_o5 A_o5

  s92 d1/2
  r r r r  B A G E
  D E F# G  F# E D B_o5
  A_o5 B_o5 C_o6 D_o6  E_o6 D_o6 C_o6 A_o5
  G_o5 A_o5 B_o5 D_o6  C_o6 B_o5 A_o5 G_o5
  F#_o5 E_o5 D_o5 B_o4  C_o5 D_o5 E_o5 G_o5
  A_o5 G_o5 F#_o5 E_o5  D_o5 E_o5 F#_o5 A_o5
  B_o5 A_o5 G_o5 E_o5  F#_o5 E_o5 D_o5 B_o4
  G_o5 A_o5 B_o5 D_o6  E_o6 D_o6 B_o5 A_o5

  s66 d1
  C_o6 B_o5 A_o5 F#_o5
  G_o5 A_o5 B_o5 D_o6
  E_o6 D_o6 C_o6 A_o5
  B_o5 C_o6 D_o6 F#_o6
  A_o5 G_o5 F#_o5 E_o5
  D_o5 E_o5 F#_o5 A_o5
  G_o5 F#_o5 E_o5 D_o5
  C#_o5 D_o5 E_o5 F#_o5
  G_o5 A_o5 B_o5 D_o6
  C_o6 B_o5 A_o5 G_o5
  F#_o5 E_o5 D_o5 B_o4
  C_o5 D_o5 E_o5 G_o5
  A_o5 G_o5 F#_o5 E_o5
  D_o5 C#_o5 B_o4 A_o4
  B_o4 C#_o5 D_o5 F#_o5
  E_o5 D_o5 B_o4 A_o4

  s108 d1/2
  B_o5 A_o5 G_o5 E_o5  D_o5 E_o5 F#_o5 G_o5
  A_o5 G_o5 F#_o5 E_o5  D_o5 C_o5 B_o4 A_o4
  G_o5 A_o5 B_o5 D_o6  C_o6 B_o5 A_o5 G_o5
  F#_o5 G_o5 A_o5 B_o5  A_o5 G_o5 F#_o5 E_o5
  C_o6 B_o5 A_o5 F#_o5  G_o5 A_o5 B_o5 D_o6
  E_o6 D_o6 C_o6 B_o5  A_o5 G_o5 F#_o5 E_o5
  D_o6 B_o5 A_o5 G_o5  F#_o5 E_o5 D_o5 B_o4
  E_o5 G_o5 B_o5 E_o6  D_o6 B_o5 A_o5 G_o5
}

{
  # Offbeat chord stabs
  isquare:atk=0.004,dec=0.06,sus=0.58,rel=0.08,cut=1600,fenv=1200,fatk=0.01,fdec=0.12,fsus=0.0,frel=0.08
  o4 v0.32 d1/2

  s70
  r r r r  r r r r
  r [ C E G ] r [ C E G ]  r [ C E G ] r [ C E G ]
  r [ A C E ] r [ A C E ]  r [ A C E ] r [ A C E ]
  r [ B D F# ] r [ B D F# ]  r [ B D F# ] r [ B D F# ]

  s92
  r [ E G B ] r [ E G B ]  r [ E G B ] r [ E G B ]
  r [ C E G ] r [ C E G ]  r [ C E G ] r [ C E G ]
  r [ D F# A ] r [ D F# A ]  r [ D F# A ] r [ D F# A ]
  r [ G B D_o5 ] r [ G B D_o5 ]  r [ G B D_o5 ] r [ G B D_o5 ]
  r [ C E G ] r [ C E G ]  r [ C E G ] r [ C E G ]
  r [ A C E ] r [ A C E ]  r [ A C E ] r [ A C E ]
  r [ B D F# ] r [ B D F# ]  r [ B D F# ] r [ B D F# ]
  r [ E G B ] r [ E G B ]  r [ E G B ] r [ E G B ]

  s66
  r r r r  r r r r
  r r r r  r r r r
  r [ F# A C#_o5 ] r [ F# A C#_o5 ]  r [ F# A C#_o5 ] r [ F# A C#_o5 ]
  r [ B D F# ] r [ B D F# ]  r [ B D F# ] r [ B D F# ]
  r [ C E G ] r [ C E G ]  r [ C E G ] r [ C E G ]
  r [ G B D_o5 ] r [ G B D_o5 ]  r [ G B D_o5 ] r [ G B D_o5 ]
  r [ A C E ] r [ A C E ]  r [ A C E ] r [ A C E ]
  r [ E G B ] r [ E G B ]  r [ E G B ] r [ E G B ]
  r [ F A C ] r [ F A C ]  r [ F A C ] r [ F A C ]
  r [ C E G ] r [ C E G ]  r [ C E G ] r [ C E G ]
  r [ D F# A ] r [ D F# A ]  r [ D F# A ] r [ D F# A ]
  r [ B D F# ] r [ B D F# ]  r [ B D F# ] r [ B D F# ]
  r [ C E G ] r [ C E G ]  r [ C E G ] r [ C E G ]
  r [ A C E ] r [ A C E ]  r [ A C E ] r [ A C E ]
  r [ B D F# ] r [ B D F# ]  r [ B D F# ] r [ B D F# ]
  r [ D F# A ] r [ D F# A ]  r [ D F# A ] r [ D F# A ]

  s108
  r [ E G B ] r [ E G B ]  r [ E G B ] r [ E G B ]
  r [ G B D_o5 ] r [ G B D_o5 ]  r [ G B D_o5 ] r [ G B D_o5 ]
  r [ A C E ] r [ A C E ]  r [ A C E ] r [ A C E ]
  r [ C E G ] r [ C E G ]  r [ C E G ] r [ C E G ]
  r [ D F# A ] r [ D F# A ]  r [ D F# A ] r [ D F# A ]
  r [ B D F# ] r [ B D F# ]  r [ B D F# ] r [ B D F# ]
  r [ C E G ] r [ C E G ]  r [ C E G ] r [ C E G ]
  r [ E G B ] r [ E G B ]  r [ E G B ] r [ E G B ]
}

{
  # Bell sparkle and cadence markers
  ifm:car=1,mod=2,idx=4.8,atk=0.002,dec=0.18,sus=0.0,rel=0.34
  o6 v0.24

  s70 d2
  r r  E r  C r  B r

  s92 d1/2
  E r G r  C r E r
  D r F# r  G r B r
  C r E r  A r C_o7 r
  B r D_o7 r  E r B r
  C r G r  A r E r
  B r F# r  G r D r
  A r E r  B r F# r
  E r G r  B r E_o7 r

  s66 d1
  A r G r
  F# r B r
  C r G r
  A r E r
  F r C r
  D r B r
  C r A r
  B r D_o7 r
  E_o7 r D_o7 r
  C_o7 r B_o6 r
  A_o6 r G_o6 r
  F#_o6 r E_o6 r
  D_o6 r C_o6 r
  B_o5 r A_o5 r
  G_o5 r F#_o5 r
  E_o5 r D_o5 r

  s108 d1/2
  E r B r  G r D r
  A r E r  C r G r
  D r A r  B r F# r
  C r G r  E r B r
  E_o7 r D_o7 r  B r A r
  G r F# r  E r D r
  C r B_o5 r  A_o5 r G_o5 r
  E_o7 r B r  G r E r
}
