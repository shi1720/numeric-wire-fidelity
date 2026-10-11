/** Numeric wire fidelity. Equality is mathematical decimal equality, not bit equality. */
export function decimalKey(s) {
  const m = /^(-?)(\d+)(?:\.(\d+))?(?:[eE]([+-]?\d+))?$/.exec(s);
  if (!m) throw new SyntaxError('Not a JSON number');
  let c = BigInt(m[1] + m[2] + (m[3] || ''));
  let e = BigInt(m[4] || '0') - BigInt((m[3] || '').length);
  if (c === 0n) return '0';
  while (c % 10n === 0n) { c /= 10n; e++; }
  return c.toString() + 'e' + e.toString();
}
export function parseGuarded(text) {
  // Must receive original bytes before any ordinary JSON.parse call.
  return JSON.parse(text, (_k, v, context) => {
    if (typeof v === 'number' && (!Number.isFinite(v) ||
        decimalKey(context.source) !== decimalKey(JSON.stringify(v)))) {
      throw new RangeError('Numeric value changes during native JSON transport');
    }
    return v;
  });
}
export function parseSafeIntegers(text) {
  const x = JSON.parse(text);
  const visit = v => {
    if (typeof v === 'number' && (!Number.isFinite(v) ||
        (Number.isInteger(v) && !Number.isSafeInteger(v)))) throw new RangeError('Unsafe integer');
    if (v && typeof v === 'object') for (const z of Object.values(v)) visit(z);
  };
  visit(x); return x;
}
