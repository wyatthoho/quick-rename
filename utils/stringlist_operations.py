from math import floor, log10

type Names = list[str]
type Indices = list[int]


def replace_names(names: Names, find_str: str, replace_str: str) -> Names:
    return [name.replace(find_str, replace_str) for name in names]


def add_suffix(names: Names, suffix: str) -> Names:
    def add_to_base(name: str) -> str:
        base, sep, ext = name.rpartition('.')
        return f'{base}{suffix}.{ext}' if sep else f'{name}{suffix}'
    return [add_to_base(name) for name in names]


def clean_prefix(names: Names) -> Names:
    def remove_prefix(name: str) -> str:
        for sep in ['_', '-', ' ']:
            prefix, sep_found, remainder = name.partition(sep)
            if prefix.isdigit():
                return remainder
        return name
    return [remove_prefix(name) for name in names]


def reorder_names(names: Names, separator: str) -> Names:
    names = clean_prefix(names)
    num_name = len(names)
    decimal = floor(log10(num_name)) + 1
    return [
        f'{idx:0{decimal}d}{separator}{name}'
        for idx, name in enumerate(names)
    ]


def get_duplicate_indices(names: Names) -> Indices:
    for idx1, name1 in enumerate(names):
        for idx2, name2 in enumerate(names[idx1+1:]):
            if name2 == name1:
                return [idx1, idx1 + idx2 + 1]
    return []
