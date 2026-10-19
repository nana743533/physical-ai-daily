"""2日目: 1日目の 1,000 エピソード（ランダム方策の CartPole-v1）から、割引率 γ ごとの収益を計算して比べる。

CartPole は 1 ステップ耐えるごとに報酬 1 なので、長さ L のエピソードの収益は
    G = 1 + γ + γ^2 + ... + γ^(L-1)
になる。γ = 1.0 なら G = L、γ < 1 なら G = (1 - γ^L) / (1 - γ)。
"""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "Hiragino Kaku Gothic ProN"

GAMMAS = [0.9, 0.99, 1.0]
MAX_STEPS = 500  # CartPole-v1 の打ち切り（満点）
COLORS = {0.9: "#E8743B", 0.99: "#098FD3", 1.0: "#5B5B5B"}

lengths = np.array(json.load(open("day01/result.json"))["lengths"])


def discounted_return(length, gamma):
    """報酬が毎ステップ 1 のエピソードの収益。length はステップ数（配列でもよい）。"""
    length = np.asarray(length, dtype=float)
    if gamma == 1.0:
        return length
    return (1.0 - gamma ** length) / (1.0 - gamma)


result = {"episodes": int(len(lengths)), "mean_length": float(lengths.mean()), "by_gamma": {}}
for g in GAMMAS:
    G = discounted_return(lengths, g)
    g_max = float(discounted_return(MAX_STEPS, g))
    result["by_gamma"][str(g)] = {
        "mean": float(G.mean()),
        "median": float(np.median(G)),
        "std": float(G.std()),
        "min": float(G.min()),
        "max": float(G.max()),
        "max_possible_500steps": g_max,
        "mean_over_max_possible": float(G.mean() / g_max),
        "horizon_1_over_1_minus_gamma": None if g == 1.0 else float(1.0 / (1.0 - g)),
        "return_at_30_steps": float(discounted_return(30, g)),
        "return_at_76_steps": float(discounted_return(76, g)),
    }

m09 = result["by_gamma"]["0.9"]["mean"]
m099 = result["by_gamma"]["0.99"]["mean"]
m10 = result["by_gamma"]["1.0"]["mean"]
result["ratio_mean_099_over_09"] = m099 / m09
result["ratio_mean_10_over_099"] = m10 / m099
print(json.dumps(result, ensure_ascii=False, indent=2))
json.dump(result, open("day02/result.json", "w"), ensure_ascii=False, indent=2)

# 図1: γ ごとの収益の分布（同じ 1,000 エピソード）
fig, axes = plt.subplots(1, 3, figsize=(11, 3.6))
for ax, g in zip(axes, GAMMAS):
    G = discounted_return(lengths, g)
    ax.hist(G, bins=30, color=COLORS[g])
    ax.axvline(G.mean(), color="black", linestyle="--", linewidth=1)
    ax.set_title(f"γ = {g}（平均 {G.mean():.1f}）")
    ax.set_xlabel("収益 G")
axes[0].set_ylabel("エピソード数")
fig.suptitle("同じ 1,000 エピソードの収益を、割引率だけ変えて数え直す", y=1.02)
fig.tight_layout()
fig.savefig("day02/returns_hist.png", dpi=150, bbox_inches="tight")

# 図2: エピソードの長さと収益の関係（1〜100 ステップ）
L = np.arange(1, 101)
plt.figure(figsize=(7, 4))
for g in GAMMAS:
    plt.plot(L, discounted_return(L, g), color=COLORS[g], label=f"γ = {g}")
plt.axvspan(lengths.min(), lengths.max(), color="#cccccc", alpha=0.4, label="今日のエピソードの範囲（8〜76）")
plt.axvline(lengths.mean(), color="black", linestyle="--", linewidth=1, label=f"平均 {lengths.mean():.1f} ステップ")
plt.xlabel("倒れるまでのステップ数 L")
plt.ylabel("収益 G")
plt.title("γ = 0.9 では 10 を超えられない。30 ステップも 76 ステップもほぼ同じ価値になる")
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig("day02/return_vs_length.png", dpi=150)
