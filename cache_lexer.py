import ply.lex as lex

tokens = (
    'CLFLUSH', 'CLFLUSHOPT', 'CLWB',
    'PREFETCHT0', 'PREFETCHT1', 'PREFETCHT2', 'PREFETCHNTA',
    'WBINVD', 'INVD',
    'REGISTER', 'NUMBER', 'IDENTIFIER',
    'LBRACKET', 'RBRACKET', 'PLUS', 'MINUS', 'COMMA',
)

t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_PLUS = r'\+'
t_MINUS = r'-'
t_COMMA = r','

def t_CLFLUSHOPT(t):
    r'CLFLUSHOPT'
    return t

def t_CLFLUSH(t):
    r'CLFLUSH'
    return t

def t_CLWB(t):
    r'CLWB'
    return t

def t_PREFETCHT0(t):
    r'PREFETCHT0'
    return t

def t_PREFETCHT1(t):
    r'PREFETCHT1'
    return t

def t_PREFETCHT2(t):
    r'PREFETCHT2'
    return t

def t_PREFETCHNTA(t):
    r'PREFETCHNTA'
    return t

def t_WBINVD(t):
    r'WBINVD'
    return t

def t_INVD(t):
    r'INVD'
    return t

def t_REGISTER(t):
    r'[ER](AX|BX|CX|DX|SI|DI|BP|SP)'
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_COMMENT(t):
    r';.*'
    pass

def t_error(t):
    print(f"کاراکتر غیرمجاز \'{t.value[0]}\' در خط {t.lineno}")
    t.lexer.skip(1)

def build_lexer():
    return lex.lex()

if __name__ == "__main__":
    lexer = build_lexer()

    # تست
    test_code = """
    CLFLUSH [EAX]
    CLFLUSHOPT [EBX+16]
    PREFETCHT0 [ECX-8]
    WBINVD
    CLWB [cache_line]
    """

    lexer.input(test_code)
    print("نتیجه تحلیل واژگانی:")
    print("-" * 50)
    for tok in lexer:
        print(f"Token: {tok.type:15s} | Value: {tok.value}")
