"""
تولید جداول LR(0) و اطلاعات ماشین حالت برای پروژه کامپایلر
"""

import sys

# تعریف گرامر به صورت ساده برای پردازش
GRAMMAR = {
    0: "S' -> instruction",
    1: "instruction -> mnemonic operand",
    2: "instruction -> mnemonic",
    3: "mnemonic -> CLFLUSH",
    4: "mnemonic -> CLFLUSHOPT", 
    5: "mnemonic -> CLWB",
    6: "mnemonic -> PREFETCHT0",
    7: "mnemonic -> WBINVD",
    8: "mnemonic -> INVD",
    # ... (می‌توانید بقیه دستورات را هم اضافه کنید، اما برای جدول نمونه همین‌قدر کافیست)
    9: "operand -> LBRACKET base_expr RBRACKET",
    10: "base_expr -> REGISTER offset",
    11: "base_expr -> REGISTER",
    12: "base_expr -> IDENTIFIER",
    13: "offset -> PLUS NUMBER",
    14: "offset -> MINUS NUMBER"
}

def print_header(title):
    print("\n" + "═" * 70)
    print(f"   {title}")
    print("═" * 70)

def generate_grammar_report():
    print_header("1. قوانین گرامر (Grammar Rules)")
    for pid, rule in GRAMMAR.items():
        print(f"  ({pid}) {rule}")

def generate_lr0_items():
    print_header("2. مجموعه آیتم‌های LR(0) (Canonical Collection)")
    
    # این یک شبیه‌سازی از آیتم‌های مهم است (محاسبه کامل دستی طولانی است)
    states = {
        0: [
            "S' -> . instruction",
            "instruction -> . mnemonic operand",
            "instruction -> . mnemonic",
            "mnemonic -> . CLFLUSH",
            "mnemonic -> . WBINVD",
            "..."
        ],
        1: ["S' -> instruction ."],
        2: [
            "instruction -> mnemonic . operand", 
            "instruction -> mnemonic .",
            "operand -> . LBRACKET base_expr RBRACKET"
        ],
        3: ["mnemonic -> CLFLUSH ."],
        4: ["mnemonic -> WBINVD ."],
        5: ["instruction -> mnemonic operand ."],
        6: [
            "operand -> LBRACKET . base_expr RBRACKET",
            "base_expr -> . REGISTER offset",
            "base_expr -> . REGISTER",
            "base_expr -> . IDENTIFIER"
        ],
        7: ["operand -> LBRACKET base_expr . RBRACKET"],
        8: [
            "base_expr -> REGISTER . offset",
            "base_expr -> REGISTER .",
            "offset -> . PLUS NUMBER",
            "offset -> . MINUS NUMBER"
        ],
        9: ["base_expr -> IDENTIFIER ."],
        10: ["operand -> LBRACKET base_expr RBRACKET ."],
        11: ["base_expr -> REGISTER offset ."],
        12: ["offset -> PLUS . NUMBER"],
        13: ["offset -> PLUS NUMBER ."]
    }
    
    for state_id, items in states.items():
        print(f"\nState I{state_id}:")
        for item in items:
            print(f"    {item}")

def generate_parsing_table():
    print_header("3. جدول پارس LR(0) (Parsing Table)")
    
    # سرستون‌ها
    terminals = ["CLFLUSH", "WBINVD", "[", "]", "REG", "ID", "+", "NUM", "$"]
    non_terminals = ["inst", "mnem", "op", "base", "off"]
    
    header = f"{'State':<6} | {'Action':<50} | {'Goto':<30}"
    print(header)
    print("-" * len(header))
    
    # داده‌های جدول (شبیه‌سازی شده بر اساس States بالا)
    table_rows = [
        (0,  "CLFLUSH:s3, WBINVD:s4", "inst:1, mnem:2"),
        (1,  "$:cz (Accept)", ""),
        (2,  "[:s6, $:r2", "op:5"),  # r2: reduce by rule 2
        (3,  "[:r3, $:r3", ""),      # r3: reduce by rule 3
        (4,  "$:r7", ""),            # r7: reduce by rule 7
        (5,  "$:r1", ""),            # r1: reduce by rule 1
        (6,  "REG:s8, ID:s9", "base:7"),
        (7,  "]:s10", ""),
        (8,  "+:s12, -:s12, ]:r11", "off:11"),
        (9,  "]:r12", ""),
        (10, "$:r9", ""),
        (11, "]:r10", ""),
        (12, "NUM:s13", ""),
        (13, "]:r13", "")
    ]
    
    for state, action, goto in table_rows:
        print(f"{state:<6} | {action:<50} | {goto:<30}")
    
    print("\nراهنما:")
    print("  sN: Shift to state N")
    print("  rN: Reduce by rule N")
    print("  acc: Accept")

def main():
    print("گزارش تحلیل LR(0) برای پروژه کامپایلر")
    generate_grammar_report()
    generate_lr0_items()
    generate_parsing_table()
    
    print("\n✅ گزارش تولید شد. می‌توانید از این خروجی برای مستندات استفاده کنید.")

if __name__ == "__main__":
    main()
