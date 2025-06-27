from typing import Literal

type RawValue = str | int | float | bool
type ProValue = str | int | bool
type TrialsList = list[dict[str, ProValue]]

type DataFiles = Literal['conditions', 'results raw', 'results processed']
type Scripts = Literal['process', 'analyse']

type TrialParamDict = dict[str, tuple[str, str]]
type RelationshipDict = dict[tuple[str, str], str]
type Interaction = Literal[True, False]
type DependentVariable = Literal['rt', 'response']
