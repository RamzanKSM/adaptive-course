/**
 * Sounds of «Жребий», synthesized with the Web Audio API (no files): a ratchet click when a segment passes the arrow,
 * a dull pop when a name drops out, a short fanfare for a winner and a sparkle when the prize is revealed.
 * The audio context is created on the first click (browsers allow sound only after a gesture).
 */
export class DrawSound {
  private ctx: AudioContext | null = null
  private lastTick = 0
  constructor(public enabled: boolean, public volume: number) {}

  /** Call from a click handler before the first sound. */
  unlock() {
    if (!this.enabled) return
    try {
      this.ctx ??= new AudioContext()
      if (this.ctx.state === 'suspended') this.ctx.resume().catch(() => undefined)
    } catch { this.ctx = null }
  }

  private tone(freq: number, start: number, length: number, type: OscillatorType, gain: number, endFreq?: number) {
    const ctx = this.ctx
    if (!ctx || !this.enabled || this.volume <= 0) return
    const t = ctx.currentTime + start, osc = ctx.createOscillator(), amp = ctx.createGain()
    osc.type = type; osc.frequency.setValueAtTime(freq, t)
    if (endFreq) osc.frequency.exponentialRampToValueAtTime(endFreq, t + length)
    const peak = gain * this.volume / 100
    amp.gain.setValueAtTime(0.0001, t); amp.gain.exponentialRampToValueAtTime(peak, t + 0.008); amp.gain.exponentialRampToValueAtTime(0.0001, t + length)
    osc.connect(amp).connect(ctx.destination); osc.start(t); osc.stop(t + length + 0.02)
  }

  /** The ratchet: at most one click every 35 ms, so a fast wheel does not buzz. */
  tick() {
    const now = performance.now()
    if (now - this.lastTick < 35) return
    this.lastTick = now
    this.tone(1900, 0, 0.03, 'square', 0.08)
  }
  pop() { this.tone(420, 0, 0.18, 'sine', 0.5, 110); this.tone(160, 0.02, 0.12, 'triangle', 0.25) }
  win() { [523.25, 659.25, 783.99].forEach((f, i) => this.tone(f, i * 0.12, 0.16, 'triangle', 0.35)); this.tone(1046.5, 0.36, 0.6, 'triangle', 0.4); this.tone(523.25, 0.36, 0.6, 'sine', 0.2) }
  reveal() { [1318.5, 1568, 2093, 2637].forEach((f, i) => this.tone(f, i * 0.07, 0.25, 'sine', 0.22)) }
}
