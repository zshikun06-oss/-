import argparse
import json
import sys
from pathlib import Path

# 允许直接 `python main.py` 运行（无需手动设置 PYTHONPATH）
ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from emotion_training import (  # noqa: E402
    Emotion,
    EmotionDiary,
    EmotionTrainingEngine,
    Level1Question,
    Level2Task,
    Level3Scenario,
)


def demo() -> None:
    engine = EmotionTrainingEngine()

    q1 = Level1Question(
        image_id="l1_001",
        prompt="这个表情是什么情绪？",
        options=[Emotion.HAPPY, Emotion.SAD, Emotion.ANGRY],
        answer=Emotion.HAPPY,
    )
    print("[L1]", engine.evaluate_level1(q1, Emotion.HAPPY, reaction_ms=2300))

    t2 = Level2Task(target_emotion=Emotion.SURPRISED, description="模仿惊讶")
    print("[L2]", engine.evaluate_level2_similarity(t2, Emotion.SURPRISED, score=0.76))

    s3 = Level3Scenario(
        scene_id="s3_001",
        text="小明举手很久，老师没点到他。",
        candidate_emotions=[Emotion.SAD, Emotion.DISAPPOINTED, Emotion.ANGRY],
        inferred_primary=Emotion.DISAPPOINTED,
        strategies=["等一等再举手", "告诉老师自己的想法", "生气地离开"],
        adaptive_strategies=["告诉老师自己的想法", "等一等再举手"],
    )
    ok, feedback = engine.infer_level3(s3, Emotion.SAD, "告诉老师自己的想法", reaction_ms=9200)
    hint = engine.maybe_trigger_hint(reaction_ms=9200, last_correct=ok)
    print("[L3]", ok, feedback)
    if hint.need_hint:
        print("[Hint]", hint.hint_text)


def cmd_diary_add(args: argparse.Namespace) -> None:
    diary = EmotionDiary(storage_file=args.storage)
    entry = diary.add_photo(args.image)
    print(json.dumps({"image": entry.image_path, "emotion": entry.emotion.value, "timestamp": entry.timestamp}, ensure_ascii=False))


def cmd_diary_summary(args: argparse.Namespace) -> None:
    diary = EmotionDiary(storage_file=args.storage)
    print(json.dumps(diary.grouped_summary(), ensure_ascii=False, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="AI辅助情绪训练系统原型 CLI")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("demo", help="运行三级训练演示")

    diary_add = sub.add_parser("diary-add", help="向情绪日记添加一张照片")
    diary_add.add_argument("image", help="图片路径（当前由文件名关键词模拟分类）")
    diary_add.add_argument("--storage", default="emotion_diary.json", help="日记存储JSON文件")

    diary_summary = sub.add_parser("diary-summary", help="输出情绪日记统计")
    diary_summary.add_argument("--storage", default="emotion_diary.json", help="日记存储JSON文件")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command in (None, "demo"):
        demo()
    elif args.command == "diary-add":
        cmd_diary_add(args)
    elif args.command == "diary-summary":
        cmd_diary_summary(args)
    else:
        parser.error(f"未知命令: {args.command}")


if __name__ == "__main__":
    main()
