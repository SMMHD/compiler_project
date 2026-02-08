; ══════════════════════════════════════════════════════════════════
; Advanced Test Suite - Cache Control Instructions
; ══════════════════════════════════════════════════════════════════
; تست پیشرفته برای تمام حالات ممکن
; تیم 15 - پروژه کامپایلر
; ══════════════════════════════════════════════════════════════════

; ────────────────────────────────────────────────────────────────
; بخش 1: رجیسترهای 32-bit با offset های مختلف
; ────────────────────────────────────────────────────────────────

CLFLUSH [EAX]
CLFLUSH [EBX+1]
CLFLUSH [ECX+16]
CLFLUSH [EDX+256]
CLFLUSH [ESI-1]
CLFLUSH [EDI-32]
CLFLUSH [EBP-512]
CLFLUSH [ESP+0]

; ────────────────────────────────────────────────────────────────
; بخش 2: رجیسترهای 64-bit با offset های بزرگ
; ────────────────────────────────────────────────────────────────

CLFLUSHOPT [RAX]
CLFLUSHOPT [RBX+128]
CLFLUSHOPT [RCX+1024]
CLFLUSHOPT [RDX+4096]
CLFLUSHOPT [RSI-256]
CLFLUSHOPT [RDI-2048]
CLFLUSHOPT [RBP-8192]
CLFLUSHOPT [RSP+65536]

; ────────────────────────────────────────────────────────────────
; بخش 3: رجیسترهای مدرن R8-R15 (32 و 64 بیتی)
; ────────────────────────────────────────────────────────────────

PREFETCHT0 [R8]
PREFETCHT0 [R9+8]
PREFETCHT0 [R10-16]
PREFETCHT0 [R11+32]
PREFETCHT0 [R12-64]
PREFETCHT0 [R13+128]
PREFETCHT0 [R14-256]
PREFETCHT0 [R15+512]

PREFETCHT1 [R8D]
PREFETCHT1 [R9D+4]
PREFETCHT1 [R10D-8]
PREFETCHT1 [R11D+16]
PREFETCHT1 [R12D-32]
PREFETCHT1 [R13D+64]
PREFETCHT1 [R14D-128]
PREFETCHT1 [R15D+256]

; ────────────────────────────────────────────────────────────────
; بخش 4: تمام انواع Prefetch
; ────────────────────────────────────────────────────────────────

PREFETCHT0 [EAX+100]
PREFETCHT1 [EBX+200]
PREFETCHT2 [ECX+300]
PREFETCHNTA [EDX+400]

PREFETCHT0 [RAX-100]
PREFETCHT1 [RBX-200]
PREFETCHT2 [RCX-300]
PREFETCHNTA [RDX-400]

; ────────────────────────────────────────────────────────────────
; بخش 5: دستورات Write-Back با حالات مختلف
; ────────────────────────────────────────────────────────────────

CLWB [EAX]
CLWB [EBX+10]
CLWB [ECX-20]
CLWB [RAX+1000]
CLWB [RBX-2000]
CLWB [R8+500]
CLWB [R15D-750]

; ────────────────────────────────────────────────────────────────
; بخش 6: Labels و Identifiers مختلف
; ────────────────────────────────────────────────────────────────

CLFLUSH [buffer]
CLFLUSH [data_ptr]
CLFLUSH [cache_line_1]
CLFLUSH [my_var_123]
CLFLUSH [temp_buffer]

PREFETCHT0 [image_data]
PREFETCHNTA [audio_buffer]
CLWB [video_frame]
CLFLUSHOPT [network_packet]

; ────────────────────────────────────────────────────────────────
; بخش 7: دستورات Invalidate (بدون operand)
; ────────────────────────────────────────────────────────────────

WBINVD
INVD
WBINVD
INVD

; ────────────────────────────────────────────────────────────────
; بخش 8: ترکیب‌های خاص و Edge Cases
; ────────────────────────────────────────────────────────────────

CLFLUSH [EAX+0]
CLFLUSHOPT [RBX+1]
PREFETCHT0 [ECX-1]
CLWB [RDX+99999]

; Offset های کوچک
PREFETCHT1 [ESI+2]
PREFETCHT2 [EDI+3]
PREFETCHNTA [EBP+4]

; Offset های بزرگ
CLFLUSH [RAX+32768]
CLFLUSHOPT [RBX-16384]
CLWB [RCX+8192]

; رجیسترهای خاص
PREFETCHT0 [RIP+100]
CLFLUSH [RSP+8]
CLWB [RBP-16]

; Labels با فرمت‌های مختلف
PREFETCHNTA [var1]
CLFLUSH [MyVariable]
CLWB [BUFFER_SIZE]
CLFLUSHOPT [temp_123_data]

; ────────────────────────────────────────────────────────────────
; بخش 9: سناریوهای واقعی استفاده
; ────────────────────────────────────────────────────────────────

; Loop optimization
PREFETCHT0 [RDI+64]
PREFETCHT0 [RDI+128]
PREFETCHT0 [RDI+192]

; Multi-level cache prefetch
PREFETCHT0 [RAX]
PREFETCHT1 [RAX]
PREFETCHT2 [RAX]

; Cache line flushing sequence
CLFLUSH [RBX]
CLFLUSH [RBX+64]
CLFLUSH [RBX+128]

; Write-back sequence
CLWB [RSI]
CLWB [RSI+64]
CLWB [RSI+128]

; Full cache sync
WBINVD

; ══════════════════════════════════════════════════════════════════
; پایان - تعداد کل: 90 دستور
; همه ی دستورات صحیح و در محدوده مجاز هستند
; ══════════════════════════════════════════════════════════════════
