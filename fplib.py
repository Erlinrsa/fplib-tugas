"""fplib.py - Library fungsi umum bergaya fungsional.

Prinsip: pure function (output hanya bergantung pada input), tanpa efek
samping, dan tanpa memutasi data masukan. Setiap fungsi mengembalikan
struktur data baru.
"""
from functools import reduce


# ---------- Komposisi fungsi ----------
def compose(*fns):
    """compose(f, g, h)(x) == f(g(h(x))) -- dieksekusi dari kanan ke kiri."""
    return lambda x: reduce(lambda acc, f: f(acc), reversed(fns), x)


def pipe(value, *fns):
    """pipe(x, f, g, h) == h(g(f(x))) -- dieksekusi dari kiri ke kanan."""
    return reduce(lambda acc, f: f(acc), fns, value)


# ---------- Transformasi koleksi ----------
def map_list(f, xs):
    """Terapkan f ke setiap elemen, kembalikan list baru."""
    return [f(x) for x in xs]


def filter_list(pred, xs):
    """Ambil elemen yang memenuhi pred."""
    return [x for x in xs if pred(x)]


def reduce_list(f, xs, init):
    """Lipat koleksi menjadi satu nilai dengan f(acc, x), mulai dari init."""
    return reduce(f, xs, init)


def flatten(xss):
    """Ratakan list of list menjadi satu list."""
    return [x for xs in xss for x in xs]


def partition(pred, xs):
    """Pisahkan xs menjadi (yang memenuhi pred, yang tidak)."""
    return (filter_list(pred, xs), filter_list(lambda x: not pred(x), xs))


def pluck(key, xs):
    """Ambil nilai dict[key] dari setiap elemen."""
    return [x[key] for x in xs]


def take(n, xs):
    """Ambil n elemen pertama."""
    return list(xs)[:n]


# ---------- Pencarian & pembaruan immutable ----------
def find_first(pred, xs, default=None):
    """Elemen pertama yang memenuhi pred, atau default."""
    return next((x for x in xs if pred(x)), default)


def add_item(xs, item):
    """Tambah item di akhir tanpa mengubah xs asli."""
    return [*xs, item]


def update_where(pred, f, xs):
    """Ganti elemen yang memenuhi pred dengan f(elemen); lainnya tetap."""
    return [f(x) if pred(x) else x for x in xs]


def remove_where(pred, xs):
    """Buang elemen yang memenuhi pred."""
    return [x for x in xs if not pred(x)]


# ---------- Agregasi ----------
def sum_by(key, xs):
    """Jumlahkan key(x) untuk semua x."""
    return reduce(lambda acc, x: acc + key(x), xs, 0)


def avg(xs):
    """Rata-rata; 0 jika kosong."""
    xs = list(xs)
    return sum(xs) / len(xs) if xs else 0


def percent(part, whole):
    """Persentase part terhadap whole (1 desimal); 0.0 jika whole = 0."""
    return round(part * 100 / whole, 1) if whole else 0.0


def group_by(key, xs):
    """Kelompokkan xs menjadi dict {key(x): [x, ...]}."""
    def step(acc, x):
        k = key(x)
        return {**acc, k: [*acc.get(k, []), x]}
    return reduce(step, xs, {})


def count_by(key, xs):
    """Hitung jumlah elemen per key(x)."""
    return {k: len(v) for k, v in group_by(key, xs).items()}


def max_by(key, xs, default=None):
    """Elemen dengan key(x) terbesar."""
    return max(xs, key=key, default=default)


# ---------- Pengurutan & peringkat ----------
def sort_by(key, xs, reverse=False):
    """Urutkan tanpa mengubah xs asli."""
    return sorted(xs, key=key, reverse=reverse)


def rank_by(key, xs):
    """Urutkan menurun menurut key dan tambahkan field 'peringkat'.

    Nilai sama mendapat peringkat sama (competition ranking: 1,2,2,4).
    """
    ordered = sort_by(key, xs, reverse=True)
    return [
        {**x, "peringkat": 1 + len(filter_list(lambda y: key(y) > key(x), ordered))}
        for x in ordered
    ]


# ---------- Format tampilan ----------
def format_rupiah(n):
    """12500 -> 'Rp 12.500'."""
    return "Rp " + f"{n:,.0f}".replace(",", ".")


def format_table(headers, rows):
    """Tabel teks sederhana dari headers dan rows (list of list)."""
    rows = [[str(c) for c in r] for r in rows]
    widths = [
        max([len(str(h))] + [len(r[i]) for r in rows])
        for i, h in enumerate(headers)
    ]
    line = lambda cells: " | ".join(str(c).ljust(w) for c, w in zip(cells, widths))
    sep = "-+-".join("-" * w for w in widths)
    return "\n".join([line(headers), sep, *map(line, rows)])
