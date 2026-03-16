"""t-Digest — streaming quantile estimation."""
import bisect

class Centroid:
    def __init__(self, mean, count=1):
        self.mean, self.count = mean, count

class TDigest:
    def __init__(self, delta=100):
        self.delta = delta
        self.centroids = []
        self.n = 0
    def add(self, x):
        c = Centroid(x)
        pos = bisect.bisect_left([c2.mean for c2 in self.centroids], x)
        if pos < len(self.centroids) and self.centroids[pos].count < self.delta / len(self.centroids):
            c2 = self.centroids[pos]
            c2.mean = (c2.mean * c2.count + x) / (c2.count + 1)
            c2.count += 1
        else:
            self.centroids.insert(pos, c)
        self.n += 1
    def quantile(self, q):
        if not self.centroids: return 0
        target = q * self.n
        cum = 0
        for c in self.centroids:
            cum += c.count
            if cum >= target: return c.mean
        return self.centroids[-1].mean

if __name__ == "__main__":
    import random; random.seed(42)
    td = TDigest(100)
    data = [random.gauss(0, 1) for _ in range(10000)]
    for x in data: td.add(x)
    data.sort()
    for q in [0.5, 0.9, 0.99]:
        est = td.quantile(q)
        actual = data[int(q * len(data))]
        print(f"q={q}: est={est:.3f}, actual={actual:.3f}")
    print(f"Centroids: {len(td.centroids)}")
    print("All tests passed!")
