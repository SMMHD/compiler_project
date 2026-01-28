"""
تست سریع Parser دستورات کش (نسخه ویندوز)
برای اجرا: python quick_test.py
"""

import sys
import time

# ---------------------------------------------------------
# تابع برای چاپ سرتیترهای زیبا
# ---------------------------------------------------------
def print_header(title):
    print("\n" + "═" * 60)
    print(f"   {title}")
    print("═" * 60)

# ---------------------------------------------------------
# تابع اصلی اجرای هر تست
# ---------------------------------------------------------
def run_test(name, code_to_test, expected_mnemonic=None, expected_offset=None):
    print(f"🔹 تست: {name}")
    print(f"   کد: {code_to_test}")
    
    try:
        # تلاش برای وارد کردن پارسر (Import)
        # این کار داخل تابع است تا اگر فایل نبود، برنامه کامل متوقف نشود
        from cache_parser import parse_instruction
        
        # اندازه‌گیری زمان اجرا
        start_time = time.time()
        ast = parse_instruction(code_to_test)
        duration = (time.time() - start_time) * 1000
        
        if ast:
            print(f"   ✅ موفق ({duration:.2f}ms)")
            
            # چک کردن نام دستور (Mnemonic)
            if expected_mnemonic and ast.mnemonic != expected_mnemonic:
                print(f"      ⚠️ هشدار: Mnemonic اشتباه است (انتظار: {expected_mnemonic}, دریافت: {ast.mnemonic})")
                return False
                
            # چک کردن افست (Offset) اگر وجود داشته باشد
            if expected_offset:
                if not ast.operand or ast.operand.offset != expected_offset:
                    print(f"      ⚠️ هشدار: Offset اشتباه است")
                    return False
            
            return True
        else:
            print("   ❌ ناموفق (Parse result is None)")
            return False
            
    except ImportError:
        print("   ❌ خطا: فایل cache_parser.py پیدا نشد!")
        print("      (مطمئن شوید که فایل cache_parser.py در کنار همین فایل است)")
        return False
    except Exception as e:
        print(f"   ❌ خطا: {e}")
        return False

# ---------------------------------------------------------
# تابع برای نمایش نمونه درخت (فقط در صورت موفقیت)
# ---------------------------------------------------------
def show_tree_demo():
    print_header("نمایش Parse Tree (نمونه)")
    try:
        from cache_parser import parse_instruction
        code = "CLFLUSHOPT [EBX+16]"
        ast = parse_instruction(code)
        
        print(f"کد نمونه: {code}\n")
        if ast:
            # چاپ خط به خط درخت
            for line in ast.pretty_print():
                print(line)
        else:
            print("❌ پارس نشد")
            
    except Exception as e:
        print(f"❌ خطا: {e}")

# ---------------------------------------------------------
# تابع اصلی برنامه
# ---------------------------------------------------------
def main():
    print_header("🚀 شروع تست سریع Parser")
    
    # لیست تست‌هایی که انجام می‌شوند
    # فرمت: (نام تست، کد اسمبلی، نام دستور مورد انتظار، افست مورد انتظار)
    tests = [
        ("دستور ساده", "CLFLUSH [EAX]", "CLFLUSH", None),
        ("دستور با Offset مثبت", "CLFLUSHOPT [EBX+16]", "CLFLUSHOPT", "+16"),
        ("دستور با Offset منفی", "PREFETCHT0 [ECX-8]", "PREFETCHT0", "-8"),
        ("دستور بدون Operand", "WBINVD", "WBINVD", None),
        ("دستور با Label", "CLWB [cache_line]", "CLWB", None),
        ("دستور 64 بیتی", "PREFETCHNTA [RAX+128]", "PREFETCHNTA", "+128"),
    ]
    
    passed = 0
    # حلقه برای اجرای تک تک تست‌ها
    for name, code, mnemonic, offset in tests:
        if run_test(name, code, mnemonic, offset):
            passed += 1
        print("-" * 40)
            
    # نمایش خلاصه نتایج
    print_header("📊 نتیجه نهایی")
    print(f"تعداد کل تست‌ها: {len(tests)}")
    print(f"تعداد موفق:      {passed}")
    print(f"تعداد ناموفق:    {len(tests) - passed}")
    
    if passed == len(tests):
        print("\n🎉 عالی! همه چیز درست کار می‌کند.")
        show_tree_demo()
    else:
        print("\n⚠️ برخی تست‌ها شکست خوردند. لطفا خطاها را بررسی کنید.")

if __name__ == "__main__":
    main()
