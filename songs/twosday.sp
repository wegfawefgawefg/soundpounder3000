tTwosday_Quest_Structured s40

# 4/4 @ s40 => 1 beat = 1.5s, 1 bar (4 beats) = 6s.
# 10 bars total ~= 60s.
# Form:
# - Bars 1-4: Intro (no lead)
# - Bar 5: Lead ease-in
# - Bars 6-7: Theme (call/response)
# - Bar 8: Counter-theme
# - Bar 9: Theme reprise
# - Bar 10: Closer

{
  # Pad: one long chord per bar
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
  # Pluck ostinato (steady 8th notes)
  ipluck:decay=0.990,bright=0.18,damp=0.34,atk=0.001,rel=0.07
  o4 d1/8 v0.34
  E B E_o5 B  E B E_o5 B
  C G C_o5 G  C G C_o5 G
  D A D_o5 A  D A D_o5 A
  B_o3 F# B F#  B_o3 F# B F#
  E B E_o5 B  E B E_o5 B
  C G C_o5 G  C G C_o5 G
  D A D_o5 A  D A D_o5 A
  A_o3 E A E  A_o3 E A E
  E B E_o5 B  D A D_o5 A
  E B G E  D B_o3 A_o3 B_o3
}

{
  # Noise hats (subtle)
  inoise
  d1/8 v0.12
  C r C r C r C r  C r C r C r C r
  C r C r C r C r  C r C r C r C r
  C r C r C r C r  C r C r C r C r
  C r C r C r C r  C r C r C r C r
  C r C r C r C r  C r C r C r C r
}

{
  # Lead enters after 4 bars (16 beats)
  ipulse:pw=0.20,atk=0.01,dec=0.09,sus=0.70,rel=0.16
  o5 d1/8 v0.74
  f16

  # Bar 5: ease-in
  r r E F#  G r B A

  # Bar 6: call
  E D B_o4 A_o4  B_o4 D E G

  # Bar 7: response
  A G E D  E G A B

  # Bar 8: counter-theme handoff
  C_o6 B A G  F# E D B_o4

  # Bar 9: theme reprise
  E G B A  G E D B_o4

  # Bar 10: closer
  E G B E_o6  D_o6 B A G
}

{
  # Counter line enters in the main section
  isine:atk=0.02,dec=0.10,sus=0.60,rel=0.20
  o6 d1/8 v0.28
  f20
  B A G E  D E F# G
  F# E D B_o5  A_o5 B_o5 C_o6 D_o6
  E_o6 D_o6 C_o6 A_o5  G_o5 F#_o5 E_o5 D_o5
  B_o5 D_o6 E_o6 D_o6  B_o5 A_o5 G_o5 F#_o5
  G_o5 A_o5 B_o5 D_o6  E_o6 D_o6 B_o5 A_o5
}

{
  # Bass last so final parsed tones reach end-of-song (engine sizing quirk)
  isaw:atk=0.01,dec=0.10,sus=0.74,rel=0.12,cut=640,fenv=1400,fatk=0.01,fdec=0.18,fsus=0.0,frel=0.12
  o2 d1 v0.58
  E E E E
  C C C C
  D D D D
  B_o1 B_o1 B_o1 B_o1
  E E E E
  C C C C
  D D D D
  A_o1 A_o1 A_o1 A_o1
  E E E E
  E E B_o1 B_o1
}
