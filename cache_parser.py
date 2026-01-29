#!/usr/bin/env python3
"""
Cache Control Instructions Parser
تحلیل‌گر نحوی برای دستورات کنترل کش
تیم 15 - پروژه کامپایلر - دانشگاه شهید باهنر کرمان

این فایل شامل:
- قوانین گرامر کامل
- ساخت Abstract Syntax Tree (AST)
- تحلیل Bottom-Up با LR Parser
- مدیریت خطا
- ابزارهای تست و نمایش
- Parse Tree کامل طبق گرامر BNF
"""

import ply.yacc as yacc
from cache_lexer import tokens, build_lexer
import json


# ═══════════════════════════════════════════════════════════════════
#                          AST Node Classes
# ═══════════════════════════════════════════════════════════════════

class ASTNode:
    """کلاس پایه برای تمام گره‌های درخت نحوی (Abstract Syntax Tree)"""

    def to_dict(self):
        """تبدیل گره به دیکشنری برای JSON"""
        raise NotImplementedError

    def pretty_print(self, indent=0):
        """نمایش زیبای درخت"""
        raise NotImplementedError


class Instruction(ASTNode):
    """
    گره دستور - ریشه AST

    Args:
        mnemonic: نام دستور (مثل CLFLUSH)
        operand: عملوند (آدرس حافظه یا None)
    """

    def __init__(self, mnemonic, operand=None):
        self.mnemonic = mnemonic
        self.operand = operand
        self.type = 'Instruction'

    def __repr__(self):
        if self.operand:
            return f"Instruction({self.mnemonic}, {self.operand})"
        return f"Instruction({self.mnemonic})"

    def to_dict(self):
        return {
            'type': 'Instruction',
            'mnemonic': self.mnemonic,
            'operand': self.operand.to_dict() if self.operand else None,
            'has_operand': self.operand is not None
        }

    def pretty_print(self, indent=0):
        """نمایش Parse Tree ساده‌شده (AST)"""
        prefix = "  " * indent
        lines = []
        lines.append(f"{prefix}Instruction: {self.mnemonic}")
        if self.operand:
            lines.append(f"{prefix}├─ Operand:")
            lines.extend(self.operand.pretty_print(indent + 1))
        else:
            lines.append(f"{prefix}└─ No Operand")
        return lines

    def full_parse_tree(self):
        """
        نمایش Parse Tree کامل طبق همه سطوح گرامر BNF
        این نمایش برای گزارش و ارائه به استاد مناسب است
        """
        lines = []
        lines.append("Instruction")

        # تشخیص نوع Mnemonic و دسته‌بندی
        category = self.get_instruction_category()

        category_mapping = {
            'flush': 'CacheFlush',
            'writeback': 'CacheWrite',
            'prefetch': 'CachePrefetch',
            'invalidate': 'CacheInvalidate'
        }

        category_name = category_mapping.get(category, 'Mnemonic')

        if self.operand:
            lines.append("├── Mnemonic")
            lines.append(f"│   └── {category_name}")
            lines.append(f"│       └── {self.mnemonic} (terminal)")
            lines.append("└── Operand")
            lines.append("    └── MemoryAddress")
            lines.append("        ├── [ (terminal)")
            lines.append("        ├── BaseExpr")

            # نوع Base (Register یا Identifier)
            if isinstance(self.operand.base, Register):
                lines.append("        │   ├── Register")
                lines.append(f"        │   │   └── {self.operand.base.name} (terminal)")

                # اگر Offset داشت
                if self.operand.offset:
                    lines.append("        │   └── Offset")
                    sign = self.operand.offset[0]
                    num = self.operand.offset[1:]
                    lines.append(f"        │       ├── {sign} (terminal)")
                    lines.append(f"        │       └── {num} (terminal)")
                else:
                    lines.append("        │   └── ε (no offset)")

            elif isinstance(self.operand.base, Identifier):
                lines.append("        │   └── Identifier")
                lines.append(f"        │       └── {self.operand.base.name} (terminal)")

            lines.append("        └── ] (terminal)")
        else:
            # دستور بدون Operand
            lines.append("└── Mnemonic")
            lines.append(f"    └── {category_name}")
            lines.append(f"        └── {self.mnemonic} (terminal)")

        return lines

    def derivation_steps(self):
        """
        نمایش مراحل اشتقاق (Derivation) از گرامر
        مفید برای گزارش
        """
        steps = []
        steps.append("Instruction")

        if self.operand:
            steps.append("→ Mnemonic Operand")

            category = self.get_instruction_category()
            if category == 'flush':
                steps.append("→ CacheFlush Operand")
            elif category == 'writeback':
                steps.append("→ CacheWrite Operand")
            elif category == 'prefetch':
                steps.append("→ CachePrefetch Operand")

            steps.append(f"→ {self.mnemonic} Operand")
            steps.append(f"→ {self.mnemonic} MemoryAddress")
            steps.append(f"→ {self.mnemonic} [ BaseExpr ]")

            if isinstance(self.operand.base, Register):
                if self.operand.offset:
                    steps.append(f"→ {self.mnemonic} [ Register Offset ]")
                    sign = self.operand.offset[0]
                    num = self.operand.offset[1:]
                    steps.append(f"→ {self.mnemonic} [ {self.operand.base.name} {sign} {num} ]")
                else:
                    steps.append(f"→ {self.mnemonic} [ Register ]")
                    steps.append(f"→ {self.mnemonic} [ {self.operand.base.name} ]")
            else:
                steps.append(f"→ {self.mnemonic} [ Identifier ]")
                steps.append(f"→ {self.mnemonic} [ {self.operand.base.name} ]")
        else:
            # دستور بدون Operand (فقط WBINVD و INVD)
            steps.append("→ CacheInvalidate")
            steps.append(f"→ {self.mnemonic}")

        return steps

    def get_instruction_category(self):
        """دسته‌بندی نوع دستور"""
        categories = {
            'flush': ['CLFLUSH', 'CLFLUSHOPT'],
            'writeback': ['CLWB'],
            'prefetch': ['PREFETCHT0', 'PREFETCHT1', 'PREFETCHT2', 'PREFETCHNTA'],
            'invalidate': ['WBINVD', 'INVD']
        }

        for category, mnemonics in categories.items():
            if self.mnemonic in mnemonics:
                return category
        return 'unknown'


