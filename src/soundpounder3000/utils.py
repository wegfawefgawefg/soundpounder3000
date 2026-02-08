def parse_num_or_frac(num_or_frac):
    if '/' in num_or_frac:  #   its a frac
        numerator, denom = num_or_frac.split('/')
        return float(numerator) / float(denom)
    else:   #   its a num
        return float(num_or_frac)