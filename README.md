# done-chime

A Claude Code mod that plays a chime when a long turn finishes, so you can look
away while Claude works. If the turn ended in an error, it plays a low tone
instead.

- Only turns longer than **20 seconds** chime. Quick answers stay quiet.
- No sound when you interrupted the turn yourself (you're already looking).
- No sound for subagent turns, only the main conversation.

## Install

In a Claude Code terminal session:

```
/plugin install done-chime --marketplace poppydad/done-chime
```

Answer `y` to add the marketplace and pick the **user** scope so it loads in
every repo.

## The sounds

`sounds/done.aiff` (two rising bell notes) and `sounds/error.aiff` (two falling
low tones) are generated from scratch by `tools/make_sounds.py`, which uses only
the Python standard library. Change the notes there and rerun it to make your
own:

```bash
python3 tools/make_sounds.py
```

## Layout

```
hooks/register.ts        turn.complete hook: when to chime, which sound
hooks/register.test.ts   tests
sounds/                  done.aiff, error.aiff
tools/make_sounds.py     generates the sounds
```
