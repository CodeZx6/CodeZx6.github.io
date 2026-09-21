# Additions for the five existing code repos

Paste the matching block at the **top** of each README (badges + one-line description + links), and replace the existing BibTeX with the DOI-bearing version. Then set the repo **description**, **website** and **topics** in GitHub → repo → ⚙ "About". Topics are indexed by GitHub search, Google, and the crawlers behind ChatGPT/Perplexity.

---

## CodeZx6/MCSTL

**Description:** Code for "Mask- and Contrast-Enhanced Spatio-Temporal Learning for Urban Flow Prediction" (CIKM 2023)
**Website:** https://codezx6.github.io/papers/mcstl.html
**Topics:** urban-flow-prediction, spatio-temporal, contrastive-learning, masked-pretraining, traffic-prediction, cikm2023, pytorch

```markdown
[![DOI](https://img.shields.io/badge/DOI-10.1145%2F3583780.3614958-blue)](https://doi.org/10.1145/3583780.3614958)
[![PDF](https://img.shields.io/badge/PDF-open%20access-brightgreen)](https://dl.acm.org/doi/pdf/10.1145/3583780.3614958)
[![Project page](https://img.shields.io/badge/project-page-blue)](https://codezx6.github.io/papers/mcstl.html)

Official PyTorch implementation of **MCSTL** (CIKM 2023, pp. 3298–3307). MCSTL pre-trains an urban flow model with a mask-reconstruction task across space and time and a graph-based contrastive task that weights regions by inter-regional attention, then fine-tunes for flow prediction.
```

```bibtex
@inproceedings{zhang2023mcstl,
  title     = {Mask- and Contrast-Enhanced Spatio-Temporal Learning for Urban Flow Prediction},
  author    = {Zhang, Xu and Gong, Yongshun and Zhang, Xinxin and Wu, Xiaoming and Zhang, Chengqi and Dong, Xiangjun},
  booktitle = {Proceedings of the 32nd ACM International Conference on Information and Knowledge Management (CIKM '23)},
  year      = {2023},
  pages     = {3298--3307},
  publisher = {ACM},
  doi       = {10.1145/3583780.3614958}
}
```

---

## CodeZx6/ST-CSL

**Description:** Code for "Spatio-temporal fusion and contrastive learning for urban flow prediction" (Knowledge-Based Systems 2023)
**Website:** https://codezx6.github.io/papers/st-csl.html
**Topics:** urban-flow-prediction, contrastive-learning, spatio-temporal-fusion, traffic-prediction, knowledge-based-systems, pytorch

```markdown
[![DOI](https://img.shields.io/badge/DOI-10.1016%2Fj.knosys.2023.111104-blue)](https://doi.org/10.1016/j.knosys.2023.111104)
[![Project page](https://img.shields.io/badge/project-page-blue)](https://codezx6.github.io/papers/st-csl.html)
```

```bibtex
@article{zhang2023stcsl,
  title   = {Spatio-temporal fusion and contrastive learning for urban flow prediction},
  author  = {Zhang, Xu and Gong, Yongshun and Zhang, Chengqi and Wu, Xiaoming and Guo, Ying and Lu, Wenpeng and Zhao, Long and Dong, Xiangjun},
  journal = {Knowledge-Based Systems},
  year    = {2023},
  volume  = {282},
  pages   = {111104},
  doi     = {10.1016/j.knosys.2023.111104}
}
```

---

## CodeZx6/MR-UPF

**Description:** Code for "Enhancing urban flow prediction via mutual reinforcement with multi-scale regional information" (Neural Networks 2025)
**Website:** https://codezx6.github.io/papers/mr-ufp.html
**Topics:** urban-flow-prediction, contrastive-pretraining, multi-task-learning, spatial-temporal-heterogeneity, neural-networks-journal, pytorch

```markdown
[![DOI](https://img.shields.io/badge/DOI-10.1016%2Fj.neunet.2024.106900-blue)](https://doi.org/10.1016/j.neunet.2024.106900)
[![Project page](https://img.shields.io/badge/project-page-blue)](https://codezx6.github.io/papers/mr-ufp.html)

Official implementation of **MR-UFP** (Neural Networks, vol. 182, 2025). MR-UFP pre-trains with spatial-temporal random masking and contrastive learning, then jointly trains the predictor with a multi-scale region-classification auxiliary task so spatial features and flow prediction reinforce each other; it is robust on small or noisy datasets.
```

