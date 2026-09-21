# Social post drafts (edit numbers/names before posting; every claim below comes from the papers' abstracts)

## X / Twitter thread — DUET

1/ Diffusion & flow-matching TTS sound great but you can't *tell them how to feel*. Emotion is tangled up with speaker identity.
We found emotion is a **linearly decodable direction** in their frozen hidden states, nearly orthogonal to speaker identity. 🧵

2/ That gives us DUET: plug-and-play emotion control for *pretrained* diffusion / flow-matching TTS. No fine-tuning.
One per-step update = hidden-space steering (move along the emotion direction) + mel-space guidance (gradients through a differentiable vocoder).

3/ Tested on 5 architecturally different backbones × 3 datasets. Beats 10 supervised emotional-TTS baselines and gets the highest human-rated emotion appropriateness.

4/ We also put it on an Ameca humanoid robot. 🎧 Listen: https://codezx6.github.io/duet-demo-fresh/
📄 arXiv: https://arxiv.org/abs/2606.00066
w/ Longbing Cao, Zhangkai Wu @ Macquarie University

## X / Twitter thread — PhysioSER

1/ Most deep speech-emotion models only look at *amplitude*. Voice physiology says emotion also lives in the *phase*, via the vocal-tract filter and glottal source.
PhysioSER couples both. 🧵

2/ Physiology-informed amplitude + phase views → quaternion field → Hamilton-structured quaternion convolutions, aligned with a frozen SSL backbone (Contrastive Projection & Alignment) + a shallow attention head. Compact, plug-and-play, interpretable.

3/ Evaluated on 14 datasets, 10 languages, 6 SSL backbones, and running in real time on a humanoid robot.
📄 https://arxiv.org/abs/2602.13259

## LinkedIn (one post, both papers)

Two preprints from my PhD at Macquarie University on affective speech for humanoid robots:

🔊 DUET (arXiv:2606.00066) adds fine-grained, training-free emotion control to pretrained diffusion and flow-matching TTS. Key finding: emotion is a linearly decodable direction in the hidden states, nearly orthogonal to speaker identity. Validated on 5 backbones and 3 datasets against 10 supervised baselines, and deployed on an Ameca robot. Demo: https://codezx6.github.io/duet-demo-fresh/

🎙️ PhysioSER (arXiv:2602.13259) is a physiology-informed speech emotion recognizer that couples vocal amplitude and phase with quaternion convolutions on top of frozen self-supervised models. Evaluated across 14 datasets and 10 languages.

Papers, code and BibTeX: https://codezx6.github.io
With Longbing Cao, Zhangkai Wu, and Runze Yang.
#SpeechSynthesis #TTS #SpeechEmotionRecognition #AffectiveComputing #HumanoidRobots

## 知乎 / 微信公众号 — DUET（中文）

**标题：** 不用微调，给任何 Diffusion / Flow-Matching TTS 加上情感控制：DUET

现在的扩散式和流匹配式 TTS 自然度很高，但基本没有显式的情感控制，因为情感信息和说话人身份纠缠在一起。

我们发现：在这些模型冻结的隐状态里，**情感是一个线性可解码的方向，而且几乎与说话人身份方向正交**。基于这一点，我们提出 DUET，一个即插即用的情感控制框架，直接作用在预训练模型上，不需要重新训练。

生成时每一步只做一次更新，同时在两个空间干预：
- 隐空间 steering：沿目标情感方向平移隐状态；
- Mel 空间 guidance：通过可微分 vocoder 反传梯度，细化频谱细节。

在 5 个结构不同的预训练 TTS 骨干和 3 个数据集上，DUET 超过了 10 个有监督情感 TTS 基线，并在人工评测中获得最高的情感恰当性评分。我们还把它部署在 Ameca 人形机器人上，让机器人说出富有情感的语音。

- 论文：https://arxiv.org/abs/2606.00066
- 试听：https://codezx6.github.io/duet-demo-fresh/
- 主页与引用：https://codezx6.github.io/papers/duet.html

## 知乎 / 微信公众号 — PhysioSER（中文）

**标题：** 语音情感识别为什么只看幅度不够？PhysioSER：把发声生理学装进模型

主流的深度语音情感识别（SER）模型几乎只用幅度谱。但嗓音生理学研究表明，情感同时体现在**幅度和相位**的动态上，二者通过声道滤波器和声门源相互耦合。

PhysioSER 把这一先验做进模型：
1. 基于发声解剖与生理（VAP）构造幅度视图和相位视图；
2. 把它们嵌入四元数空间，用 Hamilton 结构的四元数卷积建模二者的动态交互；
3. 与冻结的自监督语音模型（SSL）分支通过对比投影对齐（Contrastive Projection and Alignment）融合，再接一个浅层注意力分类头。

模型紧凑、即插即用、可解释。我们在 14 个数据集、10 种语言、6 种 SSL 骨干上做了评测，并在人形机器人上做了实时部署。

- 论文：https://arxiv.org/abs/2602.13259
- 主页与引用：https://codezx6.github.io/papers/physioser.html

## 知乎 — 城市流量 / OD 预测系列（中文，一篇合集）

**标题：** 从 MCSTL 到 DSTCN：我们在城市流量与 OD 需求预测上的五篇工作（附代码）

- MCSTL（CIKM 2023）：时空掩码重建预训练 + 基于区域注意力的图对比学习。代码 https://github.com/CodeZx6/MCSTL
- ST-CSL（Knowledge-Based Systems 2023）：时间视图与空间视图的对比学习融合，捕捉全局周期性与相似功能区之间的隐含关联。代码 https://github.com/CodeZx6/ST-CSL
- MR-UFP（Neural Networks 2025）：时空随机掩码 + 对比预训练，再用多尺度区域分类辅助任务与流量预测互相增强，小数据/噪声数据下更稳。代码 https://github.com/CodeZx6/MR-UPF
- BiST-IF（Expert Systems with Applications 2025）：OD 延迟校正、双向注意力、OD 与到达 OD（Out-OD）的互信息特征演化；在 HZMetro 与 NYC-TOD2018 上评测。代码 https://github.com/CodeZx6/BiST-IF
- DSTCN（Expert Systems with Applications 2026，开放获取）：动态时空相关性建模用于地铁 OD 需求预测。代码 https://github.com/CodeZx6/DSTCN

全部论文与 BibTeX：https://codezx6.github.io
