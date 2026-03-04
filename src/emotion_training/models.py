from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class Emotion(str, Enum):
    HAPPY = "快乐"
    ANGRY = "愤怒"
    SAD = "悲伤"
    SURPRISED = "惊讶"
    NERVOUS = "紧张"
    DISAPPOINTED = "失落"


@dataclass
class Level1Question:
    image_id: str
    prompt: str
    options: List[Emotion]
    answer: Emotion


@dataclass
class Level2Task:
    target_emotion: Emotion
    description: str


@dataclass
class Level3Scenario:
    scene_id: str
    text: str
    candidate_emotions: List[Emotion]
    inferred_primary: Emotion
    strategies: List[str]
    adaptive_strategies: List[str]


@dataclass
class SessionStats:
    total: int = 0
    correct: int = 0
    hints_used: int = 0
    reaction_times_ms: List[int] = field(default_factory=list)
    confusions: List[str] = field(default_factory=list)

    @property
    def accuracy(self) -> float:
        return self.correct / self.total if self.total else 0.0

    @property
    def avg_reaction_ms(self) -> Optional[float]:
        if not self.reaction_times_ms:
            return None
        return sum(self.reaction_times_ms) / len(self.reaction_times_ms)
