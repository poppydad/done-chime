import type { Register } from 'claude-code'

// Quick answers don't need a chime — only turns long enough that you
// probably looked away.
export const MIN_TURN_MS = 20_000

export const register: Register = (on) => {
  on('turn.complete', async ($, e, next) => {
    const result = await next(e)
    // Main loop only (subagent turns carry agentId), and never when you
    // interrupted it yourself — you're already looking.
    if (e.agentId || e.isAborted || e.durationMs < MIN_TURN_MS) return result
    const asset = e.reason === 'answer' ? 'sounds/done.aiff' : 'sounds/error.aiff'
    // Fire and forget: the turn shouldn't wait on playback, and a missing
    // player (non-macOS) shouldn't surface as a failed hook.
    $.audio.play({ asset }).catch(() => {})
    return result
  })
}
