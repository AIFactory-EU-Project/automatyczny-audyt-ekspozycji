import lmdb


def _get_size(db):
    with db.begin(write=False) as txn:
        with txn.cursor() as cursor:
            i = 0
            for _ in cursor:
                i += 1
            return i


def get_size(lmdb_or_path):
    if isinstance(lmdb_or_path, lmdb.Environment):
        return _get_size(lmdb_or_path)
    else:
        with lmdb.open(lmdb_or_path) as db:
            return _get_size(db)
