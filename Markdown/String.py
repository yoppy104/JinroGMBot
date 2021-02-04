
def Symbolic(symbol, text):
    return "{}{}{}".format(symbol, text, symbol)

def Italic(text):
    return Symbolic("*", text)

def Bold(text):
    return Symbolic("**", text)

def UnderLine(text):
    return Symbolic("__", text)

def DelLine(text):
    return Symbolic("~~", text)

def Hide(text):
    return Symbolic("||", text)

def Background(text):
    return Symbolic("'", text)

def Quote(text):
    return "> {}".format(text)
