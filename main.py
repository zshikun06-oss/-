from emotion_training import (
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

    diary = EmotionDiary()
    entry = diary.add_photo("sample_happy_face.jpg")
    print("[Diary]", entry.emotion.value, diary.grouped_summary())


if __name__ == "__main__":
    demo()
