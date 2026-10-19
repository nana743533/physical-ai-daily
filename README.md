# physical-ai-daily

Physical AI を毎日1本ずつ書く技術発信の、実験コードと結果の置き場です。記事は [Qiita](https://qiita.com/nana743533) に出しています。

日ごとにフォルダを分けています。各フォルダに、その日に動かしたスクリプト、結果（`result.json`）、図が入っています。

## 第1期: 強化学習の2週間（2026-10-20 〜）

倒立振子（CartPole）で表の Q 学習から DQN まで、そのあと連続行動の Pendulum と MuJoCo の2リンクアーム（Reacher）で方策勾配から PPO までをやり、14日目にアームが目標に届くところまでを書きます。

| 日 | 内容 | フォルダ |
|---|---|---|
| 1 | ランダム方策の CartPole。平均 22.2 ステップで倒れる | [day01](day01) |

## 動かし方

```bash
uv sync
uv run python day01/random_cartpole.py
```

Python 3.12、Gymnasium 1.4、MuJoCo 3.16、Stable-Baselines3 2.9、PyTorch 2.14 で動かしています。
