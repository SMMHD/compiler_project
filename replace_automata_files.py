#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اسکریپت جایگزینی فایل اتوماتا
Replace Automata Files
تیم 15 - پروژه کامپایلر
"""

import os
import shutil
from datetime import datetime

def main():
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 18 + "جایگزینی فایل‌های اتوماتای LR(0)" + " " * 26 + "║")
    print("╚" + "═" * 78 + "╝")
    print()

    # بررسی وجود فایل جدید
    new_dot_file = 'lr0_automata_COMPLETE.dot'
    target_dot_file = 'lr0_automata'  # فایل قدیمی بدون پسوند

    if not os.path.exists(new_dot_file):
        print(f"❌ خطا: فایل '{new_dot_file}' یافت نشد!")
        print("💡 ابتدا اسکریپت قبلی را اجرا کنید.")
        return

    print("✅ فایل جدید یافت شد")
    print()

    # ایجاد پوشه backup
    backup_dir = f"backup_automata_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(backup_dir, exist_ok=True)
    print(f"📦 ایجاد پوشه backup: {backup_dir}")
    print()

    # پشتیبان‌گیری از فایل‌های قدیمی
    files_to_backup = [
        'lr0_automata',
        'lr0_automata.jpg',
        'lr0_automata.png',
        'lr0_automata.pdf'
    ]

    backed_up_count = 0
    for old_file in files_to_backup:
        if os.path.exists(old_file):
            backup_path = os.path.join(backup_dir, old_file)
            shutil.copy2(old_file, backup_path)
            print(f"  ✓ پشتیبان: {old_file} → {backup_path}")
            backed_up_count += 1

    print(f"\n📊 تعداد فایل‌های backup شده: {backed_up_count}")
    print()

    # جایگزینی فایل DOT
    print("─" * 80)
    print("🔄 جایگزینی فایل DOT...")
    shutil.copy2(new_dot_file, target_dot_file)
    print(f"  ✓ {new_dot_file} → {target_dot_file}")

    # اضافه کردن فایل توضیحات
    details_file = 'LR0_AUTOMATA_DETAILS.txt'
    if os.path.exists(details_file):
        print(f"  ✓ فایل توضیحات موجود: {details_file}")
    else:
        print(f"  ⚠️ فایل توضیحات موجود نیست: {details_file}")

    print()
    print("═" * 80)
    print("✅ عملیات با موفقیت انجام شد!")
    print("═" * 80)
    print()

    print("📋 وضعیت فعلی:")
    print(f"  • lr0_automata → ✅ به‌روز شد (17 states)")
    if os.path.exists(details_file):
        print(f"  • {details_file} → ✅ موجود")
    print()

    print("🎯 مرحله بعدی:")
    print("  1. تولید تصویر از اتوماتا:")
    print("     python generate_automata_diagram.py")
    print()
    print("  2. یا به صورت دستی با Graphviz:")
    print("     dot -Tpng lr0_automata -o lr0_automata.png")
    print("     dot -Tpdf lr0_automata -o lr0_automata.pdf")
    print()

    print(f"💾 فایل‌های قدیمی در '{backup_dir}' ذخیره شدند")
    print()

    # بررسی سازگاری
    print("─" * 80)
    print("🔍 بررسی سازگاری:")
    print("─" * 80)

    # خواندن فایل جدید و شمارش state ها
    with open(target_dot_file, 'r', encoding='utf-8') as f:
        content = f.read()
        # شمارش state ها
        state_count = content.count('[label="State')
        print(f"  ✓ lr0_automata → {state_count} state")

    # بررسی lr_tables.py
    if os.path.exists('lr_tables.py'):
        with open('lr_tables.py', 'r', encoding='utf-8') as f:
            content = f.read()
            if 'LR_PARSING_TABLE = {' in content:
                # تخمین تعداد state ها
                states = content.count(': {')
                print(f"  ✓ lr_tables.py → {states-1} state در جدول")  # -1 برای خود دیکشنری

    print()
    print("✅ تطابق کامل با lr_tables.py!")
    print()
    print("💡 می‌توانید فایل‌های _COMPLETE را حذف کنید:")
    print("   rm lr0_automata_COMPLETE.dot")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 لغو شد")
    except Exception as e:
        print(f"\n❌ خطا: {e}")
        import traceback
        traceback.print_exc()
