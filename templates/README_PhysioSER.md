# PhysioSER: Physiology-Informed Vocal Spectrotemporal Representations for Speech Emotion Recognition

[![arXiv](https://img.shields.io/badge/arXiv-2602.13259-b31b1b.svg)](https://arxiv.org/abs/2602.13259)
[![Project page](https://img.shields.io/badge/project-page-blue)](https://codezx6.github.io/papers/physioser.html)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
<!-- After uploading checkpoints: [![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97-model-yellow)](https://huggingface.co/CodeZx6/PhysioSER) -->

Official implementation of **PhysioSER** (Xu Zhang, Longbing Cao, Runze Yang, Zhangkai Wu, 2026), a compact, plug-and-play speech emotion recognition (SER) method that couples vocal **amplitude and phase** through voice anatomy and physiology (VAP), and aligns them with a frozen self-supervised (SSL) speech backbone.

**TL;DR.** Most deep SER models use amplitude only. PhysioSER decomposes speech into physiology-informed amplitude and phase views, embeds them in a quaternion field, models their interaction with Hamilton-structured quaternion convolutions, and aligns the result with SSL features via Contrastive Projection and Alignment. Evaluated on **14 datasets, 10 languages, and 6 SSL backbones**, and deployed in real time on a humanoid robot.

## Highlights

- **Physiology-informed inputs.** Amplitude and phase views derived from the vocal-tract filter and glottal source, not just a mel spectrogram.
- **Quaternion modelling.** Hamilton-structured quaternion convolutions capture the coupled dynamics between amplitude and phase.
- **Plug-and-play.** Works on top of a frozen SSL backbone (e.g. WavLM, HuBERT, wav2vec 2.0) with a shallow attention fusion head.
- **Interpretable and efficient.** Designed for humanoid-robot use cases such as social interaction and psychological assessment.

## Installation

```bash
git clone https://github.com/CodeZx6/PhysioSER.git
cd PhysioSER
conda env create -f environment.yml   # or: pip install -r requirements.txt
```

## Quick start

```bash
# extract VAP amplitude/phase views and run inference on a wav file
python infer.py --wav examples/happy.wav --backbone wavlm-base-plus --ckpt ckpts/physioser_iemocap.pt
```

## Training

```bash
python train.py --config configs/iemocap_wavlm.yaml
```

Supported datasets (see `configs/`): IEMOCAP, MSP-Podcast, CREMA-D, RAVDESS, EmoDB, ... <!-- list the 14 datasets used in the paper -->

## Results

<!-- Paste the main table from the paper (UA / WA per dataset and backbone). Numbers in the README are picked up by search engines and LLM crawlers. -->

## Citation

```bibtex
@article{zhang2026physioser,
  title        = {Learning Physiology-Informed Vocal Spectrotemporal Representations for Speech Emotion Recognition},
  author       = {Zhang, Xu and Cao, Longbing and Yang, Runze and Wu, Zhangkai},
  journal      = {arXiv preprint arXiv:2602.13259},
  year         = {2026},
  eprint       = {2602.13259},
  archivePrefix= {arXiv},
  primaryClass = {cs.SD},
  url          = {https://arxiv.org/abs/2602.13259}
}
```

## Related work by the authors

- [DUET: Unified Dual-Space Emotion Control for Diffusion and Flow-Matching Driven Text-to-Speech](https://arxiv.org/abs/2606.00066) (2026)
- Full publication list and BibTeX: https://codezx6.github.io

## Contact

Xu Zhang · xu.zhang12@hdr.mq.edu.au · [Google Scholar](https://scholar.google.com/citations?user=MnZDgiUAAAAJ) · [ORCID](https://orcid.org/0000-0002-4143-0715)
