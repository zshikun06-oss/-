# Emotion Training Prototype（运行与使用）

这是一个面向“三级情绪训练系统”概念验证的 Python 原型，包含：
- 训练引擎（Level 1/2/3）
- 情绪日记（本地 JSON 持久化）
- CLI 演示命令
- 单元测试

## 1. 环境要求
- Python 3.10+

## 2. 快速运行
在仓库根目录执行：

```bash
python main.py demo
```

> 说明：`main.py` 已自动加入 `src/` 到 Python 路径，无需手工设置 `PYTHONPATH`。

## 3. 使用情绪日记命令

### 3.1 添加照片记录
```bash
python main.py diary-add sample_happy_face.jpg
```

当前分类器为原型实现：根据文件名关键词分类：
- 包含 `happy` → 快乐
- 包含 `angry` → 愤怒
- 包含 `sad` → 悲伤
- 其他 → 惊讶

也可指定存储文件：
```bash
python main.py diary-add kid_sad_001.png --storage my_diary.json
```

### 3.2 查看统计
```bash
python main.py diary-summary
```

或：
```bash
python main.py diary-summary --storage my_diary.json
```

## 4. 运行测试
```bash
PYTHONPATH=src python -m pytest -q
```

## 5. 程序结构
- `src/emotion_training/models.py`：数据模型与统计结构
- `src/emotion_training/engine.py`：三级训练评估与提示逻辑
- `src/emotion_training/diary.py`：情绪日记与分类器接口
- `main.py`：CLI 入口
- `tests/`：单元测试

## 6. 后续可扩展方向
- 将 `VisionClassifier` 替换为真实云端视觉 API（如 Google Cloud Vision）。
- 增加 Web/API 层，支持前端训练页面接入。
- 扩充策略库与自适应规则（按年龄、能力分层）。
