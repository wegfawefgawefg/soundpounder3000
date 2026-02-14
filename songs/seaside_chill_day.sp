tSeaside_Chill_Day s68

# === SEASIDE CHILL DAY ===
# Structural arc:
#   I   [bars  1-4 ] Dawn tide: pad only, sparse plucks wash in
#   II  [bars  5-12] Morning light: bass joins, ripples build
#   III [bars 13-20] Midday warmth: full texture, lead sings
#   IV  [bars 21-24] Afternoon drift: seagull accents, FM shimmer
#   V   [bars 25-28] Dusk fade: layers dissolve back to ocean
#
# Key: C major (with modal Lydian colour on F bars)
# Chord palette: Cmaj7 / Am7 / Fmaj7(#11) / G6sus2

{
  # === OCEAN PAD: slow lapping chords, wide stereo wash ===
  istring:harmonics=14,decay=9.0,detune=7,atk=0.08,rel=0.70,cut=1200,fenv=600,fatk=0.06,fdec=0.40,fsus=0.18,frel=0.50
  o4 v0.38 d4

  # I: Dawn — just the bed rolling in
  [ C E G B ]
  [ A_o3 C E G ]
  [ F A C_o5 E_o5 ]
  [ G B D_o5 F_o5 ]

  # II: Morning — harmony deepens
  [ C E G B ]
  [ E G B D_o5 ]
  [ A_o3 C E G ]
  [ F A C_o5 E_o5 ]

  [ C E G B ]
  [ G B D_o5 F_o5 ]
  [ A_o3 C E G ]
  [ F A C_o5 B_o5 ]

  # III: Midday — pad full and lush
  [ C E G B ]
  [ A_o3 C E G ]
  [ F A C_o5 E_o5 ]
  [ G B D_o5 F_o5 ]

  [ C E G B ]
  [ E G B D_o5 ]
  [ A_o3 C E G ]
  [ G B D_o5 F_o5 ]

  # IV: Afternoon
  [ F A C_o5 E_o5 ]
  [ C E G B ]
  [ A_o3 C E G ]
  [ G B D_o5 F_o5 ]

  # V: Dusk — gentle resolve
  [ C E G B ]
  [ A_o3 C E G ]
  [ F A C_o5 E_o5 ]
  [ C E G C_o5 ]
}

{
  # === SHORELINE BASS: tidal push and pull ===
  isaw:atk=0.01,dec=0.14,sus=0.72,rel=0.20,cut=480,fenv=1400,fatk=0.01,fdec=0.22,fsus=0.0,frel=0.16
  o2 v0.48 d1

  # I: Dawn — bass absent, let the pad breathe
  r r r r
  r r r r
  r r r r
  r r r r

  # II: Morning — bass wades in softly
  C r G_o1 r
  A_o1 r E_o1 r
  F r C_o2 r
  G r D_o2 r

  C G_o1 C G_o1
  A_o1 E_o1 A_o1 E_o1
  F C_o2 F C_o2
  G D_o2 G D_o2

  # III: Midday — bass is confident, walking
  C G_o1 E_o1 G_o1
  A_o1 E_o1 C_o2 E_o1
  F C_o2 A_o1 C_o2
  G D_o2 B_o1 D_o2

  C G_o1 C E_o1
  E B_o1 E B_o1
  A_o1 E_o1 A_o1 C_o2
  G D_o2 G F_o2

  # IV: Afternoon — lazy trippy bass
  F C_o2 F A_o1
  C G_o1 C E_o1
  A_o1 E_o1 A_o1 G_o1
  G D_o2 G D_o2

  # V: Dusk — slowing, back to root
  C G_o1 C G_o1
  A_o1 E_o1 A_o1 E_o1
  F C_o2 F A_o1
  C r r r
}

{
  # === RIPPLE PLUCKS: water surface arpeggios ===
  ipluck:decay=0.994,bright=0.22,damp=0.28,atk=0.001,rel=0.09
  o5 v0.26 d1/2

  # I: Dawn — sparse, one ripple at a time
  r r C G  r r E G
  r r A E  r r C E
  r r F C  r r A C
  r r G D  r r B D

  # II: Morning — ripples fill in
  C G E G  r G E r
  A E C E  r E C r
  F C A C  r C A r
  G D B D  r D B r

  C G E G  B G E G
  A E C E  G E C E
  F C A C  E C A C
  G D B D  F D B D

  # III: Midday — full ripple cascade
  C G E G  B G E G
  A E C E  G E C E
  F C A C  E C A C
  G D B D  F D B D

  C G E G  B G E G
  E B G B  D B G B
  A E C E  G E C E
  G D B D  F D B D

  # IV: Afternoon — syncopated, lazy
  F C A_o4 C  E C A_o4 C
  C G E G  B G E G
  A E C E  G E C E
  G D B D  F D B D

  # V: Dusk — sparse again, fading
  C G E G  r G r G
  A E C E  r E r E
  F C A C  r r r r
  C r r r  r r r r
}

