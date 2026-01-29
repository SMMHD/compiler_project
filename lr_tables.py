#!/usr/bin/env python3
"""
جدول پارس کامل LR(0) برای دستورات کنترل کش
Complete LR(0) Parsing Table for Cache Control Instructions
پروژه کامپایلر - گروه 15
دانشگاه شهید باهنر کرمان
"""

# ═════════════════════════════════════════════════════════════════════
# قوانین گرامر (Grammar Rules)
# ═════════════════════════════════════════════════════════════════════

GRAMMAR_RULES = {
    0: "S' -> instruction",
    1: "instruction -> mnemonic operand",
    2: "instruction -> mnemonic",
    3: "mnemonic -> CLFLUSH",
    4: "mnemonic -> CLFLUSHOPT",
    5: "mnemonic -> CLWB",
    6: "mnemonic -> PREFETCHT0",
    7: "mnemonic -> PREFETCHT1",
    8: "mnemonic -> PREFETCHT2",
    9: "mnemonic -> PREFETCHNTA",
    10: "mnemonic -> WBINVD",
    11: "mnemonic -> INVD",
    12: "operand -> memory_address",
    13: "memory_address -> [ base_expr ]",
    14: "base_expr -> REGISTER offset",
    15: "base_expr -> REGISTER",
    16: "base_expr -> IDENTIFIER",
    17: "offset -> + NUMBER",
    18: "offset -> - NUMBER"
}

# ═════════════════════════════════════════════════════════════════════
# تعریف نمادها (Symbols)
# ═════════════════════════════════════════════════════════════════════

TERMINALS = [
    'CLFLUSH', 'CLFLUSHOPT', 'CLWB',
    'PREFETCHT0', 'PREFETCHT1', 'PREFETCHT2', 'PREFETCHNTA',
    'WBINVD', 'INVD',
    '[', ']', 'REGISTER', 'IDENTIFIER', '+', '-', 'NUMBER', '$'
]

NON_TERMINALS = ['instruction', 'mnemonic', 'operand', 'memory_address', 'base_expr', 'offset']

# گروه‌بندی دستورات
FLUSH_OPS = ['CLFLUSH', 'CLFLUSHOPT']
WRITEBACK_OPS = ['CLWB']
PREFETCH_OPS = ['PREFETCHT0', 'PREFETCHT1', 'PREFETCHT2', 'PREFETCHNTA']
INVALIDATE_OPS = ['WBINVD', 'INVD']

# ═════════════════════════════════════════════════════════════════════
# جدول پارس کامل LR(0)
# ═════════════════════════════════════════════════════════════════════
# فرمت: {state: {symbol: action}}
# action = 'sN' (shift to N), 'rN' (reduce by rule N), 'acc' (accept), 'N' (goto N)

