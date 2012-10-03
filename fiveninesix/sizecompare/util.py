from sizecompare.models import SizeComparable

SQFT_PER_ACRE = 43560.0

def get_factor(comparable=None, compare_sqft=None):
    try:
        if comparable.sqft > compare_sqft:
            return comparable.sqft / compare_sqft
        else:
            return compare_sqft / comparable.sqft
    except Exception:
        return None

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
            #TODO find '.', keep one digit
            'factor': str(round(smaller_factor, 1)),
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
            #TODO find '.', keep one digit
            'factor': str(round(bigger_factor, 1)),
            'name': bigger.name,
            'sqft': bigger.sqft,
        }
    except Exception:
        bigger = None

    return_dict = {}
    if smaller and bigger:
        if bigger_factor < smaller_factor:
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
