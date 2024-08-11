# Recursive Contemplation (ReCon)

Shenzhi Wang*, Chang Liu*, Zilong Zheng†, Siyuan Qi, Shuo Chen, Qisen Yang, Andrew Zhao, Chaofei Wang, Shiji Song, Gao Huang†

*: Equal Contribution, †: Corresponding Authors

## 1. Introduction

This repository is the official source code for [*Boosting LLM Agents with Recursive Contemplation for Effective Deception Handling*](https://openreview.net/pdf?id=tw5yAlP1ne) (ACL 2024, Findings). 

![](imgs/teaser.png)

The figure above is the illustrative framework of our proposed Recursive Contemplation (ReCon) with the Avalon game as an example. Specifically, ReCon presents a cognitive process with two stages: contemplation of formulation and refinement, each associated with first-order and second-order perspective transition, respectively.

[Project Page](https://shenzhi-wang.github.io/avalon_recon/) | [Chinese Report by Synced (机器之心)](https://mp.weixin.qq.com/s/TglUikgaQe17XTP29cF9Uw) | [Chinese Report by AI Era (新智元)](https://mp.weixin.qq.com/s/lf5tMVLuWjRAzADLgxdVig) | [Chinese Report by QbitAI (量子位)](https://mp.weixin.qq.com/s/wxBzWBC_aCJPgpstrDBJgw)

## 2. Installation

The python version used in our experiments is `3.9.17`.

```bash
git clone https://github.com/Shenzhi-Wang/recon.git
cd recon
pip install -r requirements.txt 
```

## 3. Usage

### 3.1 Add you API key

Change the `gpt_api_key` in [api_config.py](api_config.py) to your own API key.

### 3.2 Play Avalon games!

In the following, `N_ROUNDS` is the number of game repetitions.

1. CoT (as the good side) v.s. CoT (as the evil side):

```bash
./scripts/run_exp.sh baseline_gpt baseline_gpt ${N_ROUNDS}
```

2. ReCon (as the good side) v.s. CoT (as the evil side):

```bash
./scripts/run_exp.sh ours_gpt baseline_gpt ${N_ROUNDS}
```

3. ReCon (as the good side) v.s. ReCon (as the evil side):

```bash
./scripts/run_exp.sh ours_gpt ours_gpt ${N_ROUNDS}
```

4. CoT (as the good side) v.s. ReCon (as the evil side):

```bash
./scripts/run_exp.sh baseline_gpt ours_gpt ${N_ROUNDS}
```

The logs of Avalon games will be saved at `game_history.csv` under the `logs` directory.


## Citation
We would greatly appreciate it if you could cite our work!

```
@inproceedings{
wang2024boosting,
title={Boosting LLM Agents with Recursive Contemplation for Effective Deception Handling},
author={Wang, Shenzhi and Liu, Chang and Zheng, Zilong and Qi, Siyuan and Chen, Shuo and Yang, Qisen and Zhao, Andrew and Wang, Chaofei and Song, Shiji and Huang, Gao},
booktitle={The 62nd Annual Meeting of the Association for Computational Linguistics},
year={2024},
url={https://openreview.net/forum?id=tw5yAlP1ne}
}
```
