import bitmath


def normalize_bytes(n):
    if "K" in n:
        return float(n.replace('K', '')), 'K'
    elif "M" in n:
        return float(n.replace('M', '')), 'M'
    elif "G" in n:
        return float(n.replace('G', '')), 'G'
    elif "T" in n:
        return float(n.replace('T', '')), 'T'
    else:
        return 0, 'E'


def normalize_number(n):
    if "K" in n:
        return float(n.replace('K', '')), 'K'
    elif "M" in n:
        return float(n.replace('M', '')), 'M'
    elif "G" in n:
        return float(n.replace('G', '')), 'G'
    elif "T" in n:
        return float(n.replace('T', '')), 'T'
    else:
        return n, 'N'


def to_base_10(n):
    if "K" in n[1]:
        return int(round(bitmath.kB(n[0]).to_Byte()))
    elif "M" in n[1]:
        return int(round(bitmath.MB(n[0]).to_Byte()))
    elif "G" in n[1]:
        return int(round(bitmath.GB(n[0]).to_Byte()))
    elif "T" in n[1]:
        return int(round(bitmath.TB(n[0]).to_Byte()))
    else:
        return n[0]


def to_MiB(n):
    if "K" in n[1]:
        return int(round(bitmath.KiB(n[0]).to_MiB()))
    elif "M" in n[1]:
        return int(round(bitmath.MiB(n[0]).to_MiB()))
    elif "G" in n[1]:
        return int(round(bitmath.GiB(n[0]).to_MiB()))
    elif "T" in n[1]:
        return int(round(bitmath.TiB(n[0]).to_MiB()))
    else:
        return 0


def to_KiB(n):
    if "B" in n[1]:
        return int(round(bitmath.Byte(n[0]).to_KiB()))
    elif "K" in n[1]:
        return int(round(bitmath.KiB(n[0]).to_KiB()))
    elif "M" in n[1]:
        return int(round(bitmath.MiB(n[0]).to_KiB()))
    elif "G" in n[1]:
        return int(round(bitmath.GiB(n[0]).to_KiB()))
    elif "T" in n[1]:
        return int(round(bitmath.TiB(n[0]).to_KiB()))
    else:
        return 0
