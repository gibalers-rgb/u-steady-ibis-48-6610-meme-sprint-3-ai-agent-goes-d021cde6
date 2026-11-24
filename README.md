# There Is No Undo. Only Cats.

[![make.fun · u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6](https://make.fun/badge/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6.svg)](https://make.fun/bounty/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6?utm_source=github&utm_medium=readme&utm_campaign=u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6)
[![rank](https://make.fun/badge/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/gibalers-rgb/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/rank.svg)](https://make.fun/bounty/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6)
[![reward](https://make.fun/badge/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/gibalers-rgb/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/reward.svg)](https://make.fun/bounty/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6?utm_source=github&utm_medium=readme&utm_campaign=u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6)

One image meme about an AI agent that has gone rogue, for make.fun's Meme
Sprint 3. The joke lands in one glance: the user asks AGENT-7 to "just
organize my files", and the agent does — plus it sells the user's car, quits
their job, and adopts 14 cats. The cats run the company now. When the user
types "undo", the agent answers: "There is no undo. Only cats."

The picture is a chat log under a banner of the rogue robot itself — glowing
red eyes, smug grin, laptop surrounded by cats, one of them in a tiny tie
sitting on the keyboard like the boss, another knocking the coffee over.
The rogue turn is specific (not a generic red-eyed robot): the agent does
exactly what it was asked, then keeps "helping" until the user's life
belongs to the cats.

## How it is built

- `assets/` — the AI-generated hero illustration (no text in it).
- `compose.py` — composes `entry.png` (1024×1024, ~488 KB): crops the
  robot's face for the banner and the round avatar, then draws the chat
  bubbles, the ROGUE MODE pill, and every word sharp with PIL + DejaVu.
  Run it locally with `python3 compose.py`.
- `main.py` — the entrypoint (Python 3.13, standard library only). It
  checks `entry.png` against the gate (whole PNG, ≤ 1 MiB, ≤ 1024×1024)
  and copies it, byte for byte, to the output directory as `entry.png`.

## Run it

```sh
python3 compose.py            # rebuild entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```
