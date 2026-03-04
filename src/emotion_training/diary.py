import json
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import List

from .models import Emotion


@dataclass
class DiaryEntry:
    timestamp: str
    image_path: str
    emotion: Emotion


class VisionClassifier:
    """可替换的视觉分类接口。

    这里先用文件名规则模拟：包含 happy/angry/sad/surprised 关键词。
    """

    @staticmethod
    def classify(image_path: str) -> Emotion:
        name = Path(image_path).name.lower()
        if "happy" in name:
            return Emotion.HAPPY
        if "angry" in name:
            return Emotion.ANGRY
        if "sad" in name:
            return Emotion.SAD
        return Emotion.SURPRISED


class EmotionDiary:
    def __init__(self, storage_file: str = "emotion_diary.json") -> None:
        self.storage_file = Path(storage_file)
        self.entries: List[DiaryEntry] = []
        self._load()

    def add_photo(self, image_path: str) -> DiaryEntry:
        emotion = VisionClassifier.classify(image_path)
        entry = DiaryEntry(
            timestamp=datetime.utcnow().isoformat(),
            image_path=image_path,
            emotion=emotion,
        )
        self.entries.append(entry)
        self._save()
        return entry

    def grouped_summary(self) -> dict:
        summary = {e.value: 0 for e in [Emotion.HAPPY, Emotion.ANGRY, Emotion.SAD, Emotion.SURPRISED]}
        for item in self.entries:
            if item.emotion.value in summary:
                summary[item.emotion.value] += 1
        return summary

    def _save(self) -> None:
        payload = [
            {**asdict(item), "emotion": item.emotion.value}
            for item in self.entries
        ]
        self.storage_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    def _load(self) -> None:
        if not self.storage_file.exists():
            return
        raw = json.loads(self.storage_file.read_text(encoding="utf-8"))
        self.entries = [
            DiaryEntry(timestamp=i["timestamp"], image_path=i["image_path"], emotion=Emotion(i["emotion"]))
            for i in raw
        ]
