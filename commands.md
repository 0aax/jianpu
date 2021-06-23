```
### header, all of the following should be put into a [header ...] array
### i.e. [header [title name] [comp name] ...]
[title name]: Title, centered at the top of the first page.
[comp name], [comp name affiliation]: Composer name or composer name and affiliation.
[inst name]: Instrument name
#### end header

[time 4 4]: Time signature
[key 1 C]: Key signature
[tempo 100]: Tempo

[roct 1 2]: Raised octave, in example note 1 is raised 2 octaves.
[loct 1 2]: Lowered octave, in exaomple note 1 is lowered 2 octaves

[bar]: Vertical bar line
[lrpt], [rrpt]: Left and right repeat bars

[ddot 1]: Increases length by 3/4, in example note 1 is extended by 3/4
[dot 1]: Increases length by 1/2, in example note 1 is extened by 1/2

[qvr 1]: quaver, 8th
[sqvr 1]: semiquaver, 16th
[qtr 1]: quarter/crotchet, 1/4th (but plain notes are also by default 1/4th)
[mm 1]: minim, half
[sbrve 1]: semibreve, whole

[sharp 1]: Sharp
[flat 1]: Flat
[nat 1]: Natural

[grace 1]: Grace note
[chord 1 2], [chord 1 2 3], etc.: Chords where each note is separated by a comma.
[trem 1]: Tremolo on note 1.

[fing 1 2]: Fingering instructions. Example shown represents using finger 2 for note 1.
[down 1]: Down strumming/bowing/etc. direction, lines adjusted based on where it is a single note or a chord.
[up 1]: Up _____''_____

[stie 1], [etie 1]: Tie, where \stie starts and \etie ends the tie
[sslur 1], [eslur 1]: Slur, in example the slur starts at 1 and ends at 4.

[p 1]: Piano associated with note 1.
[mp 1]: Mezzo-piano ____''____
[f 1]: Forte ____''____
[mf 1]: Mezzo-forte ____''____
[scresc 1], [ecresc 4]: Crescendo, in example crescendo starts at 1 and ends at 4.
[sdim 4], [edim 1]: Diminuendo/Decrescendo, didn't differentiate between the two :), same pattern as crescendo.

1, 2, ..., 7: Notes
0: Rest
X: Percussion (or placeholder for rhythms without pitch)
```