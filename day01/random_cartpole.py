"""1日目: ランダム方策で CartPole-v1 を 1,000 エピソード動かし、何ステップで倒れるかを数える。"""
import json
import gymnasium as gym
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "Hiragino Kaku Gothic ProN"

N_EPISODES = 1000
SEED = 0

env = gym.make("CartPole-v1")
rng = np.random.default_rng(SEED)
lengths = []
for ep in range(N_EPISODES):
    obs, info = env.reset(seed=SEED + ep)
    steps = 0
    while True:
        action = int(rng.integers(env.action_space.n))  # 左右をコイン投げで選ぶ
        obs, reward, terminated, truncated, info = env.step(action)
        steps += 1
        if terminated or truncated:
            break
    lengths.append(steps)
env.close()

a = np.array(lengths)
stats = {
    "episodes": N_EPISODES,
    "mean": float(a.mean()),
    "median": float(np.median(a)),
    "std": float(a.std()),
    "min": int(a.min()),
    "max": int(a.max()),
    "p90": float(np.percentile(a, 90)),
    "over_100": int((a >= 100).sum()),
    "reached_500": int((a >= 500).sum()),
}
print(json.dumps(stats, ensure_ascii=False, indent=2))
json.dump({"stats": stats, "lengths": lengths}, open("day01/result.json", "w"), ensure_ascii=False)

plt.figure(figsize=(7, 4))
plt.hist(a, bins=range(0, a.max() + 5, 5), color="#098FD3")
plt.xlabel("倒れるまでのステップ数")
plt.ylabel("エピソード数")
plt.title(f"ランダム方策の CartPole-v1（{N_EPISODES}回、平均 {a.mean():.1f} ステップ）")
plt.tight_layout()
plt.savefig("day01/hist.png", dpi=150)