class MemoryOperand(ASTNode):
    """
    گره عملوند حافظه

    Args:
        base: رجیستر یا شناسه پایه
        offset: جابجایی (offset) نسبت به base
    """

    def __init__(self, base, offset=None):
        self.base = base
        self.offset = offset
        self.type = 'MemoryOperand'

    def __repr__(self):
        if self.offset:
            return f"Memory([{self.base}{self.offset}])"
        return f"Memory([{self.base}])"

    def to_dict(self):
        return {
            'type': 'MemoryOperand',
            'base': self.base.to_dict() if hasattr(self.base, 'to_dict') else str(self.base),
            'offset': self.offset,
            'has_offset': self.offset is not None
        }

    def pretty_print(self, indent=0):
        prefix = "  " * indent
        lines = []
        lines.append(f"{prefix}MemoryOperand:")
        lines.append(f"{prefix}├─ Base: {self.base}")
        if self.offset:
            lines.append(f"{prefix}└─ Offset: {self.offset}")
        else:
            lines.append(f"{prefix}└─ Offset: None")
        return lines


class Register(ASTNode):
    """
    گره رجیستر

    Args:
        name: نام رجیستر (مثل EAX، RBX)
    """

    def __init__(self, name):
        self.name = name
        self.type = 'Register'
        self.bit_width = 64 if name.startswith('R') else 32

    def __repr__(self):
        return f"Register({self.name})"

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            'type': 'Register',
            'name': self.name,
            'bit_width': self.bit_width
        }

    def pretty_print(self, indent=0):
        prefix = "  " * indent
        return [f"{prefix}Register: {self.name} ({self.bit_width}-bit)"]


class Identifier(ASTNode):
    """
    گره شناسه (لیبل)

    Args:
        name: نام شناسه (مثل cache_line، data_ptr)
    """

    def __init__(self, name):
        self.name = name
        self.type = 'Identifier'

    def __repr__(self):
        return f"Identifier({self.name})"

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            'type': 'Identifier',
            'name': self.name
        }

    def pretty_print(self, indent=0):
        prefix = "  " * indent
        return [f"{prefix}Identifier: {self.name}"]


# ═══════════════════════════════════════════════════════════════════
#                          Grammar Rules
# ═══════════════════════════════════════════════════════════════════

