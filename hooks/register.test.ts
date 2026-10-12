import { expect, test } from 'claude-code/testing'

import { MIN_TURN_MS } from './register'

const turn = (over: Record<string, unknown> = {}) => ({
  answer: 'done',
  durationMs: MIN_TURN_MS + 1,
  isAborted: false,
  turnId: 't1',
  reason: 'answer',
  ...over,
})

// Stand in for the engine beneath the plugin: record what it asked to play.
const played = async ($: any, on: any, e: any) => {
  const assets: string[] = []
  on('audio.play', (_: unknown, e: { clip: { asset: string } }) => {
    assets.push(e.clip.asset)
    return undefined
  })
  on('turn.complete', () => ({ text: e.answer }))
  await $.turn.complete(e)
  return assets
}

test('chimes after a long answered turn', async ($, on) => {
  expect(await played($, on, turn())).toEqual(['sounds/done.aiff'])
})

test('low tone when the turn errored', async ($, on) => {
  expect(await played($, on, turn({ reason: 'error' }))).toEqual(['sounds/error.aiff'])
})

test('silent for short turns', async ($, on) => {
  expect(await played($, on, turn({ durationMs: 500 }))).toEqual([])
})

test('silent when interrupted', async ($, on) => {
  expect(await played($, on, turn({ isAborted: true, reason: 'aborted' }))).toEqual([])
})

test('silent for subagent turns', async ($, on) => {
  expect(await played($, on, turn({ agentId: 'a1' }))).toEqual([])
})
