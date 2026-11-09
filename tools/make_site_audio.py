"""Encode web previews (MP3) for the site from the rendered Combo Ladder files."""
import os, subprocess, numpy as np, soundfile as sf
SRC = "/workspace/unity-asset-store/combo-ladder/build/Assets/ComboLadder/Audio/"
PRE = "/workspace/unity-asset-store/combo-ladder/preview/"
OUT = "/workspace/unity-asset-store/site/assets/audio/"
os.makedirs(OUT, exist_ok=True)


def enc(wav, mp3, br="160k"):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav, "-codec:a", "libmp3lame", "-b:a", br, mp3], check=True)


def ladder(folder, name, gap):
    xs = []
    for k in range(1, 9):
        x, sr = sf.read(f"{SRC}ComboLadder/{folder}/CL_Combo_{folder}_Step{k:02d}.wav", always_2d=True)
        xs.append(x)
    n = int((7 * gap) * 48000) + max(len(x) for x in xs)
    mix = np.zeros((n, 1))
    for k, x in enumerate(xs):
        i = int(k * gap * 48000); mix[i:i + len(x)] += x[:, :1]
    mix *= 10 ** (-1.5 / 20) / max(1e-9, np.max(np.abs(mix))) if np.max(np.abs(mix)) > 10 ** (-1.5 / 20) else 1
    tmp = f"/tmp/{name}.wav"; sf.write(tmp, mix, 48000, subtype="PCM_24"); enc(tmp, OUT + name + ".mp3")


enc(PRE + "ComboLadder_Preview.wav", OUT + "ComboLadder_Preview.mp3", "192k")
ladder("Glass", "CL_Combo_Glass_Ladder_Steps01-08", 0.16)
ladder("Pluck", "CL_Combo_Pluck_Ladder_Steps01-08", 0.14)
for rel in ["Coins/CL_Coin_Pickup_01", "Coins/CL_Gem_Pickup_02", "Pops/CL_Bubble_Burst_01", "UI/CL_UI_Button_Confirm_01",
            "Stars/CL_Star_Rating_03", "Chimes/CL_Chime_LevelUp_01", "Stingers/CL_Stinger_Success_01",
            "Stingers/CL_Stinger_Fail_01", "Boosters/CL_Booster_Charge_01"]:
    enc(SRC + rel + ".wav", OUT + os.path.basename(rel) + ".mp3")
print(sorted(os.listdir(OUT)))
