# jianpu

Temperamental program for [简谱 : jiǎnpǔ](https://en.wikipedia.org/wiki/Numbered_musical_notation) engraving. This program's capabilities are mainly geared towards plucked instruments since I play the 柳琴 : liǔqín.

## Currently Working On
- [ ] Gracenotes

## Todo
- [ ] Fix duration grouping (i broke it somehow)
- [ ] Change direction symbol if used with a chord.
- [ ] Render characters individually to mitigate cross-platform kerning and tracking differences.

## 1. Composition general information
### 1.1 Header-related commands
```
\title{Name}: Title, centered at the top of the first page.
\composer{Name}: Composer name
\affiliation{Institution}: Institutional affiliation
\instrument{Name}: Instrument name
\time{4, 4}: Time signature
\key{1=C}: Key signature
\tempo{100}: Tempo
```
All of the previous commands should wrapped in `\header{...}`. Changes in key or tempo within the composition are not currently implemented (but will be implemented in the future).
```
\header{
    \title{Composition no. 1},
    \composer{0aax},
    \instrument{柳琴},
    \time{4, 4},
    \key{1=C},
    \tempo{100}
}
```
### 1.2 Not strictly relegated to header commands
The time signature will show up anywhere you put it.
```
\bar \time{2, 4} 1 1 \bar
```
## 2. Note-related commands
### 2.1 Representation of notes and/or other rhythms
```
1, 2, ..., 7: Notes
0: Rest
X: Percussion (or placeholder for rhythms without pitch)
-: Extend note
```
### 2.2 Octaves
```
\oct{1, 2}: Raised octave, in example note 1 is raised 2 octaves.
\oct{1, -2}: Lowered octave, in example note 1 is lowered 2 octaves.
```
### 2.3 Duration
```
(1)

\ddot{1}: Increases length by 3/4, in example note 1 is extended by 3/4
\dot{1}: Increases length by 1/2, in example note 1 is extended by 1/2
```
```
(2)

\sqvr{1}: semiquaver, 16th
\qvr{1}: quaver, 8th
\ccht{1}: crotchet, 4th (but plain notes are also by default 4th)
\mm{1}: minim, half
\sbrve{1}: semibreve, whole
```
All duration operators can handle operators applied to notes.
```
\qvr{\oct{4, 1}}
\qvr{\down{\oct{4, 1}}}
\qvr{\fing{\down{\oct{4, 1}}, 2}}
```
Additionally, the operators from `(2)` can take any number notes.
```
\sqvr{1, 2, 3, 4}
```
To group notes of different durations, use `\group{...}`.
```
\group{\qvr{1}, \sqvr{1, 2}}
```
### 2.4 Extensions
The notes starting and ending a tie should be consecutive.
```
\stie{1}, \etie{1}: Tie, where \stie starts and \etie ends the tie
```
Slur placement is determined by the start and end notes. The curve itself will extend above all notes between the location of the start and end of the slur.
```
\sslur{1}, \eslur{4}: Slur, in example the slur starts at 1 and ends at 4.
```
### 2.5 Dynamics
```
\p{1}: Piano associated with note 1.
\mp{1}: Mezzo-piano ____''____
\f{1}: Forte ____''____
\mf{1}: Mezzo-forte ____''____
```
The placement of dynamic changes are determined by their start and end notes.
```
\scresc{1}, \ecresc{4}: Crescendo, in example crescendo starts at 1 and ends at 4.
\sdim{4}, \edim{1}: Diminuendo/Decrescendo, didn't differentiate between the two :)
```
### 2.6 Additional modifiers
```
\grace{1}: Grace note
```
The `\grace` operator can handle any number of notes as well as duration and direction operators.
```
\grace{\sqvr{\down{\oct{1, 1}}, \up{\oct{2, 1}}}}
```
```
\chord{1, 2}, \chord{1, 2, 3}, etc.: Chords where each note is separated by a comma.
\trem{1}: Tremolo on note 1.
```
### 2.7 Miscellaneous notation
Fingering instructions will appear on the upper left corner of the note.
```
\fing{1, 2}: Fingering instructions. Example shown represents using finger 2 for note 1.
```
Direction for a single note is represented as a single forward or backslash. For chords, the forward or backslash will additionally have smaller perpendicular dashes.
```
\down{1}: Down strumming/bowing/etc. direction
\up{1}: Up _____''_____
```
## 3. Measures and bars
### 3.1 Bars
```
\bar: Single bar line
\dbar: Double bar line
\ebar: End bar line, placed by default at the end of a composition
\lrep, \rrep: Left and right repeat bars
```