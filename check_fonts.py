import docx
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def inspect_all():
    for fname in ['Workshop_Developer_to_Tester_completed.docx', 'Workshop2_DataFlowDetection_completed.docx']:
        doc = docx.Document(fname)
        print('=== ' + fname + ' ===')
        for i, p in enumerate(doc.paragraphs):
            has_q = '?' in p.text and '??' in p.text
            for r in p.runs:
                rPr = r._r.find(qn('w:rPr'))
                fonts = None
                if rPr is not None:
                    rFonts = rPr.find(qn('w:rFonts'))
                    if rFonts is not None:
                        fonts = rFonts.attrib
                # print suspicious
                if has_q or fonts is None:
                    print(f'P[{i}]: text={p.text[:60]!r} | run_font={fonts}')

inspect_all()
