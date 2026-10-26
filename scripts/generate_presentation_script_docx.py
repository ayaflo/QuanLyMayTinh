import os
import re
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def set_cell_background(cell, fill_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def main():
    doc = docx.Document()

    # Set margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

    # Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_uni = p_title.add_run("TRƯỜNG ĐẠI HỌC CÔNG NGHỆ THÔNG TIN - ĐHQG-HCM\nKHOA MẠNG MÁY TÍNH VÀ TRUYỀN THÔNG\n\n")
    r_uni.font.name = "Arial"
    r_uni.font.size = Pt(11)
    r_uni.bold = True
    r_uni.font.color.rgb = RGBColor(71, 85, 105)

    r_main = p_title.add_run("KỊCH BẢN THUYẾT TRÌNH BẢO VỆ CHUYÊN ĐỀ TỐT NGHIỆP\n")
    r_main.font.name = "Arial"
    r_main.font.size = Pt(18)
    r_main.bold = True
    r_main.font.color.rgb = RGBColor(14, 116, 144)

    r_sub = p_title.add_run("ĐỀ TÀI: ỨNG DỤNG QUẢN LÝ MÁY TÍNH TRẺ EM (OPEN GUARDIAN KIDS)\n")
    r_sub.font.name = "Arial"
    r_sub.font.size = Pt(13)
    r_sub.bold = True
    r_sub.font.color.rgb = RGBColor(30, 41, 59)

    p_info = doc.add_paragraph()
    p_info.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_info = p_info.add_run(
        "Sinh viên thực hiện: Nguyễn Minh Hoàng (23127368) & Lê Văn Hoàng Tấn (23127471)\n"
        "Bộ slide trình chiếu: Open_Guardian_Kids_Complete_25_Slides.pptx.pdf (23 slides chuẩn)\n"
        "Thời lượng dự kiến: 18 - 20 phút (Mỗi slide 40 - 60 giây)\n"
    )
    r_info.font.name = "Arial"
    r_info.font.size = Pt(10)
    r_info.font.italic = True
    r_info.font.color.rgb = RGBColor(100, 116, 139)

    doc.add_paragraph()

    # Read the markdown file
    md_path = os.path.join("docs", "KICH_BAN_THUYT_TRINH_23_SLIDES.md")
    with open(md_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Parse and write content
    for line in lines:
        line_s = line.strip()
        if not line_s:
            continue
        
        # Skip header metadata that was already added
        if line_s.startswith("# KỊCH BẢN") or line_s.startswith("## ĐỀ TÀI") or line_s.startswith("* **Hệ đào tạo:") or line_s.startswith("* **Sinh viên:") or line_s.startswith("* **Tài liệu:") or line_s.startswith("* **Tổng thời lượng:"):
            continue

        if line_s.startswith("### SLIDE "):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(14)
            p.paragraph_format.space_after = Pt(4)
            r = p.add_run(line_s.replace("### ", ""))
            r.font.name = "Arial"
            r.font.size = Pt(13)
            r.bold = True
            r.font.color.rgb = RGBColor(14, 116, 144)
        elif line_s.startswith("## "):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(16)
            p.paragraph_format.space_after = Pt(6)
            r = p.add_run(line_s.replace("## ", ""))
            r.font.name = "Arial"
            r.font.size = Pt(14)
            r.bold = True
            r.font.color.rgb = RGBColor(30, 41, 59)
        elif line_s.startswith("#### 🎙️ Lời thoại"):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run("🎙️ LỜI THOẠI THUYẾT TRÌNH (SPEAKING SCRIPT):")
            r.font.name = "Arial"
            r.font.size = Pt(10.5)
            r.bold = True
            r.font.color.rgb = RGBColor(180, 83, 9)
        elif line_s.startswith("> "):
            quote_text = line_s[2:].replace("**", "").replace("*", "")
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Inches(0.25)
            p.paragraph_format.space_after = Pt(4)
            r = p.add_run(quote_text)
            r.font.name = "Arial"
            r.font.size = Pt(10)
            r.font.color.rgb = RGBColor(15, 23, 42)
        elif line_s.startswith("* **"):
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Inches(0.15)
            p.paragraph_format.space_after = Pt(2)
            # Parse bold parts
            clean = line_s.replace("**", "")
            r = p.add_run(clean)
            r.font.name = "Arial"
            r.font.size = Pt(9.5)
            r.font.color.rgb = RGBColor(51, 65, 85)
        else:
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(3)
            r = p.add_run(line_s.replace("**", "").replace("*", ""))
            r.font.name = "Arial"
            r.font.size = Pt(9.5)
            r.font.color.rgb = RGBColor(51, 65, 85)

    out_docx = os.path.join("docs", "KichBan_ThuyetTrinh_OGK_23_Slides.docx")
    doc.save(out_docx)
    print(f"Generated Word script at: {out_docx}")

if __name__ == "__main__":
    main()
