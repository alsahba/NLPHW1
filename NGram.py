import bisect


class NGram():

    def boundaries(self, num, breakpoints, result):
        i = bisect.bisect(breakpoints, num)
        if i > len(result):
            return '</s>'
        return result[i]

    def totalCountCalculator(self, mapping):
        sum = 0

        for values in mapping.items():
            sum += values[1]
        return sum

    def counter(self, separated_line):
        pass

