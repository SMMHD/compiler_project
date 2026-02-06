#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اسکریپت تولید تصویر اتوماتای LR(0)
Generate LR(0) Automata Diagram
تیم 15 - پروژه کامپایلر
"""

import os
import subprocess
import sys

def check_graphviz():
    """بررسی نصب Graphviz"""
    try:
        result = subprocess.run(['dot', '-V'], 
                              capture_output=True, 
                              text=True)
        return True
    except FileNotFoundError:
        return False

def generate_diagram(dot_file, output_format='png'):
    """تولید دیاگرام از فایل DOT"""

    if not os.path.exists(dot_file):
        print(f"❌ خطا: فایل '{dot_file}' یافت نشد!")
        return False

    output_file = dot_file.replace('.dot', f'.{output_format}')

    print(f"🔄 در حال تولید {output_format.upper()}...")
    print(f"   ورودی: {dot_file}")
    print(f"   خروجی: {output_file}")

    try:
        cmd = ['dot', f'-T{output_format}', dot_file, '-o', output_file]
        result = subprocess.run(cmd, 
                              capture_output=True, 
                              text=True,
                              check=True)

        print(f"✅ فایل تولید شد: {output_file}")

        # نمایش اطلاعات فایل
        size = os.path.getsize(output_file)
        print(f"📊 حجم فایل: {size:,} بایت ({size/1024:.1f} KB)")

        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ خطا در تولید تصویر:")
        print(e.stderr)
        return False

def main():
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 20 + "تولید دیاگرام اتوماتای LR(0)" + " " * 29 + "║")
    print("╚" + "═" * 78 + "╝")
    print()

    # بررسی Graphviz
    print("🔍 بررسی Graphviz...")
    if not check_graphviz():
        print("❌ Graphviz نصب نیست!")
        print()
        print("💡 برای نصب:")
        print()
        print("  Ubuntu/Debian:")
        print("    sudo apt-get install graphviz")
        print()
        print("  macOS:")
        print("    brew install graphviz")
        print()
        print("  Windows:")
        print("    1. دانلود از: https://graphviz.org/download/")
        print("    2. نصب و اضافه کردن به PATH")
        print()
        print("  یا با pip:")
        print("    pip install graphviz")
        print()
        return

    print("✅ Graphviz نصب است")
    print()

    # فایل ورودی
    dot_file = 'lr0_automata_COMPLETE.dot'

    if not os.path.exists(dot_file):
        print(f"❌ فایل '{dot_file}' یافت نشد!")
        print("💡 ابتدا اسکریپت قبلی را اجرا کنید تا فایل DOT ایجاد شود.")
        return

    print("─" * 80)

    # تولید فرمت‌های مختلف
    formats = ['png', 'pdf', 'svg']

    success_count = 0
    for fmt in formats:
        if generate_diagram(dot_file, fmt):
            success_count += 1
        print()

    print("─" * 80)
    print(f"✅ {success_count}/{len(formats)} فرمت با موفقیت تولید شد")
    print()

    if success_count > 0:
        print("📁 فایل‌های تولید شده:")
        for fmt in formats:
            output_file = dot_file.replace('.dot', f'.{fmt}')
            if os.path.exists(output_file):
                print(f"  • {output_file}")
        print()
        print("💡 می‌توانید این فایل‌ها را در گزارش استفاده کنید:")
        print("  - PNG برای گزارش Word/PDF")
        print("  - PDF برای کیفیت بالا")
        print("  - SVG برای وب یا اسلاید")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 لغو شد")
    except Exception as e:
        print(f"\n❌ خطا: {e}")
        import traceback
        traceback.print_exc()
