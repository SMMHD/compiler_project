#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اسکریپت تولید خودکار جدول LR(0) از lr_tables.py
Auto-generate LR(0) table in various formats
تیم 15 - پروژه کامپایلر
"""

import os
import sys

def import_lr_tables():
    """Import کردن جدول و قوانین از lr_tables.py"""
    try:
        from lr_tables import LR_PARSING_TABLE, GRAMMAR_RULES
        return LR_PARSING_TABLE, GRAMMAR_RULES
    except ImportError:
        print("❌ خطا: فایل lr_tables.py یافت نشد!")
        print("💡 این اسکریپت باید در همان پوشه lr_tables.py اجرا شود.")
        return None, None

def generate_markdown_table(table, grammar):
    """تولید جدول به فرمت Markdown"""

    output = []
    output.append("# LR(0) Parsing Table")
    output.append("")
    output.append("## ACTION and GOTO Table")
    output.append("")

    # هدر جدول
    output.append("| State | Action | GOTO |")
    output.append("|-------|--------|------|")

    for state in sorted(table.keys()):
        actions = table[state]

        # استخراج action ها
        action_list = []
        goto_list = []

        for symbol, value in actions.items():
            if isinstance(value, int):
                goto_list.append(f"{symbol}→{value}")
            else:
                action_list.append(f"{symbol}:{value}")

        action_str = ", ".join(action_list) if action_list else "-"
        goto_str = ", ".join(goto_list) if goto_list else "-"

        output.append(f"| {state} | {action_str} | {goto_str} |")

    output.append("")
    output.append("## Grammar Rules")
    output.append("")

    for rule_num in sorted(grammar.keys()):
        output.append(f"- **R{rule_num}**: `{grammar[rule_num]}`")

    return "\n".join(output)

def generate_html_table(table, grammar):
    """تولید جدول به فرمت HTML"""

    html = []
    html.append("<!DOCTYPE html>")
    html.append("<html><head>")
    html.append("<meta charset='UTF-8'>")
    html.append("<title>LR(0) Parsing Table</title>")
    html.append("<style>")
    html.append("body { font-family: 'Courier New', monospace; margin: 20px; }")
    html.append("table { border-collapse: collapse; margin: 20px 0; }")
    html.append("th, td { border: 1px solid #333; padding: 8px 12px; text-align: center; }")
    html.append("th { background-color: #4CAF50; color: white; }")
    html.append("tr:nth-child(even) { background-color: #f2f2f2; }")
    html.append(".action { background-color: #ffe6e6; }")
    html.append(".goto { background-color: #e6f3ff; }")
    html.append("</style>")
    html.append("</head><body>")
    html.append("<h1>LR(0) Parsing Table</h1>")

    # جدول
    html.append("<table>")
    html.append("<tr><th>State</th><th class='action'>ACTION</th><th class='goto'>GOTO</th></tr>")

    for state in sorted(table.keys()):
        actions = table[state]

        action_list = []
        goto_list = []

        for symbol, value in actions.items():
            if isinstance(value, int):
                goto_list.append(f"{symbol}→{value}")
            else:
                action_list.append(f"{symbol}:{value}")

        action_str = "<br>".join(action_list) if action_list else "-"
        goto_str = "<br>".join(goto_list) if goto_list else "-"

        html.append(f"<tr><td>{state}</td><td class='action'>{action_str}</td><td class='goto'>{goto_str}</td></tr>")

    html.append("</table>")

    # قوانین
    html.append("<h2>Grammar Rules</h2>")
    html.append("<ul>")
    for rule_num in sorted(grammar.keys()):
        html.append(f"<li><strong>R{rule_num}:</strong> <code>{grammar[rule_num]}</code></li>")
    html.append("</ul>")

    html.append("</body></html>")

    return "\n".join(html)

def generate_csv_table(table, grammar):
    """تولید جدول به فرمت CSV"""

    csv = []
    csv.append("State,Terminal/Non-terminal,Action/Goto")

    for state in sorted(table.keys()):
        actions = table[state]

        for symbol, value in sorted(actions.items()):
            csv.append(f"{state},{symbol},{value}")

    return "\n".join(csv)

def main():
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 20 + "تولید جدول LR(0) از lr_tables.py" + " " * 24 + "║")
    print("╚" + "═" * 78 + "╝")
    print()

    # Import جدول
    print("🔄 در حال بارگذاری lr_tables.py...")
    table, grammar = import_lr_tables()

    if table is None or grammar is None:
        return

    print(f"✅ بارگذاری موفق:")
    print(f"   • {len(table)} state")
    print(f"   • {len(grammar)} قانون گرامر")
    print()

    # تولید فرمت‌های مختلف
    formats = {
        'markdown': ('LR_TABLE.md', generate_markdown_table),
        'html': ('LR_TABLE.html', generate_html_table),
        'csv': ('LR_TABLE.csv', generate_csv_table)
    }

    print("─" * 80)

    for fmt_name, (filename, generator) in formats.items():
        print(f"🔄 تولید {fmt_name.upper()}...")

        try:
            content = generator(table, grammar)

            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)

            size = os.path.getsize(filename)
            print(f"  ✓ {filename} ({size:,} bytes)")

        except Exception as e:
            print(f"  ✗ خطا در تولید {fmt_name}: {e}")

        print()

    print("─" * 80)
    print("✅ تولید فایل‌ها کامل شد!")
    print()

    print("📁 فایل‌های تولید شده:")
    print("  • LR_TABLE.md    → برای GitHub, GitLab")
    print("  • LR_TABLE.html  → برای مرورگر (قابل چاپ)")
    print("  • LR_TABLE.csv   → برای Excel, Google Sheets")
    print()

    print("💡 برای مشاهده:")
    print("  - Markdown: در GitHub یا VSCode")
    print("  - HTML: باز کردن در مرورگر")
    print("  - CSV: باز کردن در Excel")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 لغو شد")
    except Exception as e:
        print(f"\n❌ خطا: {e}")
        import traceback
        traceback.print_exc()
