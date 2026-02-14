tTwosday_Quest_Structured s40

# 4/4 @ s40 => 1 beat = 1.5s, 1 bar = 6s, 10 bars ~= 60s.
# Updated: shorter rhythm-only intro, denser melodies, more variation.

{
  # Pad: one chord per bar
  istring:harmonics=10,decay=7.2,detune=5,atk=0.03,rel=0.40,cut=1800,fenv=700,fatk=0.03,fdec=0.35,fsus=0.2,frel=0.30
  o4 d4 v0.46
  [ E G B ]
  [ C E G ]
  [ D F# A ]
  [ B_o3 D F# ]
  [ E G B ]
  [ C E G ]
  [ D F# A ]
  [ A_o3 C E ]
  [ E G B ]
  [ E G B ]
}

{
  # Pluck ostinato with small rhythmic/melodic mutations each section
  ipluck:decay=0.990,bright=0.18,damp=0.34,atk=0.001,rel=0.07
  o4 d1/8 v0.35
  E B E_o5 B  E B F#_o5 B
  C G C_o5 G  C G D_o5 G
  D A D_o5 A  F# A D_o5 A
  B_o3 F# B F#  B_o3 F# C#_o5 F#
  E B G E  F# B G B
  C G E C  D G E G
  D A F# D  E A F# A
  A_o3 E C E  B_o3 E D E
  E B G E  D A F# D
  E B G E  D B_o3 A_o3 B_o3
}

{
  # Hats: add syncopation and occasional denser hits
  inoise
  d1/8 v0.12
  C r C r C r C C  C r C r C r C r
  C r C r C C C r  C r C r C r C r
  C r C r C r C C  C r C r C r C r
  C r C r C C C r  C r C r C r C r
  C r C r C r C C  C r C r C r C r
}

{
  # Lead now enters after 2 bars (8 beats), with denser call/response
  ipulse:pw=0.20,atk=0.01,dec=0.09,sus=0.70,rel=0.16
  o5 d1/8 v0.76
  f8

  # Bar 3: ease-in phrase
  r E F# G  A G F# E

  # Bar 4: call
  B_o4 D E G  A G E D

  # Bar 5: response
  E F# G B  A G E D

  # Bar 6: theme variation
  C E G A  B A G E

  # Bar 7: counter-theme push
  D F# A B  C_o6 B A F#

  # Bar 8: answer + descent
  A G E D  E D B_o4 A_o4

  # Bar 9: reprise hook
  E G B A  G E D B_o4

  # Bar 10: closer
  E G B E_o6  D_o6 B A G
}

{
  # Counter line enters after 3 bars to avoid long sparse section
  isine:atk=0.02,dec=0.10,sus=0.60,rel=0.20
  o6 d1/8 v0.30
  f12
  B A G E  D E F# G
  F# E D B_o5  A_o5 B_o5 C_o6 D_o6
  E_o6 D_o6 C_o6 A_o5  G_o5 F#_o5 E_o5 D_o5
  B_o5 D_o6 E_o6 D_o6  B_o5 A_o5 G_o5 F#_o5
  G_o5 A_o5 B_o5 D_o6  E_o6 D_o6 B_o5 A_o5
  B_o5 A_o5 G_o5 E_o5  F#_o5 E_o5 D_o5 B_o4
  E_o5 F#_o5 G_o5 B_o5  A_o5 G_o5 F#_o5 E_o5
}

{
  # Bass with more movement; not just straight roots all the way through
  isaw:atk=0.01,dec=0.10,sus=0.74,rel=0.12,cut=640,fenv=1400,fatk=0.01,fdec=0.18,fsus=0.0,frel=0.12
  o2 d1 v0.58
  E E B_o1 B_o1
  C C G_o1 G_o1
  D A_o1 D A_o1
  B_o1 F#_o1 B_o1 F#_o1
  E B_o1 E G_o1
  C G_o1 C E_o1
  D A_o1 D F#_o1
  A_o1 E_o1 A_o1 C_o2
  E B_o1 E D_o2
  E E B_o1 B_o1
}
