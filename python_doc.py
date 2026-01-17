import requests
from bs4 import BeautifulSoup
import re
from docx import Document
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT, WD_LINE_SPACING, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, Cm, RGBColor
 
# 常用中英文标点转换
def E_trans_to_C(string):
    E_pun = u',!?[]【】()<>'
    C_pun = u'，！？〔〕〔〕（）《》'
    table= {ord(f):ord(t) for f,t in zip(E_pun,C_pun)}
    return string.translate(table)
# 设置页面样式
def setDocument():
    # -----------文档部分设置-------------#
    document = Document()
    # 文档页面设置
    # A4和页边距
    document.sections[0].page_height = Cm(29.7)
    document.sections[0].page_width = Cm(22)
    document.sections[0].left_margin = Cm(2.8)
    document.sections[0].right_margin = Cm(2.6)
    document.sections[0].top_margin = Cm(2.5)
    document.sections[0].bottom_margin = Cm(2.5)
    return document
 
def AddFooterNumber(run):
    fldChar1 = OxmlElement('w:fldChar')  # creates a new element
    fldChar1.set(qn('w:fldCharType'), 'begin')  # sets attribute on element
    instrText = OxmlElement('w:instrText')
    instrText.set(qn('xml:space'), 'preserve')  # sets attribute on element
    instrText.text = 'Page'
    fldChar2 = OxmlElement('w:fldChar')
    fldChar2.set(qn('w:fldCharType'), 'separate')
    t = OxmlElement('w:t')
    t.text = "Seq"
    fldChar2.append(t)
    fldChar4 = OxmlElement('w:fldChar')
    fldChar4.set(qn('w:fldCharType'), 'end')
    r_element = run._r
    r_element.append(fldChar1)
    r_element.append(instrText)
    r_element.append(fldChar2)
    r_element.append(fldChar4)
 
 
def InsertPageNumber(Doc):
    footer = Doc.sections[0].footer  # 获取第一个节的页脚
    footer.is_linked_to_previous = True  # 编号续前一节
    paragraph = footer.paragraphs[0]  # 获取页脚的第一个段落
    paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER  # 页脚居中对齐
    run_footer = paragraph.add_run()  # 添加页脚内容
 
    AddFooterNumber(run_footer)
    run_footer.first_line_indent = Pt(-32)
 
    font = run_footer.font
    font.name = 'Times New Roman'  # 新罗马字体
    font.size = Pt(14)  # 14号字体
    font.bold = False  # 不加粗
 
# 设置正文样式
def setContent(content):
    content = document.add_paragraph(content)
    document.styles['Normal'].font.name = u'仿宋_GB2312'
    document.styles['Normal'].font.size = Pt(16)
    document.styles['Normal']._element.rPr.rFonts.set(qn('w:eastAsia'), u'仿宋_GB2312') # 中文字体
    document.styles['Normal']._element.rPr.rFonts.set(qn('w:ascii'), u'Times New Roman') # 西文字体
    # document.styles['Normal'].paragraph_format.first_line_indent = document.styles['Normal'].font.size * 2
    document.styles['Normal'].paragraph_format.first_line_indent = Pt(32)
    document.styles['Normal'].paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY  # 行距固定值
    document.styles['Normal'].paragraph_format.line_spacing = Pt(28) # 行距
    document.styles['Normal'].paragraph_format.space_after = Pt(0)
    document.styles['Normal'].paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY  #LEFT,RIGHT,CENTER,JUSTIFY(两端对齐),DISTRIBUTE(分散对齐)
    return content
    # w:ascii -用于前128个Unicode代码点
    # w:cs -用于复杂的脚本代码点
    # w:eastAsia -用于东亚代码点
    # w:hAnsi -代表 高ANSI ，但实际上是对其他三个代码点之一未指定的所有代码点的捕获。
 
# 设置一级标题样式
def setHead1(head_1):
    head = document.add_heading()
    head.paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER # 居中对齐
    head_1 = E_trans_to_C(head_1)
    run = head.add_run(head_1)
    run.font.name = u'方正小标宋简体'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), u'方正小标宋简体')
    run._element.rPr.rFonts.set(qn('w:ascii'), u'Times New Roman')
    document.styles['Heading 1'].font.size = Pt(22) # 字体大小二号
    document.styles['Heading 1'].font.color.rgb=RGBColor(0x00,0x00,0x00) #标题颜色
    document.styles['Heading 1'].paragraph_format.first_line_indent = Pt(0) # 首行缩进
    document.styles['Heading 1'].paragraph_format.line_spacing = Pt(39)
    document.styles['Heading 1'].paragraph_format.space_before = Pt(0)
    document.styles['Heading 1'].paragraph_format.space_after = Pt(0)
    document.styles['Heading 1'].font.bold = False # 不加粗
    return run
 
# 设置文号样式
def setNumber(head_6):
    head = document.add_heading(level=6)
    head.paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER # 居中对齐
    head_6 = E_trans_to_C(head_6)
    run = head.add_run(head_6)
    run.font.name = u'楷体_GB2312'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), u'楷体_GB2312')
    run._element.rPr.rFonts.set(qn('w:ascii'), u'Times New Roman')
    document.styles['Heading 6'].font.size = Pt(16) # 字体大小二号
    document.styles['Heading 6'].font.color.rgb=RGBColor(0x00,0x00,0x00) #标题颜色
    document.styles['Heading 6'].paragraph_format.first_line_indent = Pt(0) # 首行缩进
    document.styles['Heading 6'].paragraph_format.line_spacing = Pt(28)
    document.styles['Heading 6'].paragraph_format.space_before = Pt(0)
    document.styles['Heading 6'].paragraph_format.space_after = Pt(0)
    document.styles['Heading 6'].font.italic = False # 倾斜
    document.styles['Heading 6'].font.bold = False # 加粗
    return run
 
