from emotion_training import Emotion, EmotionTrainingEngine, Level1Question, Level2Task, Level3Scenario


def test_level1_eval():
    engine = EmotionTrainingEngine()
    q = Level1Question("1", "", [Emotion.HAPPY], Emotion.HAPPY)
    assert engine.evaluate_level1(q, Emotion.HAPPY, 1000) is True
    assert engine.level1_stats.accuracy == 1.0


def test_level2_feedback():
    engine = EmotionTrainingEngine()
    t = Level2Task(Emotion.ANGRY, "")
    result = engine.evaluate_level2_similarity(t, Emotion.ANGRY, 0.8)
    assert result["pass"] == "yes"


def test_level3_hint_trigger():
    engine = EmotionTrainingEngine()
    s = Level3Scenario(
        scene_id="x",
        text="",
        candidate_emotions=[Emotion.SAD, Emotion.DISAPPOINTED],
        inferred_primary=Emotion.DISAPPOINTED,
        strategies=["a"],
        adaptive_strategies=["a"],
    )
    ok, _ = engine.infer_level3(s, Emotion.SAD, "a", reaction_ms=9000)
    hint = engine.maybe_trigger_hint(9000, ok)
    assert hint.need_hint is True
