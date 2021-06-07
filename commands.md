```
\title{name}: Title, centered at the top of the first page.
\composer{name}, \composer{name, affliliation}: Composer name or composer name and affiliation.
\instrument{name}: Instrument name

\time{4}{4}: Time signature
\key{1}{C}: Key signature
\tempo{100}: Tempo

\raiseoct{1}{2}: Raised octave, in example note 1 is raised 2 octaves.
\loweroct{1}{2}: Lowered octave, in exaomple note 1 is lowered 2 octaves

\bar: Vertical bar line
\lrepeat, \rrepeat: Left and right repeat bars

\doubledot{1}: Increases length by 3/4
\dot{1}: Increased length by 1/2

\quaver{1}: 8th
\semiquaver{1}: 16th
\crochet{1}: 1/4th (but plain notes are also by default 1/4th)
\minim{1}: 1/2th
\semibreve{1}: Whole

\sharp{1}: Sharp
\flat{1}: Flat
\natural{1}: Natural

\grace{1}: Grace note
\chord{1}{2}, \chord{1}{2}{3}, etc.: Chords where each note is separated by a comma.
\trem{1}: Tremolo on note 1.

\finger{1}{2}: Fingering instructions. Example shown represents using finger 2 for note 1.
\down{1}: Down strumming/Bowing/etc. direction, lines adjusted based on where it is a single note or a chord.
\up{1}: Up _____''_____

\stie{1}, \etie{1}: Tie, where \stie starts and \etie ends the tie
\sslur{1}, \eslur{4}: Slur. In the example, the slur starts at 1 and ends at 4.

\p{1}: Piano associated with note 1.
\mp{1}: Mezzo-piano ____''____
\f{1}: Forte ____''____
\mf{1}: Mezzo-forte ____''____
\scresc{1}, \ecresc{4}: Crescendo, in example crescendo starts at 1 and ends at 4.
\sdim{4}, \edim{1}: Diminuendo/Decrescendo, didn't differentiate between the two :), same pattern as crescendo.

1, 2, ..., 7: Notes
0: Rest
X: Percussion (or placeholder for rhythms without pitch)
```