# ───────────────────────────────────────────────────────────────────
# قوانین دستورات با Operand (الزامی برای Flush، Prefetch، WriteBack)
# ───────────────────────────────────────────────────────────────────

# قانون 1: دستورات Flush با operand
def p_instruction_flush_with_operand(p):
    """instruction : flush_mnemonic operand"""
    p[0] = Instruction(p[1], p[2])
    if parser_debug:
        print(f"  [REDUCE] {p[1]} + Operand → Instruction (Flush)")


# قانون 2: دستورات Prefetch با operand
def p_instruction_prefetch_with_operand(p):
    """instruction : prefetch_mnemonic operand"""
    p[0] = Instruction(p[1], p[2])
    if parser_debug:
        print(f"  [REDUCE] {p[1]} + Operand → Instruction (Prefetch)")


# قانون 3: دستورات WriteBack با operand
def p_instruction_writeback_with_operand(p):
    """instruction : writeback_mnemonic operand"""
    p[0] = Instruction(p[1], p[2])
    if parser_debug:
        print(f"  [REDUCE] {p[1]} + Operand → Instruction (WriteBack)")


# ───────────────────────────────────────────────────────────────────
# قوانین دستورات بدون Operand (فقط برای Invalidate)
# ───────────────────────────────────────────────────────────────────

# قانون 4: فقط دستورات Invalidate می‌توانند بدون operand باشند
def p_instruction_invalidate_no_operand(p):
    """instruction : WBINVD
                   | INVD"""
    p[0] = Instruction(p[1])
    if parser_debug:
        print(f"  [REDUCE] {p[1]} → Instruction (Invalidate - no operand)")


# ───────────────────────────────────────────────────────────────────
# تعریف Mnemonics
# ───────────────────────────────────────────────────────────────────

# قانون 5: Flush Mnemonics
def p_flush_mnemonic(p):
    """flush_mnemonic : CLFLUSH
                      | CLFLUSHOPT"""
    p[0] = p[1]
    if parser_debug:
        print(f"  [REDUCE] {p[1]} → FlushMnemonic")


# قانون 6: Prefetch Mnemonics
def p_prefetch_mnemonic(p):
    """prefetch_mnemonic : PREFETCHT0
                         | PREFETCHT1
                         | PREFETCHT2
                         | PREFETCHNTA"""
    p[0] = p[1]
    if parser_debug:
        print(f"  [REDUCE] {p[1]} → PrefetchMnemonic")


# قانون 7: WriteBack Mnemonics
def p_writeback_mnemonic(p):
    """writeback_mnemonic : CLWB"""
    p[0] = p[1]
    if parser_debug:
        print(f"  [REDUCE] {p[1]} → WriteBackMnemonic")


# ───────────────────────────────────────────────────────────────────
# قوانین Operand
# ───────────────────────────────────────────────────────────────────

# قانون 8: Operand
def p_operand(p):
    """operand : memory_address"""
    p[0] = p[1]
    if parser_debug:
        print(f"  [REDUCE] MemoryAddress → Operand")


# قانون 9: آدرس حافظه
def p_memory_address(p):
    """memory_address : LBRACKET base_expr RBRACKET"""
    p[0] = p[2]
    if parser_debug:
        print(f"  [REDUCE] [ BaseExpr ] → MemoryAddress")


# قانون 10: عبارت پایه با offset
def p_base_expr_register_offset(p):
    """base_expr : REGISTER offset"""
    p[0] = MemoryOperand(Register(p[1]), p[2])
    if parser_debug:
        print(f"  [REDUCE] Register + Offset → BaseExpr")


# قانون 11: عبارت پایه بدون offset (رجیستر)
def p_base_expr_register(p):
    """base_expr : REGISTER"""
    p[0] = MemoryOperand(Register(p[1]))
    if parser_debug:
        print(f"  [REDUCE] Register → BaseExpr")


# قانون 12: عبارت پایه بدون offset (شناسه)
def p_base_expr_identifier(p):
    """base_expr : IDENTIFIER"""
    p[0] = MemoryOperand(Identifier(p[1]))
    if parser_debug:
        print(f"  [REDUCE] Identifier → BaseExpr")


# قانون 13: Offset مثبت
def p_offset_plus(p):
    """offset : PLUS NUMBER"""
    p[0] = f"+{p[2]}"
    if parser_debug:
        print(f"  [REDUCE] + NUMBER → Offset (+{p[2]})")


