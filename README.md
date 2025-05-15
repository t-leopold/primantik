# BA – Semantic Priming Project

## Routinen
Die Proberunde und das eigentliche Experiment nutzen dieselben Routinen. Die Routinen greifen auf dieselben Variablen zu, die allerdings aus zwei unterschiedlichen Stimulus-Dateien gespeist werden – diese Aufgabe übernehmen die Schleifen.

## Stimuli
Die Stimuli sind in zwei Dateien enthalten: `conditions.xlsx` enthält die Stimuli für das eigentliche Experiment und `conditions_test.xlsx` enthält die Stimuli für die Proberunde. Der Aufbau beider Dateien ist ident.

## Texte
Die Schleife mit dem Namen `text` überspannt das gesamte Experiment, um die Einträge der Datei `texts.xlsx` bereitzustellen. Aus diesen beziehen die Textfelder in der Einführung (intro), Überleitung von Versuchsrunde zu eigentlichem Experiment (bridge) und am Ende (end) ihren Inhalt.

## Vorlage
[A novel co-occurrence-based approach to predict pure associative and semantic priming](https://doi.org/10.3758/s13423-018-1453-6)

## To-Do
* define a separate set of stimuli for the test round
* look over stimuli and stimuli sampling for experiment
* check (or at least track) device of participants