LR_PARSING_TABLE = {
    # ───────────────────────────────────────────────────────────────
    # State 0: Initial state
    # Items: S' -> . instruction
    #        instruction -> . mnemonic operand
    #        instruction -> . mnemonic
    # ───────────────────────────────────────────────────────────────
    0: {
        'CLFLUSH': 's3',
        'CLFLUSHOPT': 's3',
        'CLWB': 's3',
        'PREFETCHT0': 's3',
        'PREFETCHT1': 's3',
        'PREFETCHT2': 's3',
        'PREFETCHNTA': 's3',
        'WBINVD': 's4',
        'INVD': 's4',
        'instruction': '1',  # goto
        'mnemonic': '2'  # goto
    },

    # ───────────────────────────────────────────────────────────────
    # State 1: Accept state
    # Items: S' -> instruction .
    # ───────────────────────────────────────────────────────────────
    1: {
        '$': 'acc'
    },

    # ───────────────────────────────────────────────────────────────
    # State 2: After mnemonic
    # Items: instruction -> mnemonic . operand
    #        instruction -> mnemonic .
    # ───────────────────────────────────────────────────────────────
    2: {
        '[': 's6',
        '$': 'r2',  # reduce: instruction -> mnemonic
        'operand': '5'  # goto
    },

    # ───────────────────────────────────────────────────────────────
    # State 3: After CLFLUSH/CLFLUSHOPT/CLWB/PREFETCH
    # Items: mnemonic -> CLFLUSH/CLFLUSHOPT/CLWB/PREFETCH* .
    # ⚠️ تغییر: این دستورات همیشه نیاز به operand دارند
    #    پس فقط [ را می‌پذیرند، نه $
    # ───────────────────────────────────────────────────────────────
    3: {
        '[': 'r3'  # reduce: mnemonic -> CLFLUSH/CLFLUSHOPT/etc
        # ✅ بدون '$': چون این دستورات بدون operand نامعتبرند
    },

    # ───────────────────────────────────────────────────────────────
    # State 4: After WBINVD/INVD
    # Items: mnemonic -> WBINVD/INVD .
    # ✅ این دستورات می‌توانند بدون operand باشند
    # ───────────────────────────────────────────────────────────────
    4: {
        # ⚠️ نکته: WBINVD و INVD نباید operand داشته باشند
        # پس فقط $ می‌پذیرند
        '$': 'r10'  # reduce: mnemonic -> WBINVD/INVD
        # ✅ بدون '[': چون این دستورات نمی‌توانند operand داشته باشند
    },

    # ───────────────────────────────────────────────────────────────
    # State 5: After operand
    # Items: instruction -> mnemonic operand .
    # ───────────────────────────────────────────────────────────────
    5: {
        '$': 'r1'  # reduce: instruction -> mnemonic operand
    },

    # ───────────────────────────────────────────────────────────────
    # State 6: After '['
    # Items: memory_address -> [ . base_expr ]
    # ───────────────────────────────────────────────────────────────
    6: {
        'REGISTER': 's8',
        'IDENTIFIER': 's9',
        'base_expr': '7'  # goto
    },

    # ───────────────────────────────────────────────────────────────
    # State 7: After base_expr
    # Items: memory_address -> [ base_expr . ]
    # ───────────────────────────────────────────────────────────────
    7: {
        ']': 's10'
    },

    # ───────────────────────────────────────────────────────────────
    # State 8: After REGISTER
    # Items: base_expr -> REGISTER . offset
    #        base_expr -> REGISTER .
    # ───────────────────────────────────────────────────────────────
    8: {
        '+': 's12',
        '-': 's12',
        ']': 'r15',  # reduce: base_expr -> REGISTER
        'offset': '11'  # goto
    },

    # ───────────────────────────────────────────────────────────────
    # State 9: After IDENTIFIER
    # Items: base_expr -> IDENTIFIER .
    # ───────────────────────────────────────────────────────────────
    9: {
        ']': 'r16'  # reduce: base_expr -> IDENTIFIER
    },

    # ───────────────────────────────────────────────────────────────
    # State 10: After ']'
    # Items: memory_address -> [ base_expr ] .
    #        operand -> memory_address .
    # ───────────────────────────────────────────────────────────────
    10: {
        '$': 'r13'  # reduce: memory_address -> [ base_expr ]
        # followed by r12: operand -> memory_address
    },

    # ───────────────────────────────────────────────────────────────
    # State 11: After offset
    # Items: base_expr -> REGISTER offset .
    # ───────────────────────────────────────────────────────────────
    11: {
        ']': 'r14'  # reduce: base_expr -> REGISTER offset
    },

    # ───────────────────────────────────────────────────────────────
    # State 12: After '+' or '-'
    # Items: offset -> + . NUMBER
    #        offset -> - . NUMBER
    # ───────────────────────────────────────────────────────────────
    12: {
        'NUMBER': 's13'
    },

    # ───────────────────────────────────────────────────────────────
    # State 13: After NUMBER
    # Items: offset -> + NUMBER .
    #        offset -> - NUMBER .
    # ───────────────────────────────────────────────────────────────
    13: {
        ']': 'r17'  # reduce by rules 17-18 depending on sign
    }
}


# ═════════════════════════════════════════════════════════════════════
# توابع کمکی (Helper Functions)
# ═════════════════════════════════════════════════════════════════════

def get_action(state, terminal):
    """
    دریافت action برای یک state و terminal
    Returns:
        str: action ('sN', 'rN', 'acc', or None for error)
    """
    if state in LR_PARSING_TABLE:
        return LR_PARSING_TABLE[state].get(terminal)
    return None


def get_goto(state, non_terminal):
    """
    دریافت goto برای یک state و non-terminal
    Returns:
        str: state number or None
    """
    if state in LR_PARSING_TABLE:
        return LR_PARSING_TABLE[state].get(non_terminal)
    return None


def print_grammar_rules():
    """چاپ قوانین گرامر"""
    print("\n" + "═" * 80)
    print(" " * 25 + "قوانین گرامر (Grammar Rules)")
    print("═" * 80 + "\n")

    for rule_num, rule in GRAMMAR_RULES.items():
        print(f"R{rule_num:2d}: {rule}")
    print()


