from dataclasses import dataclass
from typing import Dict, Tuple

from .models import Emotion, Level1Question, Level2Task, Level3Scenario, SessionStats


@dataclass
class HintResult:
    need_hint: bool
    hint_text: str


class EmotionTrainingEngine:
    """三级训练原型引擎。"""

    def __init__(self) -> None:
        self.level1_stats = SessionStats()
        self.level2_stats = SessionStats()
        self.level3_stats = SessionStats()
        self._consecutive_level3_errors = 0

    def evaluate_level1(self, question: Level1Question, selected: Emotion, reaction_ms: int) -> bool:
        self.level1_stats.total += 1
        self.level1_stats.reaction_times_ms.append(reaction_ms)
        ok = selected == question.answer
        if ok:
            self.level1_stats.correct += 1
        else:
            self.level1_stats.confusions.append(f"{question.answer.value}->{selected.value}")
        return ok

    def evaluate_level2_similarity(self, task: Level2Task, predicted_emotion: Emotion, score: float) -> Dict[str, str]:
        self.level2_stats.total += 1
        ok = (predicted_emotion == task.target_emotion and score >= 0.70)
        if ok:
            self.level2_stats.correct += 1
            feedback = "模仿很接近示范表情，做得很好。"
        elif predicted_emotion == task.target_emotion:
            feedback = "情绪方向正确，再加强眉眼和嘴角细节。"
        else:
            feedback = f"识别到{predicted_emotion.value}，尝试更突出{task.target_emotion.value}的关键表情线索。"
            self.level2_stats.confusions.append(f"{task.target_emotion.value}->{predicted_emotion.value}")
        return {
            "pass": "yes" if ok else "no",
            "feedback": feedback,
            "similarity": f"{score:.2f}",
        }

    def infer_level3(self, scenario: Level3Scenario, selected_emotion: Emotion, chosen_strategy: str, reaction_ms: int) -> Tuple[bool, str]:
        self.level3_stats.total += 1
        self.level3_stats.reaction_times_ms.append(reaction_ms)
        ok = selected_emotion == scenario.inferred_primary

        if ok:
            self.level3_stats.correct += 1
            self._consecutive_level3_errors = 0
            emotion_feedback = f"你识别出了主要情绪：{selected_emotion.value}。"
        else:
            self._consecutive_level3_errors += 1
            self.level3_stats.confusions.append(f"{scenario.inferred_primary.value}->{selected_emotion.value}")
            emotion_feedback = (
                f"这个场景更可能是{scenario.inferred_primary.value}，"
                f"你选的是{selected_emotion.value}。"
            )

        if chosen_strategy in scenario.adaptive_strategies:
            strategy_feedback = "你选择了更有助于沟通的回应策略。"
        else:
            strategy_feedback = "这个策略可能会让沟通变难，可以尝试更温和表达。"

        return ok, f"{emotion_feedback}{strategy_feedback}"

    def maybe_trigger_hint(self, reaction_ms: int, last_correct: bool) -> HintResult:
        # 规则示例：反应过慢或连续错误时给弱提示
        slow = reaction_ms > 8000
        repeat_errors = (not last_correct and self._consecutive_level3_errors >= 2)
        if slow or repeat_errors:
            self.level3_stats.hints_used += 1
            return HintResult(True, "提示：关注人物的眼睛、嘴角和身体朝向。")
        return HintResult(False, "")
