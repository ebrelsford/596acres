from fractions import Fraction

from sizecompare.models import SizeComparable

SQFT_PER_ACRE = 43560.0

def get_factor(comparable=None, compare_sqft=None):
    try:
        return compare_sqft / comparable.sqft
    except Exception:
        return None

def get_rounded_factor(factor, digits=1):
    rounded = round(factor, digits)
    if rounded: return str(rounded)

    # keep trying until we get a number
    return get_rounded_factor(factor, digits + 1)

def get_fraction(factor, denominator=10):
    fraction = Fraction(str(factor))
    display_fraction = fraction.limit_denominator(denominator)
    if display_fraction.numerator: return str(display_fraction)
    return get_fraction(factor, denominator=denominator * 10)

def find_comparable(sqft=None, acres=None):
    if not (sqft or acres):
        return None

    sqft = sqft
    if sqft is None:
        sqft = float(acres) * SQFT_PER_ACRE
    if acres is None or acres == '0':
        return dict(success=False)

    try:
        smaller = SizeComparable.objects.filter(sqft__lte=sqft).order_by('-sqft')[0]
        smaller_factor = get_factor(comparable=smaller, compare_sqft=sqft)

        smaller_dict = {
            'comparable_is': 'smaller',
            'factor': get_rounded_factor(smaller_factor),
            'name': smaller.name,
            'sqft': smaller.sqft,
        }
    except Exception:
        smaller = None

    try:
        bigger = SizeComparable.objects.filter(sqft__gte=sqft).order_by('sqft')[0]
        bigger_factor = get_factor(comparable=bigger, compare_sqft=sqft)

        bigger_dict = {
            'comparable_is': 'bigger',
            'factor': get_rounded_factor(bigger_factor),
            'fraction': get_fraction(bigger_factor),
            'name': bigger.name,
            'sqft': bigger.sqft,
        }
    except Exception:
        bigger = None

    return_dict = {}
    if smaller and bigger:
        # get the one with closest to same size
        if abs(bigger.sqft - sqft) < abs(smaller.sqft - sqft):
            return_dict = bigger_dict
        else:
            return_dict = smaller_dict
    elif smaller:
        return_dict = smaller_dict
    elif bigger:
        return_dict = bigger_dict
    else:
        return dict(success=False)

    return_dict.update({
        'success': True,
    })
    return return_dict