# 设置二级标题样式
def setHead2(head_2):
    head = document.add_heading(level=2)
    head.paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER # 左对齐
    head_2 = E_trans_to_C(head_2)
    run = head.add_run(head_2)
    run.font.name = u'黑体'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), u'黑体')
    run._element.rPr.rFonts.set(qn('w:ascii'), u'Times New Roman')
    document.styles['Heading 2'].font.size = Pt(16) # 字体三号
    document.styles['Heading 2'].font.color.rgb=RGBColor(0x00,0x00,0x00) #标题颜色
    document.styles['Heading 2'].paragraph_format.first_line_indent = 0
    document.styles['Heading 2'].paragraph_format.line_spacing = Pt(28)
    document.styles['Heading 2'].paragraph_format.space_before = Pt(0)
    document.styles['Heading 2'].paragraph_format.space_after = Pt(0)
    document.styles['Heading 2'].font.bold = False # 不加粗
    return run
 
if __name__ == '__main__':
    document = setDocument()
    footer = InsertPageNumber(document)
 
    url = 'http://www.gov.cn/zhengce/content/2021-07/22/content_5626534.htm'
    response = requests.get(url)
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.text, features="html.parser")  # 用html解析器(parser)来分析我们requests得到的html文字内容，soup就是我们解析出来的结果
    company_item = soup.find("td", class_="b12c")  # find是查找，find_all查找全部。查找标记名是div并且class属性是detail_head的全部元素
    title = soup.find("title").text.split('（')[0]
    news = company_item.text.strip() # strip() 方法用于移除字符串头尾指定的字符（默认为空格或换行符）或字符序列。在这里就是移除多余的尖括号的html数据
    # 使用.split('\n')或.splitlines()分割
    format_news = news.splitlines()
    # new = new.replace('\n','\r')
    Contents = {}
    for i in range(len(format_news)):
        # setHead1(format_news[i])
        set_head1 = re.findall('(?<!.)中华人民共和国[\u4e00-\u9fa5]+', format_news[i])
        set_head11 = re.findall(r'(?<!.)'+title+'(?!.)', format_news[i])
        set_number = re.findall('(?<!.)第\d+号(?!.)', format_news[i])
        set_head2 = re.findall('(?<!.)第[一|二|三|四|五|六|七|八|九|十]+章', format_news[i])
        set_date = re.findall('(?<!.)\d{4}年\d{1,2}月\d{1,2}日(?!.)', format_news[i])
 
        if set_number:
            number = format_news[i]
            Contents[i] = setNumber(number)
            setContent('')
        elif set_head1:
            Contents[i] = setHead1(format_news[i])
        elif set_head11:
            Contents[i] = setHead1(format_news[i])
        elif set_head2:
            setContent('')
            Contents[i] = setHead2(format_news[i])
            setContent('')
        elif set_date:
            # 空2行的操作
            year = re.findall('(?<!.)\d{4}', format_news[i])[0]
            Contents[i] = setContent(format_news[i])
            Contents[i-1].insert_paragraph_before()  # 段落的前面插入一个段落
            Contents[i-1].insert_paragraph_before()  # 段落的前面插入一个段落
            Contents[i-1].paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.RIGHT  # 右对齐
            Contents[i].paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.RIGHT  # 右对齐
            run = Contents[i].add_run()
            run.add_break(WD_BREAK.PAGE)
            # print((len(format_news[i - 1])))
            # print((len(format_news[i])))
            # print((len(format_news[i - 1].encode())))
            # print((len(format_news[i].encode())))
            if len(format_news[i-1].encode()) >= len(format_news[i].encode()):
                rightIndent = ((len(format_news[i-1].encode()) - len(format_news[i].encode()))/2 + 4) * 8
                # print(rightIndent)
                Contents[i - 1].paragraph_format.right_indent = Pt(64)  # 右对齐
                Contents[i].paragraph_format.right_indent = Pt(rightIndent)  # 右对齐
            elif len(format_news[i-1].encode()) < len(format_news[i].encode()):
                rightIndent = ((len(format_news[i].encode()) - len(format_news[i-1].encode()))/2 + 4) * 8
                # print(rightIndent)
                Contents[i - 1].paragraph_format.right_indent = Pt(rightIndent)  # 右对齐
                Contents[i].paragraph_format.right_indent = Pt(64)  # 右对齐
        else:
            if format_news[i]:
                set_bold = re.findall('(?<!.)第[一|二|三|四|五|六|七|八|九|十]+条', format_news[i])
                # setContent()
                # if set_bold:
                # Contents[i] = setContent(format_news[i])
                # run = Contents[i].add_run(set_bold[0])
                # run.bold = True
                if set_bold:
                    # print(len(set_bold[0]))
                    Contents[i] = setContent('')
                    run = Contents[i].add_run(set_bold[0])
                    # run.bold = True
                    # 设置中文字体，必须添加下面 3 行代码
                    run.font.name = "黑体"
                    r = run._element.rPr.rFonts
                    r.set(qn("w:eastAsia"), "黑体")
                    Contents[i] = Contents[i].add_run(format_news[i][len(set_bold[0]):])
                    # print(Contents[i])
                else:
                    Contents[i] = setContent(format_news[i])
 
 
    document.save(f'国务院令（{year}）{number}《{title}》.docx')
    print(f'国务院令（{year}）{number} 《{title}》通知已生成')