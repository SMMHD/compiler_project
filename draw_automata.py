"""
رسم نمودار ماشین حالت LR(0) - نسخه ساده و امن
برای اجرا: python draw_automata.py
"""

import sys

try:
    from graphviz import Digraph
except ImportError:
    print("❌ کتابخانه graphviz نصب نیست.")
    sys.exit(1)

def create_automata():
    print("⏳ در حال تولید نمودار...")

    # استفاده از تنظیمات ساده که خطا ندهد
    dot = Digraph(comment='LR(0) Automata', format='png')
    dot.attr(rankdir='LR')

    # تنظیمات گره‌ها: مستطیل ساده با گوشه‌های گرد
    dot.attr('node', shape='box', style='filled', fontname='Consolas')

    # متن ساده برای هر State (بدون کاراکترهای عجیب)
    states = {
        0: "State 0\nS -> . inst\ninst -> . mnem op",
        1: "State 1\nS -> inst . (Accept)",
        2: "State 2\ninst -> mnem . op\ninst -> mnem .",
        3: "State 3\nmnem -> CLFLUSH .",
        4: "State 4\nmnem -> WBINVD .",
        5: "State 5\ninst -> mnem op .",
        6: "State 6\nop -> [ . base ]",
        7: "State 7\nop -> [ base . ]",
        8: "State 8\nbase -> REG . off\nbase -> REG .",
        9: "State 9\nbase -> ID .",
        10: "State 10\nop -> [ base ] .",
        11: "State 11\nbase -> REG off .",
        12: "State 12\noff -> + . NUM",
        13: "State 13\noff -> + NUM ."
    }

    for sid, label in states.items():
        # رنگ‌آمیزی ساده
        is_reduce = sid in [1, 3, 4, 5, 9, 10, 11, 13]
        color = '#90EE90' if is_reduce else '#E0FFFF'  # سبز روشن / آبی روشن

        # ساخت گره با لیبل متنی ساده
        dot.node(str(sid), label=label, fillcolor=color)

    # یال‌ها
    edges = [
        ('0', '1', 'inst'), ('0', '2', 'mnem'), ('0', '3', 'CLFLUSH'),
        ('0', '4', 'WBINVD'), ('2', '5', 'op'), ('2', '6', '['),
        ('6', '7', 'base'), ('6', '8', 'REG'), ('6', '9', 'ID'),
        ('7', '10', ']'), ('8', '11', 'off'), ('8', '12', '+'),
        ('12', '13', 'NUM')
    ]

    for src, dst, label in edges:
        dot.edge(src, dst, label=label)

    try:
        output_filename = 'lr0_automata'
        output_path = dot.render(output_filename, view=True)
        print(f"\n✅ نمودار با موفقیت ساخته شد!")
        print(f"📁 فایل ذخیره شده: {output_path}")
    except Exception as e:
        print(f"\n❌ خطا: {e}")
        print("مطمئن شوید که Graphviz درست نصب شده است.")

if __name__ == "__main__":
    create_automata()
