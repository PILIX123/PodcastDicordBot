class Converters():
    def hourStrToMs(hrStr: str) -> int:
        h, m, s = hrStr.split(":")
        return (int(h) * 3600 + int(m) * 60 + int(s))*1000
