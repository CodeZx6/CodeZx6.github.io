---
language:
  - en
  - multilingual
license: mit
library_name: pytorch
pipeline_tag: audio-classification
tags:
  - speech-emotion-recognition
  - audio
  - quaternion-neural-network
  - self-supervised-learning
  - wavlm
  - humanoid-robot
datasets:
  - iemocap
  # add the other 13 datasets
metrics:
  - accuracy
  - f1
arxiv: 2602.13259
---

# PhysioSER

Physiology-informed vocal spectrotemporal representations for speech emotion recognition.
Paper: https://arxiv.org/abs/2602.13259 · Code: https://github.com/CodeZx6/PhysioSER · Project page: https://codezx6.github.io/papers/physioser.html

## Model description

PhysioSER couples vocal amplitude and phase through voice anatomy and physiology (VAP): speech is decomposed into physiology-informed amplitude and phase views, embedded in a quaternion field, modelled with Hamilton-structured quaternion convolutions, and aligned with a frozen self-supervised backbone via Contrastive Projection and Alignment. A shallow attention fusion head performs emotion classification.

## Intended use

Utterance-level emotion classification for social robots, conversational agents, and affective computing research. Not intended for clinical diagnosis without human oversight.

## How to use

```python
from physioser import PhysioSER
model = PhysioSER.from_pretrained("CodeZx6/PhysioSER-wavlm-iemocap")
print(model.predict("examples/happy.wav"))
```

## Evaluation

Evaluated across 14 datasets, 10 languages, and 6 SSL backbones. <!-- paste the main table -->

## Citation

```bibtex
@article{zhang2026physioser,
  title   = {Learning Physiology-Informed Vocal Spectrotemporal Representations for Speech Emotion Recognition},
  author  = {Zhang, Xu and Cao, Longbing and Yang, Runze and Wu, Zhangkai},
  journal = {arXiv preprint arXiv:2602.13259},
  year    = {2026}
}
```
