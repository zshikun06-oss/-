from emotion_training.diary import EmotionDiary


def test_diary_add_and_group(tmp_path):
    store = tmp_path / "diary.json"
    diary = EmotionDiary(str(store))
    diary.add_photo("kid_happy_1.png")
    diary.add_photo("kid_sad_1.png")
    summary = diary.grouped_summary()
    assert summary["快乐"] == 1
    assert summary["悲伤"] == 1
