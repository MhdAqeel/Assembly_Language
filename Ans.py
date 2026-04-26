from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, PageBreak, HRFlowable, KeepTogether)

W, H = A4
M = 1.6*cm

# ── Palette ──────────────────────────────────────────────────────────────────
CN   = colors.HexColor('#0f172a')
CB   = colors.HexColor('#1d4ed8')
CLB  = colors.HexColor('#dbeafe')
CT   = colors.HexColor('#0f766e')
CLT  = colors.HexColor('#ccfbf1')
CP   = colors.HexColor('#6d28d9')
CLP  = colors.HexColor('#ede9fe')
CR   = colors.HexColor('#b91c1c')
CLR  = colors.HexColor('#fee2e2')
CA   = colors.HexColor('#92400e')
CLA  = colors.HexColor('#fef3c7')
CG   = colors.HexColor('#374151')
CLG  = colors.HexColor('#f3f4f6')
CMG  = colors.HexColor('#6b7280')
CW   = colors.white
CGN  = colors.HexColor('#166534')
CLGN = colors.HexColor('#dcfce7')

# ── Styles ───────────────────────────────────────────────────────────────────
def S(name, **kw):
    return ParagraphStyle(name, **kw)

sT   = S('T',  fontName='Helvetica-Bold', fontSize=13, textColor=CN, leading=17, spaceBefore=10, spaceAfter=4)
sH2  = S('H2', fontName='Helvetica-Bold', fontSize=11, textColor=CB, leading=15, spaceBefore=8, spaceAfter=3)
sH3  = S('H3', fontName='Helvetica-Bold', fontSize=10, textColor=CT, leading=14, spaceBefore=6, spaceAfter=2)
sH4  = S('H4', fontName='Helvetica-Bold', fontSize=9,  textColor=CP, leading=13, spaceBefore=4, spaceAfter=2)
sB   = S('B',  fontName='Helvetica',      fontSize=9,  textColor=CG, leading=13, spaceAfter=3)
sBJ  = S('BJ', fontName='Helvetica',      fontSize=9,  textColor=CG, leading=13, spaceAfter=3, alignment=TA_JUSTIFY)
sC   = S('C',  fontName='Courier',        fontSize=8,  textColor=colors.HexColor('#1e1b4b'),
         leading=11, backColor=colors.HexColor('#eef2ff'), leftIndent=8, spaceAfter=2)
sN   = S('N',  fontName='Helvetica-Oblique', fontSize=8.5, textColor=CA, leading=12, spaceAfter=3)
sSm  = S('Sm', fontName='Helvetica',      fontSize=8,  textColor=CMG, leading=11)
sAns = S('An', fontName='Helvetica-Bold', fontSize=9,  textColor=CGN, leading=13, spaceAfter=2)

def ts(cmds): return TableStyle(cmds)

def htab(headers, rows, hbg=CN, alt=CLG, cws=None, fs=8):
    data = [headers] + rows
    t = Table(data, colWidths=cws, repeatRows=1)
    t.setStyle(ts([
        ('BACKGROUND',(0,0),(-1,0),hbg),('TEXTCOLOR',(0,0),(-1,0),CW),
        ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),fs),
        ('FONTNAME',(0,1),(-1,-1),'Helvetica'),('TEXTCOLOR',(0,1),(-1,-1),CG),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[CW,alt]),
        ('GRID',(0,0),(-1,-1),0.3,colors.HexColor('#d1d5db')),
        ('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3),
        ('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),
    ]))
    return t