# قانون 14: Offset منفی
def p_offset_minus(p):
    """offset : MINUS NUMBER"""
    p[0] = f"-{p[2]}"
    if parser_debug:
        print(f"  [REDUCE] - NUMBER → Offset (-{p[2]})")


# ═══════════════════════════════════════════════════════════════════
#                          Error Handling
# ═══════════════════════════════════════════════════════════════════

def p_error(p):
    """مدیریت خطاهای نحوی"""
    if p:
        error_msg = f"""
╔════════════════════════════════════════════════════════════════╗
║                      SYNTAX ERROR                              ║
╚════════════════════════════════════════════════════════════════╝

  خطای نحوی در توکن: '{p.value}'
  نوع توکن: {p.type}
  موقعیت: خط {p.lineno}

  💡 احتمالا مشکل در:
     - فرمت دستور اشتباه است
     - کروشه باز یا بسته فراموش شده
     - عملوند نامعتبر
     - دستورات CLFLUSH، CLFLUSHOPT، CLWB و PREFETCH* نیاز به operand دارند

  ✓ فرمت صحیح:
     MNEMONIC [REGISTER]
     MNEMONIC [REGISTER+NUMBER]
     MNEMONIC [REGISTER-NUMBER]
     MNEMONIC [IDENTIFIER]
     WBINVD  (بدون operand)
     INVD    (بدون operand)
"""
        print(error_msg)

        # پیشنهاد اصلاح
        if p.type == 'REGISTER':
            print("  📌 پیشنهاد: رجیستر باید داخل کروشه باشد: [REGISTER]")
        elif p.type == 'NUMBER':
            print("  📌 پیشنهاد: قبل از عدد باید + یا - باشد")
        elif p.type in ['CLFLUSH', 'CLFLUSHOPT', 'CLWB', 'PREFETCHT0', 'PREFETCHT1', 'PREFETCHT2', 'PREFETCHNTA']:
            print(f"  📌 پیشنهاد: {p.type} نیاز به operand دارد → {p.type} [REGISTER]")

    else:
        print("""
╔════════════════════════════════════════════════════════════════╗
║                      SYNTAX ERROR                              ║
╚════════════════════════════════════════════════════════════════╝

  خطای نحوی در انتهای ورودی

  💡 احتمالا:
     - دستور ناقص است
     - کروشه بسته نشده
""")


# ═══════════════════════════════════════════════════════════════════
#                          Parser Builder
# ═══════════════════════════════════════════════════════════════════

# متغیر سراسری برای دیباگ
parser_debug = False


def build_parser(debug=False):
    """
    ساخت parser

    Args:
        debug: فعال‌سازی حالت دیباگ

    Returns:
        parser object
    """
    global parser_debug
    parser_debug = debug

    return yacc.yacc(debug=debug, write_tables=False)


# ═══════════════════════════════════════════════════════════════════
#                          Parse Functions
# ═══════════════════════════════════════════════════════════════════

def parse_instruction(code, debug=False):
    """
    پارس یک دستور

    Args:
        code: رشته دستور assembly
        debug: نمایش مراحل پارسینگ

    Returns:
        AST node یا None در صورت خطا
    """
    lexer = build_lexer()
    parser = build_parser(debug=debug)

    try:
        result = parser.parse(code, lexer=lexer)
        return result
    except Exception as e:
        print(f"❌ خطا در پارسینگ: {e}")
        return None


def parse_file(filename, debug=False):
    """
    پارس یک فایل assembly

    Args:
        filename: نام فایل
        debug: نمایش مراحل

    Returns:
        لیست AST nodes
    """
    lexer = build_lexer()
    parser = build_parser(debug=debug)

    results = []
    errors = []

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        for line_num, line in enumerate(lines, 1):
            line = line.strip()

            # رد کردن خطوط خالی و کامنت‌ها
            if not line or line.startswith(';'):
                continue

            # حذف کامنت انتهای خط
            if ';' in line:
                line = line.split(';')[0].strip()

            try:
                ast = parser.parse(line, lexer=lexer)
                if ast:
                    results.append((line_num, line, ast))
            except Exception as e:
                errors.append((line_num, line, str(e)))

    except FileNotFoundError:
        print(f"❌ فایل '{filename}' پیدا نشد")
        return None

    return results, errors


