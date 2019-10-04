import xxhash
import numpy as np


class HashingArray(np.ndarray):
    def __new__(cls, array, filename=None, dtype=None, order=None):
        obj = np.asarray(array, dtype=dtype, order=order).view(cls)
        obj.filename = filename
        return obj

    def __hash__(self):
        h = xxhash.xxh64()
        h.update(self)
        if self.filename:
            h.update(self.filename)
        return h.intdigest()

    def __eq__(self, other):
        if hasattr(other, "filename") and self.filename != other.filename:
            return False
        return super().__eq__(other)

    def __repr__(self):  # Just makes it look nicer in dicts
        if self.filename:
            return f"HashingArray({self.filename})"
        return f"HashingArray({hash(self)})"