def print_parsing_table():
    """چاپ جدول پارس به صورت خوانا"""
    print("\n" + "═" * 100)
    print(" " * 35 + "جدول پارس LR(0)")
    print("═" * 100 + "\n")

    # هدر جدول
    print(f"{'State':<7} │ {'ACTION':<65} │ {'GOTO':<22}")
    print("─" * 100)

    for state in sorted(LR_PARSING_TABLE.keys()):
        actions = []
        gotos = []

        for symbol, action in LR_PARSING_TABLE[state].items():
            if symbol in TERMINALS:
                actions.append(f"{symbol}:{action}")
            elif symbol in NON_TERMINALS:
                gotos.append(f"{symbol}:{action}")

        action_str = ", ".join(actions) if actions else "—"
        goto_str = ", ".join(gotos) if gotos else "—"

        # Truncate if too long
        if len(action_str) > 63:
            action_str = action_str[:60] + "..."
        if len(goto_str) > 20:
            goto_str = goto_str[:17] + "..."

        print(f"{state:<7} │ {action_str:<65} │ {goto_str:<22}")

    print("─" * 100)
    print("\n📝 راهنما:")
    print("  • sN  = Shift to state N")
    print("  • rN  = Reduce by rule N")
    print("  • acc = Accept")
    print("  • N   = Goto state N (for non-terminals)")
    print()


def print_matrix_table():
    """چاپ جدول به صورت ماتریسی کامل"""
    try:
        import pandas as pd

        print("\n" + "═" * 120)
        print(" " * 40 + "جدول پارس کامل (فرمت ماتریسی)")
        print("═" * 120 + "\n")

        # ساخت ماتریس
        action_terms = ['CLFLUSH', 'CLFLUSHOPT', 'CLWB', 'PREFETCH*',
                        'WBINVD', 'INVD', '[', ']', 'REG', 'ID', '+', '-', 'NUM', '$']
        goto_nonterms = ['inst', 'mnem', 'op', 'mem', 'base', 'off']

        data = []
        for state in range(14):
            row = {'State': state}

            # Simplified mapping
            state_data = LR_PARSING_TABLE.get(state, {})

            for term in action_terms:
                if term == 'PREFETCH*':
                    val = state_data.get('PREFETCHT0', '')
                elif term == 'REG':
                    val = state_data.get('REGISTER', '')
                elif term == 'ID':
                    val = state_data.get('IDENTIFIER', '')
                elif term == 'NUM':
                    val = state_data.get('NUMBER', '')
                else:
                    val = state_data.get(term, '')
                row[term] = val

            # Goto columns (simplified names)
            mapping = {
                'inst': 'instruction',
                'mnem': 'mnemonic',
                'op': 'operand',
                'mem': 'memory_address',
                'base': 'base_expr',
                'off': 'offset'
            }

            for short, full in mapping.items():
                row[short] = state_data.get(full, '')

            data.append(row)

        df = pd.DataFrame(data)

        print("بخش 1: ACTION (ترمینال‌ها)")
        print("─" * 100)
        action_cols = ['State'] + action_terms
        print(df[action_cols].to_string(index=False))

        print("\n\nبخش 2: GOTO (نان‌ترمینال‌ها)")
        print("─" * 60)
        goto_cols = ['State'] + goto_nonterms
        print(df[goto_cols].to_string(index=False))

        print("\n" + "─" * 100 + "\n")

    except ImportError:
        print("⚠️  برای نمایش ماتریسی، پکیج pandas نیاز است: pip install pandas")


# ═════════════════════════════════════════════════════════════════════
# تابع اصلی برای main.py - DISPLAY_LR_TABLES
# ═════════════════════════════════════════════════════════════════════