# ═══════════════════════════════════════════════════════════════════
#                          Analysis Tools
# ═══════════════════════════════════════════════════════════════════

def analyze_instruction(ast):
    """تحلیل دقیق یک دستور"""

    category = ast.get_instruction_category()

    category_desc = {
        'flush': 'Cache Flush - پاک‌سازی خط کش',
        'writeback': 'Cache Write-Back - نوشتن به حافظه اصلی',
        'prefetch': 'Cache Prefetch - پیش‌خوانی داده',
        'invalidate': 'Cache Invalidate - باطل‌سازی کش'
    }

    analysis = {
        'mnemonic': ast.mnemonic,
        'category': category,
        'description': category_desc.get(category, 'نامشخص'),
        'has_operand': ast.operand is not None,
    }

    if ast.operand:
        mem = ast.operand
        analysis['operand'] = {
            'base_type': mem.base.type,
            'base_value': str(mem.base),
            'has_offset': mem.offset is not None,
            'offset_value': mem.offset
        }

        if isinstance(mem.base, Register):
            analysis['operand']['register_width'] = mem.base.bit_width

    return analysis


def print_analysis(analysis):
    """نمایش تحلیل"""
    print("\n" + "═" * 70)
    print(f"  دستور: {analysis['mnemonic']}")
    print("═" * 70)
    print(f"  دسته: {analysis['description']}")
    print(f"  دارای Operand: {'✓' if analysis['has_operand'] else '✗'}")

    if analysis['has_operand']:
        op = analysis['operand']
        print(f"  نوع Base: {op['base_type']}")
        print(f"  مقدار Base: {op['base_value']}")
        if 'register_width' in op:
            print(f"  عرض رجیستر: {op['register_width']}-bit")
        if op['has_offset']:
            print(f"  Offset: {op['offset_value']}")

    print("═" * 70)


# ═══════════════════════════════════════════════════════════════════
#                          Main Test
# ═══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("═" * 70)
    print("  تست Parser برای دستورات کنترل کش")
    print("  دانشگاه شهید باهنر کرمان - تیم 15")
    print("═" * 70)

    # تست کیس‌ها
    test_cases = [
        ("CLFLUSH [EAX]", "دستور ساده با رجیستر"),
        ("CLFLUSHOPT [EBX+16]", "دستور با offset مثبت"),
        ("PREFETCHT0 [ECX-8]", "دستور با offset منفی"),
        ("WBINVD", "دستور بدون operand"),
        ("CLWB [cache_line]", "دستور با شناسه"),
        ("PREFETCHNTA [RAX+128]", "رجیستر 64-bit"),
        ("CLFLUSHOPT", "خطا - CLFLUSHOPT بدون operand"),  # باید خطا دهد
    ]

    print(f"\n📝 تعداد تست‌ها: {len(test_cases)}\n")

    success_count = 0
    error_count = 0

    for i, (code, description) in enumerate(test_cases, 1):
        print(f"\n{'─' * 70}")
        print(f"تست {i}/{len(test_cases)}: {description}")
        print(f"کد: {code}")
        print('─' * 70)

        ast = parse_instruction(code, debug=False)

        if ast:
            print("\n✅ پارس موفق!")
            print(f"\nAST: {ast}")

            # نمایش Parse Tree ساده (AST)
            print("\n🌳 Parse Tree (ساده‌شده - AST):")
            for line in ast.pretty_print():
                print("  " + line)

            # نمایش Parse Tree کامل طبق گرامر
            print("\n🌲 Parse Tree (کامل - طبق گرامر BNF):")
            for line in ast.full_parse_tree():
                print("  " + line)

            # نمایش مراحل اشتقاق
            print("\n📐 مراحل اشتقاق (Derivation):")
            for step in ast.derivation_steps():
                print(f"  {step}")

            # تحلیل
            analysis = analyze_instruction(ast)
            print_analysis(analysis)

            # JSON
            print("\n📄 JSON Output:")
            print(json.dumps(ast.to_dict(), indent=2, ensure_ascii=False))

            success_count += 1
        else:
            print("\n❌ پارس ناموفق!")
            error_count += 1

    print("\n" + "═" * 70)
    print(f"  نتیجه: {success_count} موفق، {error_count} ناموفق")
    print("═" * 70)
