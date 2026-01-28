"""
رسم نمودار تعاملی و زیبا با PyVis
خروجی: فایل HTML قابل باز شدن در مرورگر
"""
import sys

try:
    from pyvis.network import Network
except ImportError:
    print("❌ کتابخانه pyvis نصب نیست. لطفاً دستور زیر را اجرا کنید:")
    print("pip install pyvis")
    sys.exit(1)


def create_beautiful_automata():
    print("⏳ در حال ساخت نمودار تعاملی...")

    # ساخت شبکه (Directed = جهت‌دار)
    net = Network(height='750px', width='100%', bgcolor='#222222', font_color='white', directed=True)

    # تنظیمات فیزیک برای چیدمان بهتر
    net.force_atlas_2based()

    # تعریف State ها
    # title: متنی که وقتی موس روی گره می‌رود نمایش داده می‌شود (قوانین کامل)
    # label: متنی که همیشه دیده می‌شود (نام State)
    states = {
        0: ("State 0", "Start\nS' -> . inst\ninst -> . mnem op\n..."),
        1: ("State 1", "Accept\nS' -> inst ."),
        2: ("State 2", "inst -> mnem . op\ninst -> mnem ."),
        3: ("State 3", "Reduce\nmnem -> CLFLUSH ."),
        4: ("State 4", "Reduce\nmnem -> WBINVD ."),
        5: ("State 5", "Reduce\ninst -> mnem op ."),
        6: ("State 6", "op -> [ . base ]"),
        7: ("State 7", "op -> [ base . ]"),
        8: ("State 8", "base -> REG . off\nbase -> REG ."),
        9: ("State 9", "Reduce\nbase -> ID ."),
        10: ("State 10", "Reduce\nop -> [ base ] ."),
        11: ("State 11", "Reduce\nbase -> REG off ."),
        12: ("State 12", "off -> + . NUM"),
        13: ("State 13", "Reduce\noff -> + NUM .")
    }

    # افزودن گره‌ها
    for sid, (label, tooltip) in states.items():
        # رنگ‌بندی: حالت‌های Reduce سبز، حالت‌های عادی آبی، شروع نارنجی
        if sid == 1:
            color = '#00ff00'  # سبز فسفری (Accept)
            shape = 'star'
        elif "Reduce" in tooltip:
            color = '#97c2fc'  # آبی روشن
            shape = 'box'
        elif sid == 0:
            color = '#ff9900'  # نارنجی (Start)
            shape = 'ellipse'
        else:
            color = '#ffff00'  # زرد
            shape = 'ellipse'

        net.add_node(sid, label=label, title=tooltip, color=color, shape=shape, size=25)

    # تعریف یال‌ها
    edges = [
        (0, 1, 'inst'), (0, 2, 'mnem'), (0, 3, 'CLFLUSH'),
        (0, 4, 'WBINVD'), (2, 5, 'op'), (2, 6, '['),
        (6, 7, 'base'), (6, 8, 'REG'), (6, 9, 'ID'),
        (7, 10, ']'), (8, 11, 'off'), (8, 12, '+'),
        (12, 13, 'NUM')
    ]

    # افزودن یال‌ها
    for src, dst, label in edges:
        net.add_edge(src, dst, label=label, color='white', arrows='to')

    # تنظیمات نهایی ظاهر
    net.set_options("""
    var options = {
      "edges": {
        "font": {
          "size": 16,
          "align": "middle"
        },
        "smooth": {
          "type": "curvedCW",
          "roundness": 0.2
        }
      },
      "physics": {
        "forceAtlas2Based": {
          "gravitationalConstant": -100,
          "springLength": 150,
          "springConstant": 0.05
        },
        "minVelocity": 0.75,
        "solver": "forceAtlas2Based"
      }
    }
    """)

    # ذخیره فایل HTML
    output_file = 'automata_interactive.html'
    net.show(output_file, notebook=False)
    print(f"✅ فایل ساخته شد: {output_file}")
    print("💡 این فایل را در مرورگر باز کنید تا نمودار تعاملی را ببینید.")


if __name__ == "__main__":
    create_beautiful_automata()