def display_lr_tables():
    """
    نمایش جداول LR(0) برای main.py
    این تابع توسط منوی اصلی فراخوانی می‌شود
    """

    print("\n" + "═" * 80)
    print("                        جداول LR(0) Parser")
    print("═" * 80)

    # آمار کلی
    print(f"\n📊 آمار:")
    print(f"  • تعداد States: {len(LR_PARSING_TABLE)}")
    print(f"  • تعداد قوانین گرامر: {len(GRAMMAR_RULES)}")
    print(f"  • تعداد ترمینال‌ها: {len(TERMINALS)}")
    print(f"  • تعداد نان‌ترمینال‌ها: {len(NON_TERMINALS)}")
    print(f"  • نوع Parser: LR(0) Bottom-Up")

    # نمایش States
    print("\n" + "─" * 80)
    print("📋 حالات Automata (LR(0) Items):")
    print("─" * 80)

    state_descriptions = {
        0: "State اولیه - شروع پارس",
        1: "Accept State - پذیرش ورودی",
        2: "بعد از Mnemonic - انتظار Operand یا پایان",
        3: "بعد از CLFLUSH/CLFLUSHOPT/CLWB/PREFETCH (نیاز به operand)",
        4: "بعد از WBINVD/INVD (بدون operand)",
        5: "بعد از Operand - آماده Reduce",
        6: "بعد از [ - انتظار Base Expression",
        7: "بعد از Base Expression - انتظار ]",
        8: "بعد از REGISTER - انتظار Offset یا ]",
        9: "بعد از IDENTIFIER - انتظار ]",
        10: "بعد از ] - کامل شدن Memory Address",
        11: "بعد از Offset - آماده Reduce",
        12: "بعد از +/- - انتظار NUMBER",
        13: "بعد از NUMBER - کامل شدن Offset"
    }

    for state_num in sorted(LR_PARSING_TABLE.keys()):
        desc = state_descriptions.get(state_num, "")
        print(f"\n🔹 State {state_num}: {desc}")

        # نمایش actions
        state_data = LR_PARSING_TABLE[state_num]
        actions = []
        gotos = []

        for symbol, action in state_data.items():
            if symbol in TERMINALS:
                actions.append(f"{symbol}→{action}")
            else:
                gotos.append(f"{symbol}→{action}")

        if actions:
            actions_str = ", ".join(actions[:4])
            if len(actions) > 4:
                actions_str += f", ... ({len(actions) - 4} more)"
            print(f"   ACTION: {actions_str}")
        else:
            print(f"   ACTION: —")

        if gotos:
            gotos_str = ", ".join(gotos)
            print(f"   GOTO:   {gotos_str}")

    # نمایش جدول ACTION خلاصه
    print("\n" + "─" * 80)
    print("📊 جدول ACTION (خلاصه):")
    print("─" * 80)

    print("\nState │ CLFLUSH │ CLWB │ PREFETCHT0 │ WBINVD │  [  │  ]  │  $  ")
    print("──────┼─────────┼──────┼────────────┼────────┼─────┼─────┼─────")

    key_states = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    for state in key_states:
        if state in LR_PARSING_TABLE:
            actions = LR_PARSING_TABLE[state]
            row = f"  {state:2d}  │"

            for terminal in ['CLFLUSH', 'CLWB', 'PREFETCHT0', 'WBINVD', '[', ']', '$']:
                action = actions.get(terminal, '')
                row += f"  {action:^6s} │"

            print(row)

    print("\n💡 نمادها:")
    print("  • s{n}  : Shift و برو به state n")
    print("  • r{n}  : Reduce با استفاده از قانون n")
    print("  • acc   : Accept - پذیرش ورودی")

    # توضیح تفاوت State 3 و State 4
    print("\n" + "─" * 80)
    print("⚠️  نکته مهم:")
    print("─" * 80)
    print("  • State 3: دستورات CLFLUSH، CLFLUSHOPT، CLWB و PREFETCH*")
    print("            همیشه نیاز به operand دارند → فقط [ می‌پذیرند")
    print()
    print("  • State 4: دستورات WBINVD و INVD")
    print("            نباید operand داشته باشند → فقط $ می‌پذیرند")

    # نمایش قوانین گرامر
    print("\n" + "─" * 80)
    print("📜 قوانین گرامر:")
    print("─" * 80)

    for rule_num in sorted(GRAMMAR_RULES.keys()):
        rule = GRAMMAR_RULES[rule_num]
        print(f"  R{rule_num:2d}: {rule}")

    # مثال پارسینگ
    print("\n" + "─" * 80)
    print("💡 مثال: پارسینگ 'CLFLUSH [EAX]'")
    print("─" * 80)

    parsing_steps = [
        ("1", "State 0", "Shift CLFLUSH", "→ State 3"),
        ("2", "State 3", "Reduce: mnemonic → CLFLUSH", "→ State 2"),
        ("3", "State 2", "Shift [", "→ State 6"),
        ("4", "State 6", "Shift EAX (REGISTER)", "→ State 8"),
        ("5", "State 8", "Reduce: base_expr → REGISTER", "→ State 7"),
        ("6", "State 7", "Shift ]", "→ State 10"),
        ("7", "State 10", "Reduce: memory_address → [ base_expr ]", "→ State 5"),
        ("8", "State 5", "Reduce: instruction → mnemonic operand", "→ State 1"),
        ("9", "State 1", "Accept", "✅ موفق"),
    ]

    for step, state, action, result in parsing_steps:
        print(f"  {step}. {state:12s} │ {action:45s} │ {result}")

    print("\n" + "═" * 80)


# ═════════════════════════════════════════════════════════════════════
# Main
# ═════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("╔" + "═" * 80 + "╗")
    print("║" + " " * 20 + "جدول پارس کامل LR(0) - گروه 15" + " " * 28 + "║")
    print("╚" + "═" * 80 + "╝")

    # 1. چاپ قوانین گرامر
    print_grammar_rules()

    # 2. چاپ جدول به فرمت ساده
    print_parsing_table()

    # 3. نمایش جداول برای main
    display_lr_tables()

    print("\n✅ جدول پارس کامل با موفقیت تولید شد!")
    print("📄 این جدول شامل تمام states و transitions است.")
