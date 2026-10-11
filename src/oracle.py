"""Exact rational oracle for a restricted numeric JSON Schema projection."""
import json
from fractions import Fraction
from jsonschema import Draft202012Validator, validators, ValidationError

def unique(pairs):
    d = {}
    for k,v in pairs:
        if k in d: raise ValueError("duplicate key: " + k)
        d[k] = v
    return d

def loads(s):
    return json.loads(s, parse_float=Fraction, parse_int=int, object_pairs_hook=unique,
                      parse_constant=lambda s: (_ for _ in ()).throw(ValueError(s)))

def num(x):
    return isinstance(x, (int, Fraction)) and not isinstance(x, bool)

def multiple(validator, divisor, instance, schema):
    if num(instance) and (Fraction(instance) / divisor).denominator != 1:
        yield ValidationError('not an exact multiple')

checker = Draft202012Validator.TYPE_CHECKER.redefine('number', lambda _, x: num(x))
checker = checker.redefine('integer', lambda _, x: num(x) and Fraction(x).denominator == 1)
ExactValidator = validators.extend(Draft202012Validator, {'multipleOf': multiple}, type_checker=checker)

def valid(schema, value):
    return ExactValidator(schema).is_valid(value)

def decimal(x):
    """Finite base-10 representation, without Decimal's context rounding."""
    x = Fraction(x); n, d = x.numerator, x.denominator
    a = b = 0
    while d % 2 == 0: d //= 2; a += 1
    while d % 5 == 0: d //= 5; b += 1
    if d != 1: raise ValueError('not a finite decimal')
    k = max(a, b); n *= 2**(k-a) * 5**(k-b)
    if k == 0: return str(n)
    return str(n) + 'e-' + str(k)

def dumps(x):
    if isinstance(x, Fraction): return decimal(x)
    if isinstance(x, dict): return '{' + ','.join(json.dumps(k)+':'+dumps(v) for k,v in x.items()) + '}'
    if isinstance(x, list): return '[' + ','.join(dumps(v) for v in x) + ']'
    return json.dumps(x, ensure_ascii=True, allow_nan=False, separators=(',', ':'))
