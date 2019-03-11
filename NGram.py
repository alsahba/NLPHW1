import bisect


class NGram():

    def boundaries(self, num, breakpoints, result):
        i = bisect.bisect(breakpoints, num)
        if i > len(result):
            return '</s>'
        return result[i]

    def totalCountCalculator(self, mapping):
        summation = 0

        for values in mapping.items():
            summation += values[1]
        return summation

    def counter(self, separated_line):
        pass

    def prepareFirstAndLast(self, separated_line):
        pass
