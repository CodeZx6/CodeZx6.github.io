# DUET: Unified Dual-Space Emotion Control for Diffusion and Flow-Matching Driven Text-to-Speech

[![arXiv](https://img.shields.io/badge/arXiv-2606.00066-b31b1b.svg)](https://arxiv.org/abs/2606.00066)
[![Demo](https://img.shields.io/badge/audio-demo-orange)](https://codezx6.github.io/duet-demo-fresh/)
[![Project page](https://img.shields.io/badge/project-page-blue)](https://codezx6.github.io/papers/duet.html)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

Official implementation of **DUET** (Xu Zhang, Longbing Cao, Zhangkai Wu, 2026): **training-free, plug-and-play emotion control** for pretrained diffusion and flow-matching text-to-speech (TTS) models.

**TL;DR.** Emotion is a *linearly decodable direction* in the frozen hidden states of diffusion/flow-matching TTS models, nearly orthogonal to speaker identity. DUET exploits this with a single per-step update that combines **hidden-space steering** (shift along the emotion direction) and **mel-space guidance** (gradients from a differentiable vocoder). No fine-tuning of the backbone.

🔊 **Listen:** https://codezx6.github.io/duet-demo-fresh/

## Highlights

- Works on **five architecturally different pretrained TTS backbones** <!-- name them: e.g. F5-TTS, CosyVoice 2, ... --> across **three datasets**.
- Outperforms **10 supervised emotional-TTS baselines** and achieves the highest human-rated emotion appropriateness.
- Deployed on an **Ameca humanoid robot** for expressive spoken interaction.

## Installation

```bash
git clone https://github.com/CodeZx6/DUET.git && cd DUET
pip install -r requirements.txt
```

## Usage

```bash
# 1) fit the emotion direction for a backbone (one-off, a few minutes)
python fit_direction.py --backbone f5tts --data data/esd --emotion happy
# 2) synthesise with emotion control
python synth.py --backbone f5tts --text "I can't believe we won!" --emotion happy --alpha 1.0 --mel_guidance 0.3
```

## Results

<!-- Paste the main objective table (emotion accuracy, WER, speaker similarity) and MOS table. -->

## Citation

```bibtex
@article{zhang2026duet,
  title        = {{DUET}: Unified Dual-Space Emotion Control for Diffusion and Flow-Matching Driven Text-to-Speech},
  author       = {Zhang, Xu and Cao, Longbing and Wu, Zhangkai},
  journal      = {arXiv preprint arXiv:2606.00066},
  year         = {2026},
  eprint       = {2606.00066},
  archivePrefix= {arXiv},
  primaryClass = {cs.SD},
  url          = {https://arxiv.org/abs/2606.00066}
}
```

## Related

- [PhysioSER](https://arxiv.org/abs/2602.13259): physiology-informed speech emotion recognition by the same authors.
- Full publication list and BibTeX: https://codezx6.github.io

## Contact

Xu Zhang · xu.zhang12@hdr.mq.edu.au · [Google Scholar](https://scholar.google.com/citations?user=MnZDgiUAAAAJ) · [ORCID](https://orcid.org/0000-0002-4143-0715)