```bibtex
@article{zhang2025mrufp,
  title   = {Enhancing urban flow prediction via mutual reinforcement with multi-scale regional information},
  author  = {Zhang, Xu and Cao, Mengxin and Gong, Yongshun and Wu, Xiaoming and Dong, Xiangjun and Guo, Ying and Zhao, Long and Zhang, Chengqi},
  journal = {Neural Networks},
  year    = {2025},
  volume  = {182},
  pages   = {106900},
  doi     = {10.1016/j.neunet.2024.106900}
}
```

---

## CodeZx6/BiST-IF

**Description:** Code for "Enhancing origin–destination flow prediction via bi-directional spatio-temporal inference and interconnected feature evolution" (ESWA 2025)
**Website:** https://codezx6.github.io/papers/bist-if.html
**Topics:** origin-destination-prediction, od-matrix, metro-passenger-flow, bidirectional-attention, mutual-information, hzmetro, nyc-taxi, pytorch

```markdown
[![DOI](https://img.shields.io/badge/DOI-10.1016%2Fj.eswa.2024.125679-blue)](https://doi.org/10.1016/j.eswa.2024.125679)
[![Project page](https://img.shields.io/badge/project-page-blue)](https://codezx6.github.io/papers/bist-if.html)
```

```bibtex
@article{yu2025bistif,
  title   = {Enhancing origin--destination flow prediction via bi-directional spatio-temporal inference and interconnected feature evolution},
  author  = {Yu, Piao and Zhang, Xu and Gong, Yongshun and Zhang, Jian and Sun, Haoliang and Zhang, Junjie and Zhang, Xinxin and Yin, Yilong},
  journal = {Expert Systems with Applications},
  year    = {2025},
  volume  = {264},
  pages   = {125679},
  doi     = {10.1016/j.eswa.2024.125679}
}
```

---

## CodeZx6/DSTCN

**Description:** Code for "Exploiting dynamic spatio-temporal correlations for origin-destination demand prediction" (ESWA 2026, open access)
**Website:** https://codezx6.github.io/papers/dstcn.html
**Topics:** origin-destination-prediction, metro-od-matrix, graph-convolution, attention, spatio-temporal, pytorch

```markdown
[![DOI](https://img.shields.io/badge/DOI-10.1016%2Fj.eswa.2025.130095-blue)](https://doi.org/10.1016/j.eswa.2025.130095)
[![Open access](https://img.shields.io/badge/open%20access-CC%20BY-brightgreen)](https://doi.org/10.1016/j.eswa.2025.130095)
[![Project page](https://img.shields.io/badge/project-page-blue)](https://codezx6.github.io/papers/dstcn.html)
```

```bibtex
@article{gong2026dstcn,
  title   = {Exploiting dynamic spatio-temporal correlations for origin-destination demand prediction},
  author  = {Gong, Yongshun and Yu, Piao and Zhang, Xu and Zhang, Xinxin and Nie, Xiushan and Sun, Haoliang},
  journal = {Expert Systems with Applications},
  year    = {2026},
  volume  = {299},
  pages   = {130095},
  doi     = {10.1016/j.eswa.2025.130095}
}
```

---

## GitHub profile README (new repo `CodeZx6/CodeZx6`)

Create a public repo named exactly `CodeZx6` with this `README.md`; it shows on https://github.com/CodeZx6 and is crawled heavily.

```markdown
### Xu Zhang (张旭)

PhD candidate, School of Computing, Macquarie University. I work on **speech emotion recognition**, **emotion-controllable text-to-speech** for diffusion / flow-matching models, and **spatio-temporal prediction** for urban mobility.

🌐 https://codezx6.github.io · 🎓 [Google Scholar](https://scholar.google.com/citations?user=MnZDgiUAAAAJ) · 🆔 [ORCID 0000-0002-4143-0715](https://orcid.org/0000-0002-4143-0715)

**Recent**
- [DUET](https://arxiv.org/abs/2606.00066): plug-and-play emotion control for pretrained diffusion / flow-matching TTS · [demo](https://codezx6.github.io/duet-demo-fresh/)
- [PhysioSER](https://arxiv.org/abs/2602.13259): physiology-informed speech emotion recognition, 14 datasets, 10 languages
- Urban flow & OD prediction: [MCSTL](https://github.com/CodeZx6/MCSTL) (CIKM 2023), [ST-CSL](https://github.com/CodeZx6/ST-CSL) (KBS 2023), [MR-UPF](https://github.com/CodeZx6/MR-UPF) (Neural Networks 2025), [BiST-IF](https://github.com/CodeZx6/BiST-IF), [DSTCN](https://github.com/CodeZx6/DSTCN) (ESWA)
```
