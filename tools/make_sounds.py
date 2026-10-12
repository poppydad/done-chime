"""Generate sounds/done.aiff and sounds/error.aiff from scratch.

Standard library only, so the sounds are reproducible and original:
    python3 tools/make_sounds.py
"""

import math
import struct
from pathlib import Path

RATE = 44100
# 44100 as an 80-bit IEEE extended float, which AIFF's COMM chunk requires.
RATE_EXTENDED = b"\x40\x0e\xac\x44\x00\x00\x00\x00\x00\x00"
SOUNDS = Path(__file__).resolve().parent.parent / "sounds"


def bell(freq: float, secs: float, start: float, total: float) -> list[float]:
    """A struck-bell tone: a few inharmonic partials, each decaying on its own."""
    partials = [(1.0, 1.0, 3.0), (2.76, 0.35, 5.0), (5.40, 0.15, 8.0)]
    out = [0.0] * int(total * RATE)
    begin = int(start * RATE)
    for i in range(int(secs * RATE)):
        if begin + i >= len(out):
            break
        t = i / RATE
        attack = min(1.0, t / 0.004)
        out[begin + i] += attack * sum(
            amp * math.exp(-decay * t) * math.sin(2 * math.pi * freq * ratio * t)
            for ratio, amp, decay in partials
        )
    return out


def thud(freq: float, secs: float, start: float, total: float) -> list[float]:
    """A soft low tone: fundamental plus a little odd harmonic, quick fade."""
    out = [0.0] * int(total * RATE)
    begin = int(start * RATE)
    n = int(secs * RATE)
    for i in range(n):
        if begin + i >= len(out):
            break
        t = i / RATE
        env = min(1.0, t / 0.01) * min(1.0, (n - i) / (0.06 * RATE)) * math.exp(-2.5 * t)
        out[begin + i] += env * (
            math.sin(2 * math.pi * freq * t) + 0.25 * math.sin(2 * math.pi * freq * 3 * t)
        )
    return out


def mix(*tracks: list[float]) -> list[float]:
    return [sum(s) for s in zip(*tracks)]


def write_aiff(path: Path, samples: list[float], peak: float = 0.7) -> None:
    top = max(abs(s) for s in samples) or 1.0
    pcm = b"".join(struct.pack(">h", round(s / top * peak * 32767)) for s in samples)
    comm = struct.pack(">hIh", 1, len(samples), 16) + RATE_EXTENDED
    ssnd = struct.pack(">II", 0, 0) + pcm
    body = b"AIFF"
    body += b"COMM" + struct.pack(">I", len(comm)) + comm
    body += b"SSND" + struct.pack(">I", len(ssnd)) + ssnd
    path.write_bytes(b"FORM" + struct.pack(">I", len(body)) + body)


def main() -> None:
    SOUNDS.mkdir(exist_ok=True)
    # Done: two rising bell notes, E6 then B6.
    total = 1.4
    write_aiff(SOUNDS / "done.aiff", mix(bell(1318.5, 1.3, 0.0, total), bell(1975.5, 1.2, 0.12, total)))
    # Error: two falling low tones, A3 then E3.
    total = 0.6
    write_aiff(SOUNDS / "error.aiff", mix(thud(220.0, 0.22, 0.0, total), thud(164.8, 0.4, 0.2, total)))


if __name__ == "__main__":
    main()