{
  # === OCEAN NOISE: surf crash and foam hiss ===
  inoise:atk=0.04,dec=0.18,sus=0.0,rel=0.28
  o4 v0.09 d1/2

  # I: Dawn — barely there, gentle lapping
  r r r C  r r r r
  r C r r  r r r r
  r r r C  r r r r
  r C r r  r r r r

  # II–III: Morning and midday — waves come in sets of three
  C r r C  r r C r
  C r r C  r r C r
  C r r C  r r C r
  C r r C  r r C r

  C r C r  r C r C
  C r C r  r C r C
  C r C r  r C r C
  C r C r  r C r C

  C r r C  r r C r
  C r C r  r C r r
  C r r C  r C r r
  C r C r  r r C r

  C r r C  r C r r
  C r C r  r C r C
  C r r C  r r C r
  C r C r  r C r r

  # IV: Afternoon — irregular swells
  C r r r  C r r C
  r r C r  r C r r
  C r r r  r r C r
  C r r C  r r r r

  # V: Dusk — fading to a whisper
  r r C r  r r r r
  r C r r  r r r r
  r r r r  r r C r
  r r r r  r r r r
}

{
  # === BREEZE LEAD: flowing melodic line, pentatonic feel ===
  itriangle:atk=0.03,dec=0.12,sus=0.58,rel=0.30
  o6 v0.32 d1/2
  f24

  # I: Dawn — silent, horizon building
  r r r r  r r r r
  r r r r  r r r r
  r r r r  r r r r
  r r r r  r r r r

  # II: Morning — lead enters tentatively
  r r r r  r r r r
  r r r r  r r r r
  r r E D  C A_o5 r r
  G A C D  E D C r

  r r E G  A G E D
  E D C A_o5  G A C D
  A C D F  E D C A_o5
  G A C D  E D C B_o5

  # III: Midday — lead sings out, full phrases
  E G A C_o6  B_o5 A_o5 G_o5 E_o5
  D F G A  C_o6 B_o5 A_o5 G_o5
  E D C A_o5  G A C D
  E G C_o6 E_o6  D_o6 C_o6 A_o5 G_o5

  A_o5 G_o5 E_o5 D_o5  C_o5 D_o5 E_o5 G_o5
  F_o5 E_o5 D_o5 C_o5  A_o4 C_o5 D_o5 E_o5
  G_o5 A_o5 C_o6 D_o6  E_o6 D_o6 C_o6 A_o5
  G_o5 E_o5 D_o5 C_o5  B_o4 D_o5 E_o5 G_o5

  # IV: Afternoon — looser, floating
  E D C A_o5  r r G A
  C D E G  A G E r
  A_o5 C D E  G E D C
  D E G A  C_o6 r r r

  # V: Dusk — melody dissolves gently
  E D C A_o5  G r r r
  r r E D  C r r r
  r r r r  r r r r
  r r r r  r r r r
}

{
  # === SEAGULL FM: distant bird calls and glinting light ===
  ifm:car=1.0,mod=3.5,idx=2.8,atk=0.005,dec=0.20,sus=0.10,rel=0.40
  o7 v0.14 d1
  f40

  # I–II: Dawn/Morning — no birds yet
  r r r r
  r r r r
  r r r r
  r r r r

  r r r r
  r r r r
  r r r r
  r r r r

  # III: Midday — occasional distant cry
  r r r r
  r r r r
  C_o7 r r r
  r r r r

  r r C_o7 r
  r r r r
  E_o7 r r r
  r r G_o7 r

  # IV: Afternoon — seagulls circling
  C_o7 r E_o7 r
  G_o7 r E_o7 r
  A_o7 r G_o7 r
  C_o7 r r G_o7

  # V: Dusk — last calls fading out
  E_o7 r r r
  C_o7 r r r
  r r r r
  r r r r
}

{
  # === DISTANT BELL BUOY: sparse FM pings on the offbeat ===
  ifm:car=1,mod=4.2,idx=5.0,atk=0.001,dec=0.30,sus=0.0,rel=0.60
  o5 v0.16 d2
  f56

  # I: silent
  r r r r
  r r r r

  # II: first ring
  r r r r
  r r G r

  r r r r
  r r C r

  r r r r
  r r E r

  # III: regular tolling
  r C r r
  r r r A
  r r F r
  r G r r

  r r C r
  r r E r
  r A r r
  r r G r

  # IV: offbeat tolls, lazy
  r r C r
  r E r r
  r r A r
  r r r G

  # V: fading buoy
  r r C r
  r r r r
  r r r r
  r r r r
}