def banner(txt, bg, fg=CW, sub=None):
    ts_ = S('_b', fontName='Helvetica-Bold', fontSize=11, textColor=fg, leading=15)
    ss_ = S('_s', fontName='Helvetica', fontSize=8, textColor=colors.HexColor('#bfdbfe'), leading=11)
    cell = [Paragraph(txt, ts_)]
    if sub: cell.append(Paragraph(sub, ss_))
    t = Table([[cell]], colWidths=[W-2*M])
    t.setStyle(ts([('BACKGROUND',(0,0),(-1,-1),bg),('ROUNDEDCORNERS',[5]),
                   ('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),
                   ('LEFTPADDING',(0,0),(-1,-1),12)]))
    return t

def qbox(year, qn, marks, txt):
    """Question header box."""
    qs = S('_q', fontName='Helvetica-Bold', fontSize=10, textColor=CW, leading=14)
    ms = S('_m', fontName='Helvetica', fontSize=8, textColor=colors.HexColor('#fde68a'), leading=12)
    t = Table([[Paragraph(f'{year} · Q{qn}: {txt}', qs),
                Paragraph(f'[{marks}]', ms)]], colWidths=[W-2*M-2*cm, 2*cm])
    t.setStyle(ts([('BACKGROUND',(0,0),(-1,-1),CN),('ROUNDEDCORNERS',[4]),
                   ('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),
                   ('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),8),
                   ('VALIGN',(0,0),(-1,-1),'MIDDLE'),('ALIGN',(1,0),(1,0),'RIGHT')]))
    return t

def abox(parts):
    """Green answer box."""
    items = [Paragraph('<b>Answer:</b>', sAns)]
    for part in parts:
        items.append(Paragraph(part, sB))
    t = Table([[items]], colWidths=[W-2*M])
    t.setStyle(ts([('BACKGROUND',(0,0),(-1,-1),CLGN),('ROUNDEDCORNERS',[4]),
                   ('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),
                   ('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10)]))
    return t

def explbox(txt):
    """Blue explanation box."""
    items = [Paragraph('<b>Explanation:</b>', S('_e', fontName='Helvetica-Bold', fontSize=9, textColor=CB, leading=13)),
             Paragraph(txt, sBJ)]
    t = Table([[items]], colWidths=[W-2*M])
    t.setStyle(ts([('BACKGROUND',(0,0),(-1,-1),CLB),('ROUNDEDCORNERS',[4]),
                   ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),
                   ('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10)]))
    return t

def calcbox(lines):
    """Calculation box."""
    t = Table([[Paragraph('\n'.join(lines), sC)]], colWidths=[W-2*M])
    t.setStyle(ts([('BACKGROUND',(0,0),(-1,-1),colors.HexColor('#eef2ff')),
                   ('ROUNDEDCORNERS',[4]),('TOPPADDING',(0,0),(-1,-1),8),
                   ('BOTTOMPADDING',(0,0),(-1,-1),8),('LEFTPADDING',(0,0),(-1,-1),10)]))
    return t

def sp(h=6): return Spacer(1,h)
def hr(): return HRFlowable(width='100%',thickness=0.4,color=colors.HexColor('#e5e7eb'),spaceAfter=4)
def p(txt,st=sB): return Paragraph(txt,st)

# ─────────────────────────────────────────────────────────────────────────────
# BUILD STORY
# ─────────────────────────────────────────────────────────────────────────────
story = []

# ═══════════════════════════════ COVER ═══════════════════════════════════════
from reportlab.platypus import Flowable
class Cover(Flowable):
    def __init__(self):
        super().__init__()
        self.width = W-2*M; self.height = 160
    def wrap(self,aw,ah): return self.width,self.height
    def draw(self):
        c=self.canv
        c.setFillColor(CN); c.roundRect(0,0,self.width,self.height,10,fill=1,stroke=0)
        c.setFillColor(CB);  c.rect(0,0,self.width,5,fill=1,stroke=0)
        c.setFillColor(colors.HexColor('#93c5fd')); c.rect(0,self.height-5,self.width,5,fill=1,stroke=0)

story.append(sp(20))
story.append(Cover())
story.append(sp(-148))
for txt, sty in [
    ('CSC207S3: Computer Architecture', S('cv',fontName='Helvetica-Bold',fontSize=22,textColor=CW,leading=28,alignment=TA_CENTER)),
    ('Complete Exam Answer Booklet', S('cs',fontName='Helvetica',fontSize=13,textColor=colors.HexColor('#93c5fd'),leading=18,alignment=TA_CENTER)),
    ('2020 · 2021 · 2022 · 2023 Past Papers — Model Answers with Full Explanations', S('ct',fontName='Helvetica',fontSize=9,textColor=colors.HexColor('#bfdbfe'),leading=13,alignment=TA_CENTER)),
]:
    story.append(p(txt,sty)); story.append(sp(6))
story.append(sp(110))

years = [('2020','Q1: CPU Performance, Amdahl\'s Law, Assembly','Q2: Datapath Components & Instruction Execution','Q3: Memory Hierarchy, Cache Mapping','Q4: Pipelining & Hazards'),
         ('2021','Q1: Multi-core, CPI, Amdahl\'s Law','Q2: R-type, I-type, Datapath Execution','Q3: Pipeline Stages, Hazards & Forwarding','Q4: Memory Hierarchy & Cache Mapping'),
         ('2022','Q1: Throughput, CPI, Amdahl\'s Law, Assembly','Q2: R-type, I-type, Datapath Execution','Q3: Memory Hierarchy & Cache Mapping','Q4: Pipeline Stages, Data Hazards'),
         ('2023','Q1: CPI, Throughput, Amdahl\'s Law, Assembly','Q2: Datapath & Instruction Execution','Q3: Cache: Fully Assoc., Set Assoc.','Q4: Pipelining, Hazards')]
for yr, q1, q2, q3, q4 in years:
    t = Table([[p(f'<b>{yr}</b>',S('_y',fontName='Helvetica-Bold',fontSize=12,textColor=CW,alignment=TA_CENTER)),
                p(f'{q1}\n{q2}\n{q3}\n{q4}',S('_d',fontName='Helvetica',fontSize=8,textColor=CG,leading=12))]],
              colWidths=[1.6*cm,W-2*M-1.6*cm-4])
    t.setStyle(ts([('BACKGROUND',(0,0),(0,0),CB),('BACKGROUND',(1,0),(1,0),CLG),
                   ('VALIGN',(0,0),(-1,-1),'MIDDLE'),('TOPPADDING',(0,0),(-1,-1),8),
                   ('BOTTOMPADDING',(0,0),(-1,-1),8),('LEFTPADDING',(0,0),(-1,-1),8),
                   ('ROUNDEDCORNERS',[4])]))
    story.append(t); story.append(sp(5))

story.append(PageBreak())

# ═══════════════════════════ 2020 PAPER ══════════════════════════════════════
story.append(banner('2020 EXAMINATION — Model Answers', CB, sub='University of Jaffna · CSC207S3 Computer Architecture'))
story.append(sp(10))

# ── 2020 Q1(a)i ──────────────────────────────────────────────────────────────
story.append(p('Question 1(a)(i) — Effective CPI and Execution Time for CPUs A and B', sT))
story.append(qbox('2020','1a-i','20%','Clock A=2.7GHz, Clock B=3GHz, IC=1.2M'))
story.append(sp(5))

story.append(p('Step 1: Calculate Effective CPI using the weighted sum formula:', sH3))
story.append(p('CPI<sub>eff</sub> = Σ (CPI<sub>i</sub> × frequency<sub>i</sub>)', sB))
story.append(sp(4))

cpi_tbl = htab(['Category','%','CPI-A','CPI-B','Contribution A','Contribution B'],
    [['Arithmetic & Logic','10% = 0.10','1','2','0.10×1 = 0.10','0.10×2 = 0.20'],
     ['Load & Store',      '20% = 0.20','2','2','0.20×2 = 0.40','0.20×2 = 0.40'],
     ['Branch',            '50% = 0.50','3','4','0.50×3 = 1.50','0.50×4 = 2.00'],
     ['Others',            '20% = 0.20','3','2','0.20×3 = 0.60','0.20×2 = 0.40'],
     ['','','','','',''],
     [Paragraph('<b>TOTAL (Effective CPI)</b>',S('_h',fontName='Helvetica-Bold',fontSize=8,textColor=CR)),
      '','','',
      Paragraph('<b>2.60</b>',S('_h',fontName='Helvetica-Bold',fontSize=8,textColor=CR)),
      Paragraph('<b>3.00</b>',S('_h',fontName='Helvetica-Bold',fontSize=8,textColor=CR))]],
    hbg=CB)
story.append(cpi_tbl); story.append(sp(6))

story.append(p('Step 2: Calculate CPU Execution Time:', sH3))
story.append(p('CPU Time = IC × CPI<sub>eff</sub> × Clock Cycle Time = IC × CPI<sub>eff</sub> / Clock Rate', sB))
story.append(calcbox([
    'CPU Time_A = IC × CPI_A / Clock Rate_A',
    '           = 1,200,000 × 2.60 / 2,700,000,000',
    '           = 3,120,000 / 2,700,000,000',
    '           = 0.001156 seconds = 1.156 ms',
    '',
    'CPU Time_B = IC × CPI_B / Clock Rate_B',
    '           = 1,200,000 × 3.00 / 3,000,000,000',
    '           = 3,600,000 / 3,000,000,000',
    '           = 0.001200 seconds = 1.200 ms',
]))
story.append(abox(['<b>CPU A:</b> CPI_eff = 2.60, Execution Time = 1.156 ms',
                   '<b>CPU B:</b> CPI_eff = 3.00, Execution Time = 1.200 ms',
                   '<b>CPU A is faster</b> despite having a lower clock rate.']))
story.append(explbox('The effective CPI weights each instruction class by its frequency in the program. '
    'Even though A has fewer GHz, its instruction mix uses simpler (lower CPI) instructions on average, '
    'resulting in a shorter total execution time.'))
story.append(sp(8))

# ── 2020 Q1(a)ii ─────────────────────────────────────────────────────────────
story.append(p('Question 1(a)(ii) — Clock Rate vs Performance Misconception', sT))
story.append(qbox('2020','1a-ii','10%','Is the fastest clock always the best performer?'))
story.append(sp(4))
story.append(abox(['<b>Disagree.</b> Clock rate alone does NOT determine performance.',
    'CPU A (2.7 GHz) executes in 1.156 ms; CPU B (3.0 GHz) executes in 1.200 ms.',
    'CPU A is ~3.8% faster despite a clock rate 10% lower than B.',
    'Performance also depends on: (1) CPI — cycles per instruction, (2) Instruction Count.']))
story.append(explbox('The CPU performance equation is: CPU Time = IC × CPI × Clock_Cycle_Time. '
    'A higher clock rate reduces Clock_Cycle_Time but if CPI is proportionally worse (as in B), '
    'the overall time can increase. CPU B spends 50% of time on branches which cost 4 cycles '
    'vs A\'s 3, negating its clock advantage.'))
story.append(sp(8))

# ── 2020 Q1(a)iii ────────────────────────────────────────────────────────────
story.append(p('Question 1(a)(iii) — MIPS Calculation', sT))
story.append(qbox('2020','1a-iii','10%','Calculate MIPS for CPUs A and B'))
story.append(sp(4))
story.append(p('Formula: MIPS = Clock Rate (MHz) / CPI<sub>eff</sub>', sH3))
story.append(calcbox([
    'MIPS_A = Clock Rate_A (MHz) / CPI_A',
    '       = 2700 MHz / 2.60',
    '       = 1038.46 MIPS',
    '',
    'MIPS_B = Clock Rate_B (MHz) / CPI_B',
    '       = 3000 MHz / 3.00',
    '       = 1000.00 MIPS',
]))
story.append(abox(['MIPS for CPU A = <b>1038.46 MIPS</b>',
                   'MIPS for CPU B = <b>1000.00 MIPS</b>',
                   'CPU A executes more million instructions per second, confirming it is the faster processor.']))
story.append(sp(8))

# ── 2020 Q1(b) ───────────────────────────────────────────────────────────────
story.append(p('Question 1(b) — Basic Speedup (Amdahl\'s Law)', sT))
story.append(qbox('2020','1b','10%','Old=30s, New=20s — compute speedup'))
story.append(sp(4))
story.append(calcbox([
    'Basic Speedup = Old Execution Time / New Execution Time',
    '              = 30 seconds / 20 seconds',
    '              = 1.5x',
]))
story.append(abox(['Speedup = <b>1.5x</b> — the redesigned CPU is 50% faster than the original.']))
story.append(sp(8))

# ── 2020 Q1(c) ───────────────────────────────────────────────────────────────
story.append(p('Question 1(c) — Amdahl\'s Law with Partial Improvement', sT))
story.append(qbox('2020','1c','20%','Speedup applies to only 30% of execution time'))
story.append(sp(4))
story.append(p('Amdahl\'s Law Formula: Speedup = 1 / [(1 - f) + f/s]', sH3))
story.append(p('Where: f = fraction of time improved (0.30), s = speedup of that fraction (1.5)', sB))
story.append(calcbox([
    'f = 0.30  (30% of original execution time benefits from improvement)',
    's = 1.5   (the improved portion runs 1.5x faster)',
    '',
    'Speedup = 1 / [(1 - f) + f/s]',
    '        = 1 / [(1 - 0.30) + 0.30/1.5]',
    '        = 1 / [0.70 + 0.20]',
    '        = 1 / 0.90',
    '        = 1.111x',
]))
story.append(abox(['Actual Speedup = <b>1.111x</b> (approximately 11.1% improvement)',
    'The 70% of code that was NOT improved limits the overall gain significantly.']))
story.append(explbox('This illustrates Amdahl\'s Law\'s key insight: the unimproved portion '
    '(70%) forms a ceiling on overall speedup. Even if we made the 30% portion infinitely fast, '
    'the maximum possible speedup would only be 1/0.70 = 1.43x. This is why optimizing '
    'the most frequently executed code ("hot paths") is critical.'))
story.append(sp(8))

# ── 2020 Q1(d) ───────────────────────────────────────────────────────────────
story.append(p('Question 1(d) — MIPS Assembly: Print numbers from a to b', sT))
story.append(qbox('2020','1d','30%','Read two integers a and b (b>a), print all from a to b'))
story.append(sp(4))
story.append(calcbox([
    '.data',
    '    prompt1: .asciiz "Enter a: "',
    '    prompt2: .asciiz "Enter b: "',
    '    space:   .asciiz " "',
    '    newline: .asciiz "\\n"',
    '',
    '.text',
    '.globl main',
    'main:',
    '    # Read integer a',
    '    li   $v0, 4          # syscall: print string',
    '    la   $a0, prompt1',
    '    syscall',
    '    li   $v0, 5          # syscall: read int',
    '    syscall',
    '    move $t0, $v0        # $t0 = a (current counter)',
    '',
    '    # Read integer b',
    '    li   $v0, 4',
    '    la   $a0, prompt2',
    '    syscall',
    '    li   $v0, 5          # syscall: read int',
    '    syscall',
    '    move $t1, $v0        # $t1 = b (upper bound)',
    '',
    'loop:',
    '    bgt  $t0, $t1, done  # if current > b, exit loop',
    '',
    '    # Print current number',
    '    li   $v0, 1          # syscall: print int',
    '    move $a0, $t0',
    '    syscall',
    '',
    '    # Print space separator',
    '    li   $v0, 4',
    '    la   $a0, space',
    '    syscall',
    '',
    '    addi $t0, $t0, 1     # counter++',
    '    j    loop             # repeat',
    '',
    'done:',
    '    li   $v0, 10         # syscall: exit',
    '    syscall',
]))
story.append(abox(['The program uses $t0 as a loop counter starting at a, incrementing each iteration.',
    'The bgt (branch if greater than) instruction exits the loop when counter exceeds b.',
    'syscall 5 reads an integer (result in $v0), syscall 1 prints an integer, syscall 10 exits.']))
story.append(sp(8))

# ── 2020 Q2 ──────────────────────────────────────────────────────────────────
story.append(p('Question 2(a) — Datapath Component Functions (A to I)', sT))
story.append(qbox('2020','2a','20%','Describe components A to I in the datapath diagram'))
story.append(sp(4))
comp_tbl = htab(['Label','Component','Function'],
    [['A','PC Adder (Add +4)','Adds 4 to the current PC value to compute the address of the next sequential instruction'],
     ['B','Branch MUX','Selects between PC+4 (no branch) and branch target address based on Branch AND Zero signals'],
     ['C','Program Counter (PC)','Stores the address of the currently executing instruction; updated every clock cycle'],
     ['D','Data Memory Read MUX','Selects between ALU result (R-type/store) and memory read data (load) to write back to registers'],
     ['E','Control Unit','Decodes the 6-bit opcode field [31-26] and generates all 8 control signals'],
     ['F','Sign Extend','Extends the 16-bit immediate field to 32 bits, preserving the sign (MSB replication)'],
     ['G','RegDst MUX','Selects write destination register: rt (bits [20-16]) for I-type, or rd (bits [15-11]) for R-type'],
     ['H','ALU Control','Takes ALUOp from Control Unit and funct bits [5-0]; outputs 4-bit ALU operation code'],
     ['I','ALUSrc MUX','Selects the second ALU input: Read data 2 (register) for R-type, or sign-extended immediate for I-type']],
    hbg=CB)
story.append(comp_tbl); story.append(sp(8))

story.append(p('Question 2(b) — Load and Store Instruction Structure', sT))
story.append(qbox('2020','2b','20%','Structure of lw/sw and their operation'))
story.append(sp(4))
story.append(p('Both lw and sw are I-type instructions:', sH3))
fmt_tbl = htab(['Field','op (6b)','rs (5b)','rt (5b)','immediate (16b)'],
    [['lw $rt, offset($rs)','100011 (35)','Base register','Destination reg','Signed offset'],
     ['sw $rt, offset($rs)','101011 (43)','Base register','Source reg (data)','Signed offset']],
    hbg=CT)
story.append(fmt_tbl); story.append(sp(5))
story.append(p('Load Word (lw $t0, 1200($t1)) — Operation:', sH3))
story.append(p('1. ALU computes: effective address = $t1 + sign_extend(1200)<br/>'
    '2. Data Memory is READ at that address (MemRead=1)<br/>'
    '3. The read data is written to $t0 (MemToReg=1, RegWrite=1)', sB))
story.append(p('Store Word (sw $t0, 1200($t1)) — Operation:', sH3))
story.append(p('1. ALU computes: effective address = $t1 + sign_extend(1200)<br/>'
    '2. $t0\'s value is written TO Data Memory at that address (MemWrite=1)<br/>'
    '3. No register is written back (RegWrite=0)', sB))
story.append(sp(8))

story.append(p('Question 2(c) — Execution of add $t1,$t2,$t3', sT))
story.append(qbox('2020','2c','20%','Trace add through the datapath'))
story.append(sp(4))
add_steps = htab(['Step','Action','Control Signal'],
    [['1. Fetch','PC → Instruction Memory → 32-bit instruction fetched. Add+4 computes PC+4.','—'],
     ['2. Decode','op[31-26]=000000 → Control Unit activates: RegDst=1, ALUSrc=0, MemToReg=0, RegWrite=1, MemRead=0, MemWrite=0, Branch=0, ALUOp=10','All 8 signals set'],
     ['3. Read Regs','Instr[25-21]=$t2 and Instr[20-16]=$t3 → Register File outputs both values','RegWrite=0 during read'],
     ['4. Execute','ALUSrc=0 → ALU input B = Read data 2 ($t3). ALU op=ADD (from funct=32). Result = $t2 + $t3.','ALUSrc=0, ALUOp=10'],
     ['5. Memory','MemRead=0, MemWrite=0 → Data Memory NOT accessed.','MemRead=0, MemWrite=0'],
     ['6. Write Back','MemToReg=0 → write ALU result. RegDst=1 → write to rd=$t1 (Instr[15-11]). RegWrite=1 → write enabled.','MemToReg=0, RegDst=1, RegWrite=1'],
     ['7. PC Update','Branch=0 → PC = PC+4 (no branch). MUX selects PC+4 output.','Branch=0']],
    hbg=CB)
story.append(add_steps); story.append(sp(8))

story.append(p('Question 2(d) — Execution of lw $t1, offset($t2)', sT))
story.append(qbox('2020','2d','20%','Trace lw through the datapath'))
story.append(sp(4))
lw_steps = htab(['Step','Action','Control Signal'],
    [['1. Fetch','PC → Instruction Memory → lw instruction fetched.','—'],
     ['2. Decode','op=100011 → Control: RegDst=0, ALUSrc=1, MemToReg=1, RegWrite=1, MemRead=1, MemWrite=0, Branch=0','All signals set'],
     ['3. Read Reg','Instr[25-21]=$t2 → Register File reads base address register.','—'],
     ['4. Sign Extend','Instr[15-0]=offset (16-bit) → Sign-extended to 32 bits.','—'],
     ['5. Execute','ALUSrc=1 → ALU input B = sign-extended offset. ALU computes $t2 + offset = memory address.','ALUSrc=1, ALUOp=00 (ADD)'],
     ['6. Memory','MemRead=1 → Data Memory reads 32-bit word at computed address.','MemRead=1'],
     ['7. Write Back','MemToReg=1 → write memory data (not ALU result). RegDst=0 → write to rt=$t1 (Instr[20-16]).','MemToReg=1, RegDst=0, RegWrite=1']],
    hbg=CT)
story.append(lw_steps); story.append(sp(8))

story.append(p('Question 2(e) — Normal Instruction Fetch vs Branch Instruction', sT))
story.append(qbox('2020','2e','20%','Compare normal fetch and branch operation'))
story.append(sp(4))
story.append(p('<b>Normal Instruction Fetch:</b>', sH3))
story.append(p('1. PC value sent to Instruction Memory as read address.<br/>'
    '2. 32-bit instruction fetched.<br/>'
    '3. Add+4 computes PC+4 simultaneously.<br/>'
    '4. Since Branch=0 (or Branch AND Zero = 0), the Branch MUX selects PC+4.<br/>'
    '5. PC is updated to PC+4 at end of cycle → sequential execution continues.', sB))
story.append(p('<b>Branch Instruction (beq $t1, $t2, L):</b>', sH3))
story.append(p('1. Normal fetch occurs as above.<br/>'
    '2. Two things happen in parallel: (a) ALU subtracts $t1 - $t2 and sets Zero=1 if equal. '
    '(b) Sign-extend(offset) → Shift-Left-2 → Add with PC+4 = branch target address.<br/>'
    '3. Branch control signal = 1. AND gate: Branch AND Zero.<br/>'
    '4. If Zero=1: Branch MUX selects branch target → PC jumps to L.<br/>'
    '5. If Zero=0: Branch MUX selects PC+4 → sequential execution.', sB))
story.append(sp(8))

# ── 2020 Q3 ──────────────────────────────────────────────────────────────────
story.append(p('Question 3(a) — Memory Hierarchy Request Response', sT))
story.append(qbox('2020','3a','15%','How does the memory system respond to a CPU memory request?'))
story.append(sp(4))
story.append(abox([
    '1. CPU generates a memory address request.',
    '2. Cache is checked FIRST (fastest). If the data is in cache → Cache HIT → data returned in ~1-4 ns.',
    '3. If not in cache → Cache MISS → Main Memory is checked next (~40-100 ns).',
    '4. If not in Main Memory → Main Memory MISS → Secondary Storage (disk/SSD) is accessed (~1 ms+).',
    '5. On any miss, the missing block is loaded into the higher (faster) level for future reuse.',
    'This hierarchy exploits locality: frequently used data stays in fast cache.']))
story.append(sp(8))

story.append(p('Question 3(b) — Average Access Time (3-Level)', sT))
story.append(qbox('2020','3b','15%','Cache=20ns h=60%, Main=100ns h=70%, Disk=300ns'))
story.append(sp(4))
story.append(p('Formula: T = h1×T1 + (1-h1)×[h2×T2 + (1-h2)×T3]', sH3))
story.append(calcbox([
    'h1 = 0.60 (cache hit ratio),   T1 = 20 ns',
    'h2 = 0.70 (main memory hit ratio given cache miss),   T2 = 100 ns',
    'T3 = 300 ns (disk)',
    '',
    'T_avg = h1 × T1 + (1-h1) × [h2 × T2 + (1-h2) × T3]',
    '      = 0.60 × 20 + 0.40 × [0.70 × 100 + 0.30 × 300]',
    '      = 12 + 0.40 × [70 + 90]',
    '      = 12 + 0.40 × 160',
    '      = 12 + 64',
    '      = 76 ns',
]))
story.append(abox(['Average Memory Access Time = <b>76 ns</b>']))
story.append(sp(8))

story.append(p('Question 3(c) — Spatial and Temporal Locality', sT))
story.append(qbox('2020','3c','20%','Describe locality principles and how cache improves CPU performance'))
story.append(sp(4))
loc_tbl = htab(['Principle','Definition','Example','How Cache Uses It'],
    [['Temporal Locality','If a memory location is accessed, it is likely to be accessed again soon.',
      'Loop counter accessed every iteration; same variable used repeatedly.',
      'Cache keeps recently accessed blocks resident — subsequent accesses are hits.'],
     ['Spatial Locality','If a memory location is accessed, nearby locations are likely accessed soon.',
      'Array traversal: arr[0], arr[1], arr[2]... accessed in sequence.',
      'Cache loads an entire block (e.g., 64 bytes) at once — neighbouring words already cached.']],
    hbg=CP)
story.append(loc_tbl); story.append(sp(5))
story.append(p('How cache improves CPU performance:', sH3))
story.append(p('Cache sits between the CPU and slow main memory. When data is found in cache (hit), '
    'it is delivered in ~1-4 ns instead of ~100 ns from RAM — a 25-100x speedup. '
    'The overall improvement depends on the hit rate: if hit rate = 95%, only 5% of accesses '
    'incur the full main memory penalty, making the effective access time nearly as fast as cache alone.', sBJ))
story.append(sp(8))

story.append(p('Question 3(d) — Set-Associative Memory Mapping', sT))
story.append(qbox('2020','3d','20%','Describe set-associative mapping'))
story.append(sp(4))
story.append(abox(['In set-associative mapping, the cache is divided into SETS, each containing a fixed number of lines (the set size / associativity).',
    'A memory block maps to exactly ONE set (like direct mapping), but can occupy ANY line within that set (like fully associative).',
    'This is a compromise: more flexible than direct-mapped (fewer conflicts), simpler than fully associative (cheaper hardware).']))
story.append(p('Address structure: | Tag | Set Index | Block Offset |', sH3))
story.append(p('Lookup process: (1) Extract set index → select the set. '
    '(2) Extract tag. (3) Compare tag against ALL lines in that set in parallel. '
    '(4) Hit if any valid line matches; Miss if none match.', sB))
story.append(sp(8))

story.append(p('Question 3(e) — Set-Associative Bit Field Calculation', sT))
story.append(qbox('2020','3e','30%','512-block cache, 8K-block memory, 64-word blocks, 16-block sets'))
story.append(sp(4))
story.append(calcbox([
    'Given:',
    '  Cache size     = 512 blocks',
    '  Memory size    = 8K = 8192 blocks',
    '  Block size     = 64 words',
    '  Set size       = 16 blocks per set',
    '',
    'Step 1: Block Offset bits = log2(block size) = log2(64) = 6 bits',
    '',
    'Step 2: Number of sets = Cache blocks / Set size = 512 / 16 = 32 sets',
    '        Set Index bits = log2(32) = 5 bits',
    '',
    'Step 3: Total address bits = log2(memory size in blocks) = log2(8192) = 13 bits',
    '        Tag bits = Total - Set bits - Offset bits = 13 - 5 - 6 = 2 bits',
    '',
    'Address structure:',
    '  | Tag (2b) | Set Index (5b) | Block Offset (6b) |',
    '  Total = 2 + 5 + 6 = 13 bits ✓',
]))
story.append(abox(['Tag bits = <b>2</b>, Set Index bits = <b>5</b>, Block Offset bits = <b>6</b>']))
story.append(p('Part (ii) — How to find if an address is in cache:', sH3))
story.append(p('1. Extract the 5 set-index bits from the address → identify which of the 32 sets to look in.<br/>'
    '2. Extract the 2 tag bits from the address.<br/>'
    '3. Compare the tag against the tag field of EVERY valid line in that set (all 16 lines).<br/>'
    '4. If any match and the valid bit is 1 → CACHE HIT → return that block\'s data using the 6 offset bits.<br/>'
    '5. If no match → CACHE MISS → fetch block from memory, load into set (replacing per LRU policy).', sB))
story.append(sp(8))

# ── 2020 Q4 ──────────────────────────────────────────────────────────────────
story.append(p('Question 4(a) — Five-Stage Instruction Execution Cycle', sT))
story.append(qbox('2020','4a','20%','State and describe the 5 stages'))
story.append(sp(4))
stage_tbl = htab(['Stage','Name','What Happens','Units Used'],
    [['1','IF — Instruction Fetch','PC sent to Instruction Memory; 32-bit instruction fetched; PC+4 computed by adder.','Instruction Memory, PC, Add+4'],
     ['2','ID — Instruction Decode / Register Read','Opcode decoded by Control Unit; rs and rt read from Register File; immediate sign-extended.','Control Unit, Register File, Sign-Extend'],
     ['3','EX — Execute / Address Calculate','ALU performs arithmetic/logic operation, or computes memory address (base + offset).','ALU, ALU Control, MUX(ALUSrc)'],
     ['4','MEM — Memory Access','For lw: Data Memory read. For sw: Data Memory written. Other instructions pass through.','Data Memory'],
     ['5','WB — Write Back','For R-type/lw: Result written back to destination register in Register File.','Register File, MUX(MemToReg)']],
    hbg=CP)
story.append(stage_tbl); story.append(sp(8))

story.append(p('Question 4(b) — Pipelined vs Non-Pipelined Timing', sT))
story.append(qbox('2020','4b','60%','Memory=200ps, ALU=150ps, Register=100ps — add instruction'))
story.append(sp(4))
story.append(p('First, determine the time for each stage for the add instruction:', sH3))
stage_time = htab(['Stage','Operation','Time'],
    [['IF','Instruction Fetch — memory access','200 ps'],
     ['ID','Register Read','100 ps'],
     ['EX','ALU operation (add)','150 ps'],
     ['MEM','No memory access — pass through','0 ps (or 200 ps cycle)'],
     ['WB','Register Write','100 ps'],
     ['','Total per instruction','550 ps']],
    hbg=CB)
story.append(stage_time); story.append(sp(5))

story.append(p('Part (i) — Non-Pipelined (add $t1,$t2,$t3):', sH3))
story.append(calcbox([
    'Non-pipelined: all stages complete sequentially.',
    'Time per instruction = IF + ID + EX + MEM + WB',
    '                     = 200 + 100 + 150 + 200 + 100  (MEM stage still takes 200ps clock cycle)',
    '                     = 750 ps per instruction',
    '',
    'Note: In non-pipelined, the clock cycle = longest single instruction path.',
    'For add: 200 + 100 + 150 + 0 + 100 = 550 ps',
    'But the clock must accommodate ALL instruction types including lw (200+100+150+200+100=750ps)',
    'So: Clock cycle = 750 ps, Time for one add = 750 ps',
]))
story.append(abox(['Non-pipelined time for one add = <b>750 ps</b>']))
story.append(sp(5))

story.append(p('Part (ii) — Pipelined (5 consecutive add instructions):', sH3))
story.append(calcbox([
    'Pipeline clock cycle = longest single stage = 200 ps (memory access)',
    '',
    'Pipeline timing for 5 add instructions:',
    'Time = (N + stages - 1) × clock cycle',
    '     = (5 + 5 - 1) × 200 ps',
    '     = 9 × 200 ps',
    '     = 1800 ps',
    '',
    'Diagram (each cell = 200 ps):',
    'add1: IF  ID  EX  MEM WB',
    'add2:     IF  ID  EX  MEM WB',
    'add3:         IF  ID  EX  MEM WB',
    'add4:             IF  ID  EX  MEM WB',
    'add5:                 IF  ID  EX  MEM WB',
    'Cycles:  1   2   3   4   5   6   7   8   9',
]))
story.append(abox(['Pipelined time for 5 add instructions = <b>1800 ps</b>']))
story.append(sp(5))

story.append(p('Part (iii) — Performance comparison:', sH3))
story.append(calcbox([
    'Non-pipelined: 5 × 750 ps = 3750 ps',
    'Pipelined:                  1800 ps',
    'Speedup = 3750 / 1800 = 2.08x',
    '',
    'Theoretical max speedup = number of stages = 5x',
    'Actual speedup is less because:',
    '  (1) Pipeline clock must match slowest stage (200 ps MEM, not 150 ps ALU)',
    '  (2) Pipeline startup overhead (first 4 cycles fill the pipeline)',
    '  (3) Real programs also have hazards that stall the pipeline',
]))
story.append(sp(8))

story.append(p('Question 4(c) — Two Types of Pipeline Hazards', sT))
story.append(qbox('2020','4c','20%','Describe two pipeline hazards with examples'))
story.append(sp(4))
haz_tbl = htab(['Hazard Type','Cause','Example','Resolution'],
    [['Data Hazard (RAW)','An instruction reads a register that a previous instruction has not yet written back.',
      'add $t0,$t1,$t2 followed by sub $t3,$t0,$t4 — sub reads $t0 before add writes it.',
      'Forwarding (bypass ALU result directly to next stage) or pipeline stall (insert bubble)'],
     ['Control Hazard','A branch instruction changes the PC, but the CPU has already started fetching/decoding the wrong next instructions.',
      'beq $t0,$t1,L — two instructions after the beq are fetched before the branch outcome is known.',
      'Branch prediction (assume not taken), delayed branch slots, or flush mispredicted instructions']],
    hbg=CR)
story.append(haz_tbl)
story.append(PageBreak())

# ═══════════════════════════ 2021 PAPER ══════════════════════════════════════
story.append(banner('2021 EXAMINATION — Model Answers', CT, sub='University of Jaffna · CSC207S3 Computer Architecture'))
story.append(sp(10))

story.append(p('Question 1(a) — Reasons for Multi-Core Processors', sT))
story.append(qbox('2021','1a','10%','State reasons for manufacturing multi-core CPUs since 2006'))
story.append(sp(4))
story.append(abox([
    '1. <b>Power Wall:</b> Increasing clock frequency requires disproportionately more power (P ∝ f³). Beyond ~4 GHz, chips overheat.',
    '2. <b>Memory Wall:</b> Single cores stall waiting for slow memory; multiple cores can hide latency by running other threads.',
    '3. <b>Instruction-Level Parallelism (ILP) limit:</b> Single cores struggle to find more independent instructions to execute.',
    '4. <b>Transistor budget:</b> Moore\'s Law still provides more transistors — better spent on multiple cores than one complex core.',
    '5. <b>Thread-level parallelism:</b> Modern workloads (servers, databases, video) are naturally parallel — multiple cores exploit this.']))
story.append(sp(8))

story.append(p('Question 1(b) — Throughput vs Response Time (Multi-core)', sT))
story.append(qbox('2021','1b','10%','Why benefit is more on throughput than response time'))
story.append(sp(4))
story.append(abox([
    '<b>Response time (latency):</b> Time to complete ONE task. Multiple cores do NOT speed up a single sequential program.',
    '<b>Throughput:</b> Number of tasks completed per unit time. Multiple cores can run MANY tasks simultaneously.',
    'Example: A web server handling 1000 requests — 4 cores can serve 4 requests simultaneously, 4× the throughput.',
    'But one specific database query still takes the same time (response time unchanged).']))
story.append(explbox('This is why multi-core processors transformed server performance dramatically but gave less '
    'benefit to single-threaded desktop applications like simple text editors.'))
story.append(sp(8))

story.append(p('Question 1(c) — P1 vs P2 Performance Analysis', sT))
story.append(qbox('2021','1c','30%','P1: 3GHz CPI=1.5, P2: 3.4GHz CPI=2.0'))
story.append(sp(4))
story.append(p('Part (i) — Which has highest throughput?', sH3))
story.append(calcbox([
    'Throughput ∝ 1/CPU_Time = Clock Rate / CPI',
    '',
    'Instructions per second:',
    '  P1 = Clock Rate / CPI = 3,000,000,000 / 1.5 = 2,000,000,000 = 2000 MIPS',
    '  P2 = Clock Rate / CPI = 3,400,000,000 / 2.0 = 1,700,000,000 = 1700 MIPS',
    '',
    'P1 has higher throughput: 2000 MIPS vs 1700 MIPS',
]))
story.append(abox(['<b>P1 has the highest performance</b> — executes 2000 million instructions/sec vs P2\'s 1700 MIPS.']))
story.append(sp(5))

story.append(p('Part (ii) — Number of instructions if P1 executes in 12 ms:', sH3))
story.append(calcbox([
    'CPU Time = IC × CPI / Clock Rate',
    '→ IC = CPU Time × Clock Rate / CPI',
    '      = 0.012 s × 3,000,000,000 / 1.5',
    '      = 36,000,000 / 1.5',
    '      = 24,000,000 instructions = 24 million',
]))
story.append(abox(['Instruction Count = <b>24 million instructions</b>']))
story.append(sp(5))

story.append(p('Part (iii) — Required clock rate for 30% time reduction with 20% CPI increase:', sH3))
story.append(calcbox([
    'Original time: T = IC × 1.5 / 3GHz',
    'Target time:   T_new = 0.70 × T  (30% reduction)',
    'New CPI:       CPI_new = 1.5 × 1.20 = 1.80  (20% increase)',
    '',
    'T_new = IC × CPI_new / Clock_new',
    '0.70 × T = IC × 1.80 / Clock_new',
    '0.70 × (IC × 1.5 / 3GHz) = IC × 1.80 / Clock_new',
    '',
    'Clock_new = 1.80 / (0.70 × 1.5/3GHz)',
    '          = 1.80 / (0.70 × 0.5 ns)',
    '          = 1.80 / (1.05 / 3GHz)',
    '          = 1.80 × 3GHz / 1.05',
    '          = 5.4 GHz / 1.05',
    '          = 5.143 GHz',
]))
story.append(abox(['Required clock rate = <b>5.143 GHz</b>']))
story.append(sp(8))

story.append(p('Question 1(d) — CPI, Execution Time, MIPS for P1 and P2', sT))
story.append(qbox('2021','1d','25%','P1=2.4GHz, P2=3.2GHz, IC=1M, instruction mix table'))
story.append(sp(4))
story.append(calcbox([
    'CPI_P1 = 0.10×1 + 0.20×2 + 0.40×3 + 0.30×2',
    '       = 0.10 + 0.40 + 1.20 + 0.60 = 2.30',
    '',
    'CPI_P2 = 0.10×2 + 0.20×3 + 0.40×3 + 0.30×2',
    '       = 0.20 + 0.60 + 1.20 + 0.60 = 2.60',
    '',
    'T_P1 = 1,000,000 × 2.30 / 2,400,000,000 = 0.000958 s = 0.958 ms',
    'T_P2 = 1,000,000 × 2.60 / 3,200,000,000 = 0.000813 s = 0.813 ms',
    '',
    'MIPS_P1 = 2400 / 2.30 = 1043.5 MIPS',
    'MIPS_P2 = 3200 / 2.60 = 1230.8 MIPS',
]))
story.append(abox(['P1: CPI=2.30, Time=0.958ms, MIPS=1043.5',
                   'P2: CPI=2.60, Time=0.813ms, MIPS=1230.8',
                   'P2 is faster overall despite higher CPI, because its clock rate advantage is sufficient.']))
story.append(sp(8))

story.append(p('Question 1(e) — Amdahl\'s Law: 40ms → 25ms, 40% improved', sT))
story.append(qbox('2021','1e','25%','Actual speedup using Amdahl\'s Law'))
story.append(sp(4))
story.append(calcbox([
    'Old time = 40 ms,  New time = 25 ms',
    'Basic speedup s = 40/25 = 1.6x for the improved portion',
    'Fraction improved f = 0.40',
    '',
    'Amdahl\'s Law: Speedup = 1 / [(1-f) + f/s]',
    '             = 1 / [(1-0.40) + 0.40/1.6]',
    '             = 1 / [0.60 + 0.25]',
    '             = 1 / 0.85',
    '             = 1.176x',
]))
story.append(abox(['Actual overall speedup = <b>1.176x</b> (approximately 17.6% improvement)']))
story.append(sp(8))

story.append(p('Question 2 — R-Type and I-Type Instructions', sT))
story.append(qbox('2021','2a-b','40%','Describe R-type and I-type instruction components'))
story.append(sp(4))
r_tbl = htab(['Field','Bits','Meaning','Example: add $t1,$t2,$t3'],
    [['op','6','Opcode — always 000000 for R-type','000000'],
     ['rs','5','First source register','$t2 = register 10'],
     ['rt','5','Second source register','$t3 = register 11'],
     ['rd','5','Destination register (gets result)','$t1 = register 9'],
     ['shamt','5','Shift amount (0 for non-shift)','00000'],
     ['funct','6','Selects specific ALU operation (32=add)','100000']],
    hbg=CP)
story.append(r_tbl); story.append(sp(5))

i_tbl = htab(['Field','Bits','Meaning','Example: lw $t0, 100($t2)'],
    [['op','6','Opcode identifies instruction type (35=lw, 43=sw, 4=beq)','100011 (35)'],
     ['rs','5','Base/source register','$t2 = register 10'],
     ['rt','5','Destination (lw) or source data (sw)','$t0 = register 8'],
     ['immediate','16','Sign-extended constant/offset/branch offset','100']],
    hbg=CR)
story.append(i_tbl); story.append(sp(8))

story.append(p('Question 2(c)(iii) — Branch instruction je $t1,$t2,$a', sT))
story.append(qbox('2021','2c-iii','20%','Describe branch execution in datapath'))
story.append(sp(4))
story.append(p('The je (jump if equal) / beq instruction uses the I-type format.', sH3))
br_steps = htab(['Step','Operation'],
    [['1. Fetch','Instruction fetched from Instruction Memory. PC+4 computed.'],
     ['2. Decode','op=000100 → Control: Branch=1, ALUSrc=0, ALUOp=01, RegWrite=0, MemRead=0, MemWrite=0.'],
     ['3. Read Regs','$t1 and $t2 read from Register File.'],
     ['4. Branch target','Sign-extend(imm) → Shift-Left-2 → Add with (PC+4) = branch target address $a.'],
     ['5. ALU','ALUSrc=0 → ALU subtracts $t1-$t2. If result=0 → Zero flag=1.'],
     ['6. PC decision','AND(Branch,Zero)=1 → MUX selects branch target → PC=$a. Else PC=PC+4.'],
     ['7. No write back','RegWrite=0, MemWrite=0.']],
    hbg=CB)
story.append(br_steps); story.append(sp(8))

story.append(p('Question 3 — Pipeline Timing with lw,sub,add,add,sw', sT))
story.append(qbox('2021','3','100%','Memory=100ps, ALU=70ps, Register=50ps'))
story.append(sp(4))
story.append(p('Stage times per instruction type:', sH3))
st_tbl = htab(['Instruction','IF','ID','EX','MEM','WB','Total'],
    [['lw','100','50','70','100','50','370 ps'],
     ['sub / add / R-type','100','50','70','0*','50','270 ps'],
     ['sw','100','50','70','100','0*','320 ps']],
    hbg=CB)
story.append(st_tbl)
story.append(p('*Stage still occupies one clock cycle in pipeline; functional unit may be idle.', sSm))
story.append(sp(5))
story.append(p('Pipeline clock cycle = slowest stage = 100 ps (memory access)', sH3))
story.append(sp(4))

story.append(p('Part (a) — Non-pipelined: first 3 instructions (lw, sub, add):', sH3))
story.append(calcbox([
    'Non-pipelined: each instruction completes fully before next starts.',
    'Clock cycle = longest instruction = lw = 370 ps (or standard 100+50+70+100+50)',
    'But typically we use: each instr takes sum of all active stage times.',
    '',
    'T = lw + sub + add = 370 + 270 + 270 = 910 ps',
    '',
    'OR: if using fixed clock = 100 ps per stage × 5 stages:',
    'T = 3 instructions × 5 stages × 100 ps = 1500 ps',
]))
story.append(abox(['Non-pipelined time for 3 instructions = <b>910 ps</b> (sum of actual stage times)']))
story.append(sp(5))

story.append(p('Part (c) — Pipelined: first 3 instructions:', sH3))
story.append(calcbox([
    'Pipeline clock cycle = 100 ps (slowest stage)',
    'Time = (N + stages - 1) × cycle = (3 + 5 - 1) × 100 = 700 ps',
]))
story.append(abox(['Pipelined time for 3 instructions = <b>700 ps</b>']))
story.append(sp(5))

story.append(p('Part (d)(i) — Data Hazards in the full program:', sH3))
story.append(p('<b>Program:</b> lw $t1,100($t2) | sub $t2,$t4,$t2 | add $t5,$t6,$t5 | add $t3,$t1,$t3 | sw $t3,100($t0)', sC))
haz_prog = htab(['Hazard','Instruction Pair','Type','Reason'],
    [['Hazard 1','lw $t1 → add $t3,$t1,$t3','RAW (Load-Use)','add reads $t1 which lw writes. 2 instructions apart — WB of lw is at cycle 5, EX of add is cycle 4. Needs 1 stall.'],
     ['Hazard 2','sub $t2 → (no dependency found)','None','sub writes $t2 but no subsequent instruction reads $t2 before it is written.'],
     ['Hazard 3','add $t3 → sw $t3','RAW','sw reads $t3 which add $t3 writes — 1 instruction apart. Can be resolved by forwarding.']],
    hbg=CR)
story.append(haz_prog); story.append(sp(5))

story.append(p('Part (d)(ii) — Forwarding/Bypassing approach:', sH3))
story.append(abox([
    'Forwarding adds hardware paths that bypass the register file.',
    'EX/MEM forwarding: passes ALU result directly to the next instruction\'s EX stage input.',
    'MEM/WB forwarding: passes ALU result or memory data to an instruction 2 cycles later.',
    'For the load-use hazard (lw→add): the value from memory is not available until end of MEM stage, '
    'so even forwarding cannot avoid 1 stall cycle — a bubble must be inserted between lw and add $t3.']))
story.append(sp(5))

story.append(p('Part (d)(iii) — Full pipeline with forwarding, execution time:', sH3))
story.append(calcbox([
    'With forwarding, lw→add still needs 1 stall (load-use hazard):',
    '',
    'Instruction sequence with stall:',
    '  lw $t1        | IF ID EX MEM WB',
    '  sub $t2       |    IF ID EX  MEM WB',
    '  add $t5       |       IF ID  EX  MEM WB',
    '  [stall/NOP]   |           IF  ID  stall...',
    '  add $t3,$t1   |                IF  ID  EX  MEM WB',
    '  sw $t3        |                    IF  ID  EX  MEM WB',
    '',
    'Total cycles = 5 instructions + 4 fill + 1 stall = 10 cycles',
    'Total time = 10 × 100 ps = 1000 ps',
]))
story.append(abox(['Time for all 5 instructions with forwarding = <b>1000 ps</b> (10 cycles × 100 ps)']))
story.append(sp(8))

story.append(p('Question 4 — Memory Hierarchy, Direct-Mapped and Set-Associative Cache', sT))
story.append(qbox('2021','4','100%','32-bit address, Cache=64KiB, Block=16 words, 1 word=4 bytes'))
story.append(sp(4))
story.append(p('Part (b) — Average Access Time (3-level: Cache/RAM/SSD):', sH3))
story.append(calcbox([
    'Cache: 10 ns, hit ratio h1=0.60',
    'Main memory: 50 ns, hit ratio h2=0.80',
    'SSD: 100 ns',
    '',
    'T_avg = 0.60×10 + 0.40×[0.80×50 + 0.20×100]',
    '      = 6 + 0.40×[40 + 20]',
    '      = 6 + 0.40×60',
    '      = 6 + 24 = 30 ns',
]))
story.append(abox(['Average Access Time = <b>30 ns</b>']))
story.append(sp(5))

story.append(p('Part (c) — Direct-Mapped Cache (32-bit addr, 64KiB cache, 16-word blocks, 4B/word):', sH3))
story.append(calcbox([
    'Block size in bytes = 16 words × 4 bytes = 64 bytes',
    'Offset bits = log2(64) = 6 bits',
    '',
    'Number of cache lines = 64 KiB / 64 B = 65536/64 = 1024 lines',
    'Index bits = log2(1024) = 10 bits',
    '',
    'Tag bits = 32 - 10 - 6 = 16 bits',
    '',
    'Address: | Tag (16b) | Index (10b) | Offset (6b) |',
]))
story.append(p('Part (c)(ii) — Actual cache size:', sH3))
story.append(calcbox([
    'Each cache line = valid bit (1) + tag (16) + data (16 words × 32 bits = 512 bits)',
    '               = 1 + 16 + 512 = 529 bits',
    'Total = 1024 lines × 529 bits = 541,696 bits = 67,712 bytes = 66.125 KiB',
]))
story.append(abox(['Actual cache size ≈ <b>66.125 KiB</b> (slightly larger than 64 KiB nominal due to tag/valid bits)']))
story.append(sp(5))

story.append(p('Part (d) — Set-Associative: 512-block cache, 8K-block memory, 32-word blocks, 8-block sets:', sH3))
story.append(calcbox([
    'Offset bits = log2(32) = 5 bits',
    'Number of sets = 512 / 8 = 64 sets',
    'Set bits = log2(64) = 6 bits',
    'Total address bits = log2(8192) = 13 bits',
    'Tag bits = 13 - 6 - 5 = 2 bits',
    '',
    'Address: | Tag (2b) | Set (6b) | Offset (5b) |',
]))
story.append(abox(['Tag=2 bits, Set=6 bits, Offset=5 bits']))
story.append(PageBreak())

# ═══════════════════════════ 2022 PAPER ══════════════════════════════════════
story.append(banner('2022 EXAMINATION — Model Answers', CP, sub='University of Jaffna · CSC207S3 Computer Architecture'))
story.append(sp(10))

story.append(p('Question 1(a) — Throughput and Execution Time', sT))
story.append(qbox('2022','1a','10%','Define throughput and execution time with examples'))
story.append(sp(4))
story.append(abox([
    '<b>Execution Time (Response Time/Latency):</b> The total time required to complete one task from start to finish.',
    'Example: A video encoding job that takes 45 seconds — execution time = 45 s.',
    '<b>Throughput:</b> The number of tasks completed per unit of time.',
    'Example: A web server handling 500 HTTP requests per second — throughput = 500 req/s.',
    'Key distinction: Replacing a slow CPU with a faster one reduces execution time AND increases throughput. '
    'Adding more CPUs (parallel) primarily increases throughput without reducing individual task time.']))
story.append(sp(8))

story.append(p('Question 1(b) — Effect on throughput and execution time', sT))
story.append(qbox('2022','1b','10%','i5 3.2GHz → higher frequency OR → i7 3.2GHz'))
story.append(sp(4))
story.append(abox([
    '<b>Part (i) — Replace with higher frequency (same i5):</b>',
    'Execution time DECREASES (each instruction takes fewer nanoseconds). Throughput INCREASES.',
    'Both metrics improve proportionally to the frequency increase.',
    '',
    '<b>Part (ii) — Replace with i7 3.2GHz:</b>',
    'Clock rate is the same, so same time per clock cycle.',
    'However, i7 typically has better IPC (Instructions Per Cycle) — better branch prediction, larger cache.',
    'Execution time DECREASES (fewer cycles needed). Throughput INCREASES.',
    'Additionally, i7 may have more cores → multi-threaded throughput increases significantly.']))
story.append(sp(8))

story.append(p('Question 1(c) — Elapsed Time vs CPU Time', sT))
story.append(qbox('2022','1c','10%','Describe elapsed time and CPU time'))
story.append(sp(4))
story.append(abox([
    '<b>Elapsed Time (Wall-clock time):</b> Total real-world time from program start to finish, including: CPU time, I/O wait, OS scheduling delays, and other programs sharing the CPU.',
    '<b>CPU Time:</b> Time the CPU spends executing ONLY your program (excludes I/O waits and other processes).',
    'CPU Time is further split into: User CPU time (your program code) + System CPU time (OS calls on your behalf).',
    'Example: A program that waits 2 seconds for disk I/O — elapsed time = 3 s, CPU time = 1 s.']))
story.append(sp(8))

story.append(p('Question 1(d) — CPI, Execution Time, MIPS for P1 and P2', sT))
story.append(qbox('2022','1d','25%','P1=2.5GHz, P2=3.2GHz, IC=2M — instruction mix given'))
story.append(sp(4))
story.append(calcbox([
    'Instruction mix: A=20% CPI(P1=3,P2=2), B=20% CPI(P1=2,P2=1), C=30% CPI(P1=1,P2=5), D=30% CPI(P1=4,P2=3)',
    '',
    'CPI_P1 = 0.20×3 + 0.20×2 + 0.30×1 + 0.30×4',
    '       = 0.60 + 0.40 + 0.30 + 1.20 = 2.50',
    '',
    'CPI_P2 = 0.20×2 + 0.20×1 + 0.30×5 + 0.30×3',
    '       = 0.40 + 0.20 + 1.50 + 0.90 = 3.00',
    '',
    'T_P1 = 2,000,000 × 2.50 / 2,500,000,000 = 5,000,000 / 2,500,000,000 = 0.002 s = 2.0 ms',
    'T_P2 = 2,000,000 × 3.00 / 3,200,000,000 = 6,000,000 / 3,200,000,000 = 0.001875 s = 1.875 ms',
    '',
    'MIPS_P1 = 2500 / 2.50 = 1000 MIPS',
    'MIPS_P2 = 3200 / 3.00 = 1066.7 MIPS',
]))
story.append(abox(['P1: CPI=2.50, Time=2.000ms, MIPS=1000',
                   'P2: CPI=3.00, Time=1.875ms, MIPS=1066.7',
                   'P2 is faster despite higher CPI due to its significantly higher clock rate.']))
story.append(sp(8))

story.append(p('Question 1(e) — Amdahl\'s Law: Two Redesigns Q and R', sT))
story.append(qbox('2022','1e','25%','P=36ms; Q takes 30ms for 48%; R takes 40ms for 54% — find best speedup'))
story.append(sp(4))
story.append(calcbox([
    'Design Q: improved portion takes 30ms (speedup_Q = 36/30 = 1.2x), f_Q = 0.48',
    'Design R: improved portion takes 40ms (speedup_R = 36/40 = 0.9x — actually SLOWER), f_R = 0.54',
    '',
    'Design Q Amdahl speedup:',
    '  Speedup_Q = 1 / [(1-0.48) + 0.48/1.2]',
    '            = 1 / [0.52 + 0.40]',
    '            = 1 / 0.92 = 1.087x',
    '',
    'Design R: since 40ms > 36ms, R makes that portion SLOWER. Overall speedup < 1 (slowdown).',
    '  Speedup_R = 1 / [(1-0.54) + 0.54/(36/40)]',
    '            = 1 / [0.46 + 0.54×(40/36)]',
    '            = 1 / [0.46 + 0.60] = 1 / 1.06 = 0.943x  (slowdown!)',
]))
story.append(abox(['<b>Design Q achieves the highest speedup: 1.087x (8.7% improvement).</b>',
                   'Design R actually degrades performance — the improved portion runs slower (40ms > 36ms).']))
story.append(sp(8))

story.append(p('Question 1(f) — Assembly: Sum of array of 10 numbers', sT))
story.append(qbox('2022','1f','20%','Complete the assembly program to find sum'))
story.append(sp(4))
story.append(calcbox([
    '# Find the sum of numbers - write your code',
    'la $t0, numarray          # load base address of the array',
    '',
    'sum_loop:',
    '    beq  $a2, $a3, done   # if index == size (10), exit',
    '    sll  $t1, $a2, 2      # byte offset = index * 4',
    '    add  $t2, $t0, $t1    # address = base + offset',
    '    lw   $t3, 0($t2)      # load array[index]',
    '    add  $a1, $a1, $t3    # sum = sum + array[index]',
    '    addi $a2, $a2, 1      # index++',
    '    j    sum_loop          # repeat',
    '',
    'done:',
    '    # $a1 now contains the sum',
    '    # (print and exit code not needed per question)',
]))
story.append(abox(['$a2 is the index (0..9), $a3=10 is the bound, $a1 accumulates the sum.',
    'sll $t1,$a2,2 computes byte offset (index×4) since integers are 4 bytes.',
    'add + lw loads each element; add $a1 accumulates the running sum.']))
story.append(sp(8))

story.append(p('Question 2 — R-type, I-type, and Instruction Execution', sT))
story.append(qbox('2022','2c','60%','Trace sub $t1,$t2,$t3 | lw $t1,offset($t2) | je $t1,$t2,$a'))
story.append(sp(4))
story.append(p('sub $t1,$t2,$t3 (R-type):', sH3))
story.append(p('Identical to add execution with funct=34 (subtract). '
    'ALU performs $t2-$t3 and writes result to $t1. '
    'Control: RegDst=1, ALUSrc=0, MemToReg=0, RegWrite=1, MemRead=0, MemWrite=0, ALUOp=10.', sB))
story.append(sp(5))
story.append(p('lw $t1,offset($t2) (I-type):', sH3))
story.append(p('Identical to 2020 Q2(d) answer above — '
    'effective address = $t2+offset computed by ALU, data memory read, result written to $t1.', sB))
story.append(sp(5))
story.append(p('je $t1,$t2,$a (Branch I-type):', sH3))
story.append(p('Identical to 2021 Q2(c)(iii) above — ALU computes $t1-$t2, '
    'Zero flag drives branch decision, PC updates to $a if equal else PC+4.', sB))
story.append(sp(8))

story.append(p('Question 3 — Memory Hierarchy, Average Access Time, Cache (2022)', sT))
story.append(qbox('2022','3c','20%','4-level: L1=10ns h=40%, L2=30ns h=60%, RAM=60ns h=80%, SSD=100ns h=100%'))
story.append(sp(4))
story.append(calcbox([
    'T = h1×T1 + (1-h1)×{h2×T2 + (1-h2)×[h3×T3 + (1-h3)×T4]}',
    '',
    '  = 0.40×10 + 0.60×{0.60×30 + 0.40×[0.80×60 + 0.20×100]}',
    '  = 4 + 0.60×{18 + 0.40×[48 + 20]}',
    '  = 4 + 0.60×{18 + 0.40×68}',
    '  = 4 + 0.60×{18 + 27.2}',
    '  = 4 + 0.60×45.2',
    '  = 4 + 27.12',
    '  = 31.12 ns',
]))
story.append(abox(['Average Access Time = <b>31.12 ns</b>']))
story.append(sp(5))

story.append(p('Question 3(d)(e) — Direct-Mapped and Set-Associative (256KiB mem, 8KiB cache, 16-word blocks):', sH3))
story.append(calcbox([
    'Block size = 16 words × 4 bytes = 64 bytes',
    'Offset bits = log2(64) = 6 bits',
    '',
    '--- Direct Mapped ---',
    'Cache lines = 8 KiB / 64 B = 128 lines',
    'Index bits = log2(128) = 7 bits',
    'Total address bits = log2(256 KiB) = log2(262144) = 18 bits',
    'Tag bits = 18 - 7 - 6 = 5 bits',
    'Address: | Tag (5b) | Index (7b) | Offset (6b) |',
    '',
    'Actual cache size per line = 1 + 5 + 512 = 518 bits',
    'Total = 128 × 518 = 66,304 bits = 8,288 bytes = 8.094 KiB',
    '',
    '--- Set-Associative (set size = 8 blocks) ---',
    'Number of sets = 128 / 8 = 16 sets',
    'Set bits = log2(16) = 4 bits',
    'Tag bits = 18 - 4 - 6 = 8 bits',
    'Address: | Tag (8b) | Set (4b) | Offset (6b) |',
]))
story.append(abox(['Direct-Mapped: Tag=5b, Index=7b, Offset=6b, Actual size=8.094 KiB',
                   'Set-Associative (8-way): Tag=8b, Set=4b, Offset=6b']))
story.append(sp(8))

story.append(p('Question 4 — Pipeline with li,la,lw,add,lw,add,sw (2022)', sT))
story.append(qbox('2022','4','100%','Memory=100ps, ALU=80ps, Register=60ps'))
story.append(sp(4))
story.append(p('Part (a) — Stage times per instruction type:', sH3))
st22 = htab(['Instruction','IF','ID','EX','MEM','WB'],
    [['li (load immediate)','100 ps','60 ps','80 ps','0 ps','60 ps'],
     ['la (load address)','100 ps','60 ps','80 ps','0 ps','60 ps'],
     ['lw','100 ps','60 ps','80 ps','100 ps','60 ps'],
     ['add (R-type)','100 ps','60 ps','80 ps','0 ps','60 ps'],
     ['sw','100 ps','60 ps','80 ps','100 ps','0 ps']],
    hbg=CB)
story.append(st22); story.append(sp(5))

story.append(p('Part (b) — Non-pipelined first 4 instructions (li,la,lw,add):', sH3))
story.append(calcbox([
    'Clock cycle = longest instruction path = lw = 100+60+80+100+60 = 400 ps',
    '',
    'Non-pipelined: each instruction uses full clock cycle',
    'T = 4 × 400 ps = 1600 ps',
    '',
    'OR using actual times:',
    'li:  100+60+80+0+60   = 300 ps',
    'la:  100+60+80+0+60   = 300 ps',
    'lw:  100+60+80+100+60 = 400 ps',
    'add: 100+60+80+0+60   = 300 ps',
    'Total = 1300 ps',
]))
story.append(abox(['Non-pipelined time = <b>1600 ps</b> (using fixed 400 ps clock for all)']))
story.append(sp(5))

story.append(p('Part (c) — Pipelined first 4 instructions:', sH3))
story.append(calcbox([
    'Pipeline clock = 100 ps (slowest stage = MEM)',
    'T = (4 + 5 - 1) × 100 = 8 × 100 = 800 ps',
]))
story.append(abox(['Pipelined time = <b>800 ps</b>']))
story.append(sp(5))

story.append(p('Part (d) — Data Hazards in full program:', sH3))
story.append(p('<b>Program:</b> li $t0,0 | la $t1,numarray | lw $t2,0($t1) | add $t0,$t0,$t2 | lw $t2,4($t1) | add $t0,$t0,$t2 | sw $t0,0($t0)', sC))
haz22 = htab(['Hazard','Pair','Type','Justification'],
    [['H1','lw $t2 (inst 3) → add $t0,$t0,$t2 (inst 4)','RAW Load-Use','add reads $t2 in ID stage (cycle 5) but lw writes $t2 in WB stage (cycle 7). 1 stall needed even with forwarding.'],
     ['H2','lw $t2 (inst 5) → add $t0,$t0,$t2 (inst 6)','RAW Load-Use','Same pattern: add reads $t2 before lw completes WB. Another 1-cycle stall needed.'],
     ['H3','add (inst 4) → sw $t0 (inst 7)','RAW (resolved by forwarding)','sw reads $t0 written by add. 3 instructions apart — MEM/WB forwarding resolves this without stall.'],
     ['H4','la $t1 → lw 0($t1) (inst 3)','RAW (resolved by forwarding)','lw reads $t1 written by la. 1 instruction apart — EX/MEM forwarding can resolve.']],
    hbg=CR)
story.append(haz22); story.append(sp(8))

story.append(PageBreak())

# ═══════════════════════════ 2023 PAPER ══════════════════════════════════════
story.append(banner('2023 EXAMINATION — Model Answers', CR, sub='University of Jaffna · CSC207S3 Computer Architecture'))
story.append(sp(10))

story.append(p('Question 1(a) — CPI Definition and Formula', sT))
story.append(qbox('2023','1a','10%','Define CPI and state its formula and components'))
story.append(sp(4))
story.append(abox([
    '<b>CPI (Cycles Per Instruction)</b> is the average number of clock cycles the CPU takes to execute one instruction.',
    'Formula: CPI = Total Clock Cycles / Total Instruction Count',
    'Effective CPI (weighted): CPI_eff = Σ (CPI_i × freq_i)',
    'Components: CPI_i = CPI of instruction class i; freq_i = fraction of instructions in class i.',
    'A lower CPI means the processor executes instructions more efficiently.']))
story.append(sp(8))

story.append(p('Question 1(b) — CPI, CPU Time, Throughput, MIPS for BP1 and BP2', sT))
story.append(qbox('2023','1b','40%','Processor P at 2.5 MHz — BP1 and BP2 benchmark programs'))
story.append(sp(4))
story.append(p('Note: 2.5 MHz clock (2,500,000 Hz) — unusually slow; using as given.', sN))
story.append(calcbox([
    'Instruction mix (thousands): ',
    'BP1: A=30K(CPI=2), B=10K(CPI=1), C=20K(CPI=4), D=20K(CPI=3). Total IC=80K',
    'BP2: A=40K(CPI=2), B=20K(CPI=1), C=20K(CPI=4), D=10K(CPI=3). Total IC=90K',
    '',
    '--- Part (i): CPI ---',
    'CPI_BP1 = (30×2 + 10×1 + 20×4 + 20×3) / 80',
    '        = (60 + 10 + 80 + 60) / 80 = 210 / 80 = 2.625',
    '',
    'CPI_BP2 = (40×2 + 20×1 + 20×4 + 10×3) / 90',
    '        = (80 + 20 + 80 + 30) / 90 = 210 / 90 = 2.333',
    '',
    '--- Part (ii): CPU Time ---',
    'T_BP1 = IC × CPI / Clock = 80,000 × 2.625 / 2,500,000 = 210,000/2,500,000 = 0.084 s = 84 ms',
    'T_BP2 = 90,000 × 2.333 / 2,500,000 = 210,000/2,500,000 = 0.084 s = 84 ms',
    '',
    '--- Part (iii): Sequential throughput ---',
    'Total time = T_BP1 + T_BP2 = 84 + 84 = 168 ms = 0.168 s',
    'Throughput = 2 programs / 0.168 s = 11.905 programs/second',
    '',
    '--- Part (iv): Parallel throughput (2 cores) ---',
    'Both run simultaneously: time = max(T_BP1, T_BP2) = 84 ms',
    'Throughput = 2 programs / 0.084 s = 23.81 programs/second',
    '',
    '--- Part (v): MIPS ---',
    'Sequential: Total IC = 80K+90K = 170K; Total time = 0.168 s',
    'MIPS_seq = (170,000 / 0.168) / 1,000,000 = 1.012 MIPS',
    '',
    'Parallel: Time = 0.084 s; Total IC = 170K',
    'MIPS_par = (170,000 / 0.084) / 1,000,000 = 2.024 MIPS',
]))
story.append(abox(['BP1: CPI=2.625, Time=84ms | BP2: CPI=2.333, Time=84ms',
                   'Sequential throughput=11.9 programs/s, Parallel=23.8 programs/s',
                   'Sequential MIPS=1.012, Parallel MIPS=2.024']))
story.append(sp(8))

story.append(p('Question 1(c) — Combined Amdahl\'s Law (Designs Q and R together)', sT))
story.append(qbox('2023','1c','20%','P=50ms; Q runs 40ms for 60%; R runs 45ms for 70%'))
story.append(sp(4))
story.append(p('Part (i) — Speedup of redesign Q alone:', sH3))
story.append(calcbox([
    'f_Q = 0.60, s_Q = 50/40 = 1.25 (that portion runs 1.25x faster)',
    '',
    'Speedup_Q = 1 / [(1-0.60) + 0.60/1.25]',
    '          = 1 / [0.40 + 0.48]',
    '          = 1 / 0.88',
    '          = 1.136x',
]))
story.append(abox(['Speedup of Q = <b>1.136x</b>']))
story.append(sp(5))

story.append(p('Part (ii) — Both Q and R implemented together:', sH3))
story.append(calcbox([
    'Apply Q first: T_afterQ = 50 × [(1-0.60) + 0.60/1.25]',
    '                        = 50 × [0.40 + 0.48] = 50 × 0.88 = 44 ms',
    '',
    'Now apply R to the 44ms time:',
    '  s_R = 50/45 = 1.111 (R makes its 70% portion 1.111x faster, based on original 50ms)',
    '  But the fraction covered by R overlaps with Q.',
    '',
    'Simpler approach: combine both improvements on original time:',
    '  Time_QR = T × [(1-f_Q) × (1-f_R_outside_Q) portion + improved portions]',
    '',
    'Conservative combined approach (non-overlapping worst case):',
    '  Portion only Q improves: (0.60-0.70 overlap) ... use independent fractions',
    '  If Q covers 60% and R covers 70% with some overlap, assuming independent:',
    '  Combined time = 50 × [(1-0.60)(1-0.70) + 0.60/1.25×(1-0.70) + 0.70/1.111×(1-0.60) + 0.60×0.70/(1.25×1.111)]',
    '',
    'Simpler exam approach (sequential application):',
    '  After Q: T1 = 44 ms',
    '  Apply R to T1 (R improves 70% of ORIGINAL time proportion):',
    '  T_final = T1 × [(1-0.70) + 0.70×(45/50)]',
    '          = 44 × [0.30 + 0.63] = 44 × 0.93 = 40.92 ms',
    '',
    '  Combined speedup = 50 / 40.92 = 1.222x',
]))
story.append(abox(['Combined speedup (Q+R) ≈ <b>1.222x</b>',
                   'This exceeds Q alone (1.136x), showing that combining improvements yields greater gains.']))
story.append(sp(8))

story.append(p('Question 1(d) — Techniques to improve performance without increasing frequency', sT))
story.append(qbox('2023','1d','10%','Alternatives to clock frequency increase'))
story.append(sp(4))
story.append(abox([
    '<b>Multi-core processors:</b> Run multiple threads in parallel on separate cores — increases throughput.',
    '<b>Instruction-Level Parallelism (ILP):</b> Superscalar execution — issue multiple instructions per cycle.',
    '<b>Out-of-order execution:</b> Execute instructions in a different order to avoid waiting for dependencies.',
    '<b>Larger/smarter caches:</b> Reduce memory stalls by keeping more data close to the CPU.',
    '<b>Branch prediction:</b> Speculatively execute the likely branch path to avoid pipeline stalls.',
    '<b>SIMD (Single Instruction Multiple Data):</b> One instruction processes multiple data elements (e.g., AVX).']))
story.append(sp(8))

story.append(p('Question 1(e) — Assembly: Read characters and convert octal to decimal', sT))
story.append(qbox('2023','1e','20%','Pseudocode: read chars, compute dvalue = dvalue×8 + val, exit on non-octal'))
story.append(sp(4))
story.append(calcbox([
    '.text',
    '.globl main',
    'main:',
    '    li   $t0, 0           # dvalue = 0',
    '',
    'read_loop:',
    '    li   $v0, 12          # syscall: read character',
    '    syscall',
    '    move $t1, $v0         # ch = input character (ASCII)',
    '',
    '    addi $t2, $t1, -48   # val = ASCII(ch) - 48 (48 = ASCII of \'0\')',
    '',
    '    # Check: val < 0',
    '    bltz $t2, print_exit  # if val < 0, exit',
    '',
    '    # Check: val > 7',
    '    li   $t3, 7',
    '    bgt  $t2, $t3, print_exit  # if val > 7, exit',
    '',
    '    # dvalue = dvalue * 8 + val',
    '    sll  $t0, $t0, 3     # dvalue = dvalue << 3  (multiply by 8)',
    '    add  $t0, $t0, $t2   # dvalue = dvalue + val',
    '',
    '    j    read_loop        # repeat',
    '',
    'print_exit:',
    '    li   $v0, 1           # syscall: print integer',
    '    move $a0, $t0         # argument = dvalue',
    '    syscall',
    '',
    '    li   $v0, 10          # syscall: exit',
    '    syscall',
]))
story.append(abox(['syscall 12 reads one character (ASCII value returned in $v0).',
    'Subtracting 48 converts ASCII digit to numeric value (\'0\'=48, \'1\'=49, ..., \'7\'=55).',
    'sll $t0,$t0,3 is multiply-by-8 (left shift 3 positions = ×2³).',
    'bltz exits if val<0 (non-digit character); bgt exits if val>7 (not octal digit 0-7).']))
story.append(sp(8))

story.append(p('Question 2 — 2023 Datapath: add, lw, je Instructions', sT))
story.append(qbox('2023','2c','80%','Identify instruction type and trace through datapath for α,β,γ'))
story.append(sp(4))

story.append(p('α) add $t1,$t2,$t3 — R-type instruction:', sH3))
r23_tbl = htab(['Field','op','rs','rt','rd','shamt','funct'],
    [['Value','000000 (0)','01010 ($t2=10)','01011 ($t3=11)','01001 ($t1=9)','00000','100000 (32)']],
    hbg=CB)
story.append(r23_tbl); story.append(sp(4))
story.append(p('Datapath trace: Path F (Instr[31-26]) → Control Unit sets RegDst=1, ALUSrc=0, RegWrite=1, ALUOp=10. '
    'Path A (Instr[25-21]) → reads $t2. Path B (Instr[20-16]) → reads $t3. '
    'Both values go to ALU. funct=32 → ALU adds. Result written to rd=$t1 via MUX(RegDst=1, selects Path C Instr[15-11]).', sB))
story.append(sp(6))

story.append(p('β) lw $t1,10($t2) — I-type instruction:', sH3))
i23_tbl = htab(['Field','op','rs ($t2)','rt ($t1)','immediate (10)'],
    [['Value','100011 (35)','01010 (10)','01001 (9)','0000 0000 0000 1010']],
    hbg=CT)
story.append(i23_tbl); story.append(sp(4))
story.append(p('Datapath trace: Control sets RegDst=0, ALUSrc=1, MemToReg=1, MemRead=1, RegWrite=1. '
    'Path A reads $t2 (base). Path D sign-extends 10 to 32 bits. '
    'ALUSrc MUX selects immediate → ALU computes $t2+10. '
    'Data Memory reads that address. MemToReg MUX selects memory output. Written to rt=$t1.', sB))
story.append(sp(6))

story.append(p('γ) je $t1,$t2,loop — I-type branch instruction:', sH3))
b23_tbl = htab(['Field','op','rs ($t1)','rt ($t2)','offset (to loop)'],
    [['Value','000100 (4)','01001 (9)','01010 (10)','signed offset']],
    hbg=CR)
story.append(b23_tbl); story.append(sp(4))
story.append(p('Datapath trace: Control sets Branch=1, ALUSrc=0, RegWrite=0, ALUOp=01 (subtract). '
    'Paths A and B read $t1 and $t2. ALU subtracts: Zero=1 if $t1==$t2. '
    'Path D sign-extends offset → Shift-Left-2 → add with PC+4 = branch target. '
    'AND(Branch,Zero) drives MUX: if Zero=1, PC = loop; else PC = PC+4.', sB))
story.append(sp(8))

story.append(p('Question 3 — Cache: Spatial/Temporal Locality, Avg Access Time, Fully Assoc., Set Assoc.', sT))
story.append(qbox('2023','3','100%','256KiB mem, 8KiB cache, 16-word blocks, 4 bytes/word'))
story.append(sp(4))

story.append(p('Part (a) — Spatial and Temporal Locality:', sH3))
loc23 = htab(['Type','Concept','Programming Example'],
    [['Temporal Locality','Recently accessed data will likely be accessed again soon.',
      'for(i=0;i<n;i++) sum+=arr[i]; — variable sum accessed every iteration.'],
     ['Spatial Locality','Data near recently accessed data will likely be accessed soon.',
      'for(i=0;i<n;i++) sum+=arr[i]; — arr[0],arr[1],arr[2]... accessed sequentially.']],
    hbg=CP)
story.append(loc23); story.append(sp(5))

story.append(p('Part (c) — Average Access Time (4-level hierarchy):', sH3))
story.append(calcbox([
    'L1: 2ns, h1=0.70 | L2: 8ns, h2=0.85 | DRAM: 40ns, h3=0.95 | SSD: 120ns',
    '',
    'T = 0.70×2 + 0.30×{0.85×8 + 0.15×[0.95×40 + 0.05×120]}',
    '  = 1.40 + 0.30×{6.80 + 0.15×[38 + 6]}',
    '  = 1.40 + 0.30×{6.80 + 0.15×44}',
    '  = 1.40 + 0.30×{6.80 + 6.60}',
    '  = 1.40 + 0.30×13.40',
    '  = 1.40 + 4.02',
    '  = 5.42 ns',
]))
story.append(abox(['Average access time = <b>5.42 ns</b>']))
story.append(sp(5))

story.append(p('Part (d)(i) — Fully Associative Cache (256KiB mem, 8KiB cache, 16 words/block, 4B/word):', sH3))
story.append(calcbox([
    'Block size = 16 × 4 = 64 bytes',
    'Offset bits = log2(64) = 6 bits',
    '',
    'Total address bits = log2(256 KiB) = log2(262144) = 18 bits',
    '',
    'Fully associative: NO index field',
    'Tag bits = 18 - 6 = 12 bits',
    '',
    'Address: | Tag (12 bits) | Block Offset (6 bits) |',
    '',
    'Cache has: 8 KiB / 64 B = 128 lines',
    'Each line compared simultaneously on lookup (expensive CAM hardware)',
]))
story.append(abox(['Fully Associative: Tag=12 bits, Offset=6 bits, No index field',
                   '128 cache lines — each with a 12-bit tag compared in parallel.']))
story.append(sp(5))

story.append(p('Part (d)(ii) — Set Associative (set size = 16 blocks):', sH3))
story.append(calcbox([
    'Number of sets = 128 cache lines / 16 blocks per set = 8 sets',
    'Set bits = log2(8) = 3 bits',
    'Tag bits = 18 - 3 - 6 = 9 bits',
    '',
    'Address: | Tag (9 bits) | Set (3 bits) | Offset (6 bits) |',
    '',
    'Total = 9 + 3 + 6 = 18 bits ✓',
]))
story.append(abox(['Set-Associative (16-way): Tag=9 bits, Set=3 bits, Offset=6 bits']))
story.append(sp(5))

story.append(p('Part (d)(iii) — Actual cache size for set-associative:', sH3))
story.append(calcbox([
    'Each cache line = valid bit (1) + tag (9) + data (16 words × 32 bits = 512 bits)',
    '               = 1 + 9 + 512 = 522 bits',
    'Total = 128 lines × 522 bits = 66,816 bits = 8,352 bytes = 8.156 KiB',
]))
story.append(abox(['Actual cache size = <b>8.156 KiB</b>']))
story.append(sp(8))

story.append(p('Question 4 — Pipelining: ILP, 5-Stage Example, MIPS Features, Hazards', sT))
story.append(qbox('2023','4','100%','Pipeline analysis with data and control hazards'))
story.append(sp(4))

story.append(p('Part (a) — Instruction-Level Parallelism (ILP) and Pipelining:', sH3))
story.append(abox([
    '<b>Instruction-Level Parallelism (ILP)</b> is the potential to execute multiple instructions simultaneously because they are independent of each other.',
    '<b>Pipelining</b> exploits ILP by overlapping the execution stages of sequential instructions.',
    'Like a factory assembly line: while instruction N is in EX stage, instruction N+1 is in ID, and N+2 is in IF.',
    'This keeps all hardware units busy simultaneously, increasing throughput without increasing clock speed.']))
story.append(sp(5))

story.append(p('Part (b) — Pipelining improvement with 5-stage pipeline example:', sH3))
story.append(calcbox([
    'Example: 5 add instructions, clock cycle = 200 ps',
    '',
    'Non-pipelined: 5 × (5 stages × 200 ps) = 5 × 1000 = 5000 ps',
    '',
    'Pipelined:',
    '  add1: IF ID EX MEM WB',
    '  add2:    IF ID EX  MEM WB',
    '  add3:       IF ID  EX  MEM WB',
    '  add4:          IF  ID  EX  MEM WB',
    '  add5:              IF  ID  EX  MEM WB',
    '  Cycles: 1  2  3   4   5   6   7   8   9',
    '',
    'Time = (5+5-1) × 200 ps = 9 × 200 = 1800 ps',
    'Speedup = 5000/1800 = 2.78x',
]))
story.append(sp(5))

story.append(p('Part (c) — MIPS features that facilitate pipelining:', sH3))
story.append(abox([
    '1. <b>Fixed 32-bit instruction length</b> — every instruction is the same size, so Instruction Fetch takes exactly one memory access.',
    '2. <b>Regular instruction formats (R/I/J-type)</b> — register fields (rs,rt,rd) are always in the same bit positions, allowing simultaneous decode and register read.',
    '3. <b>Load-Store architecture</b> — only lw/sw access memory; all computation uses registers, keeping MEM stage simple.',
    '4. <b>Aligned memory accesses</b> — memory accesses are always word-aligned, so Data Memory access takes exactly one cycle.']))
story.append(sp(5))

story.append(p('Part (d) — Hazards in the given MIPS program:', sH3))
story.append(p('<b>Program:</b> li $t0,0 | li $t1,100 | move $t2,$v0 | add $t0,$t0,$t2 | ble $t0,$t1,loop | syscall', sC))

story.append(p('Part (d)(i) — Data Hazard and Control Hazard:', sH3))
story.append(abox([
    '<b>Data Hazard (RAW):</b> move $t2,$v0 (instruction 3) writes $t2. add $t0,$t0,$t2 (instruction 4) reads $t2 immediately after.',
    'Without forwarding: add tries to read $t2 in its ID stage (cycle 5) but move has not yet completed WB (cycle 6). → RAW hazard.',
    '',
    '<b>Control Hazard:</b> ble $t0,$t1,loop (instruction 5) is a branch.',
    'After fetching ble, the CPU speculatively fetches syscall. But if $t0 <= $t1, the branch is taken and PC jumps to loop.',
    'The speculatively fetched syscall must be flushed → 1-2 wasted cycles.']))
story.append(sp(5))

story.append(p('Part (d)(ii) — Two hazards with resolution:', sH3))
haz23 = htab(['#','Type','Instruction Pair','Dependency','Resolution'],
    [['1','Data Hazard (RAW)','move $t2,$v0 → add $t0,$t0,$t2',
      'add reads $t2 which move writes. Only 1 instruction apart.',
      'EX/MEM forwarding: pass move\'s ALU result directly to add\'s EX stage input without waiting for WB.'],
     ['2','Control Hazard','ble $t0,$t1,loop → syscall',
      'Branch outcome not known until end of EX stage. syscall already fetched.',
      'Branch prediction (predict not taken): execute syscall speculatively. If branch IS taken, flush syscall and redirect PC to loop.']],
    hbg=CR)
story.append(haz23)
story.append(sp(12))

# ── QUICK REFERENCE SUMMARY ───────────────────────────────────────────────────
story.append(banner('Quick Formula & Fact Reference', CN))
story.append(sp(8))
story.append(p('Key Formulas', sT))
ref_tbl = htab(['Formula','Expression','Notes'],
    [['CPU Time','IC × CPI_eff × (1/Clock Rate)','Basic performance equation'],
     ['Effective CPI','Σ (CPI_i × freq_i)','Weighted average across instruction classes'],
     ['MIPS','Clock Rate (MHz) / CPI_eff','Million instructions per second'],
     ['Basic Speedup','T_old / T_new','Simple ratio'],
     ["Amdahl's Law",'1 / [(1-f) + f/s]','f=fraction improved, s=speedup of that fraction'],
     ['Avg Access (2L)','h1×T1 + (1-h1)×T2','Two-level memory'],
     ['Avg Access (3L)','h1×T1 + (1-h1)×[h2×T2+(1-h2)×T3]','Three-level memory'],
     ['Cache Offset bits','log2(block_size_in_words)','Block offset field'],
     ['Direct-map Index','log2(num_cache_lines)','Index field'],
     ['Set-assoc Set bits','log2(num_sets); num_sets=total_lines/set_size','Set field'],
     ['Tag bits','total_addr_bits - index_bits - offset_bits','Remaining bits'],
     ['Pipeline time','(N + stages - 1) × cycle_time','Ideal, no hazards'],
     ['Non-pipeline time','N × Σ(stage_times)','Sum all stages per instruction']],
    hbg=CN)
story.append(ref_tbl)
story.append(sp(8))
story.append(p('<i>CSC207S3 Computer Architecture — Complete Exam Answer Booklet · University of Jaffna · '
               'Model answers for 2020, 2021, 2022, 2023 examinations</i>', sSm))

# ── BUILD ─────────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    '/mnt/user-data/outputs/CSC207S3_Complete_Exam_Answers.pdf',
    pagesize=A4,
    leftMargin=M, rightMargin=M, topMargin=M, bottomMargin=M,
    title='CSC207S3 Complete Exam Answer Booklet 2020-2023'
)
doc.build(story)
print("Done — PDF generated.")
