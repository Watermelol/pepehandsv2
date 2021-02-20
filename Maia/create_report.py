import time
from datetime import date
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.graphics.shapes import Drawing
from reportlab.lib.colors import pink, black, red, blue, green
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.platypus.tableofcontents import TableOfContents
from .report_storage import uploadReport

def createReport(fileName, dataChart):
    doc = SimpleDocTemplate('/tmp/' + fileName, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)

    Story=[]
    logo = "Maia/static/assets/img/PngItem_3675199.png"
    generateDate = date.today().strftime("%d/%m/%Y")

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))

    PS = ParagraphStyle

    h1 = PS(name = 'Heading1',
            fontSize = 22,
            leading = 16)
    h2 = PS(name = 'Heading2',
            fontSize = 16,
            leading = 14)

    # Cover Page
    Story.append(Spacer(1, 48))
    im = Image(logo, 2*inch, 2*inch)
    Story.append(im)

    Story.append(Spacer(1, 48))
    ptext = '<font size="25">MAIA Detailed Report</font>'
    Story.append(Paragraph(ptext, styles["Center"]))

    Story.append(Spacer(1, 20))
    ptext = '<font size="12">Data Generated <br/> %s</font>' % generateDate
    Story.append(Paragraph(ptext, styles["Center"]))
    Story.append(PageBreak())
    # Cover Page End

    # profit Page
    ptext = '<font>Profit Pillar</font>'
    Story.append(Paragraph(ptext, h1))
    Story.append(Spacer(1, 30))
    chart_title = '<font size="8">Quaterly Profit and Revenue Comparison Chart</font>'
    Story.append(Paragraph(chart_title, styles['Center']))
    Story.append(Spacer(1, 5))
        #Draw Chart
    drawing = Drawing(400, 200)
    data = [
        (dataChart['profit']['chartsData']['profit'][0], dataChart['profit']['chartsData']['profit'][1], dataChart['profit']['chartsData']['profit'][2], dataChart['profit']['chartsData']['profit'][3]),
        (dataChart['profit']['chartsData']['revenue'][0], dataChart['profit']['chartsData']['revenue'][1], dataChart['profit']['chartsData']['revenue'][2], dataChart['profit']['chartsData']['revenue'][3])
    ]
    profit_line_chart = HorizontalLineChart()
    profit_line_chart.x = 50
    profit_line_chart.y = 50
    profit_line_chart.height = 125
    profit_line_chart.width = 300
    profit_line_chart.data = data
    profit_line_chart.joinedLines = 1

    catNames = 'Q1 Q2 Q3 Q4'.split(' ')
    profit_line_chart.categoryAxis.categoryNames = catNames

    profit_line_chart.categoryAxis.labels.boxAnchor = 'n'
    profit_line_chart.valueAxis.valueStep = 50000
    profit_line_chart.lines[0].strokeWidth = 2
    profit_line_chart.lines[1].strokeWidth = 1.5
    drawing.add(profit_line_chart)
    chart_style = TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER'), ('VALIGN', (0, 0), (-1, -1), 'CENTER')])
    charts = Table([[drawing]], style=chart_style)

    table_title = '<font size="8">Quaterly Profit and Revenue Comparison Table</font>'
        #Draw Chart End

        # (dataChart['profit']['chartsData']['profit'][0], dataChart['profit']['chartsData']['profit'][1], dataChart['profit']['chartsData']['profit'][2], dataChart['profit']['chartsData']['profit'][3]),
        # (dataChart['profit']['chartsData']['revenue'][0], dataChart['profit']['chartsData']['revenue'][1], dataChart['profit']['chartsData']['revenue'][2], dataChart['profit']['chartsData']['revenue'][3])
    chart_table = Table([['Quater', 'Profit', 'Revenue'],
                        ['Q1', dataChart['profit']['chartsData']['profit'][0], dataChart['profit']['chartsData']['revenue'][0]],
                        ['Q2', dataChart['profit']['chartsData']['profit'][1], dataChart['profit']['chartsData']['revenue'][1]],
                        ['Q3', dataChart['profit']['chartsData']['profit'][2], dataChart['profit']['chartsData']['revenue'][2]],
                        ['Q4', dataChart['profit']['chartsData']['profit'][3], dataChart['profit']['chartsData']['revenue'][3]],
                        ])

    Story.append(charts)
    Story.append(Paragraph(table_title, styles['Center']))

    Story.append(chart_table)
    Story.append(Spacer(1, 15))
    profit_comments = dataChart['profit']['comments']

    for comment in profit_comments:
        ptext = '<font size="12">%s<br/></font>' % comment.strip()
        Story.append(Paragraph(ptext))
        Story.append(Spacer(1, 8))

    ptext = '<font>Suggestion<br/></font>'
    Story.append(PageBreak())
    Story.append(Paragraph(ptext, h2))
    Story.append(Spacer(1, 15))

    profit_suggestion = dataChart['profit']['suggestions']

    for suggestion in profit_suggestion:
        ptext = '<font size="12">%s<br/></font>' % suggestion.strip()
        Story.append(Paragraph(ptext))
        Story.append(Spacer(1, 8))

    Story.append(PageBreak())
    # Profit Page End

    # Asset Page
    ptext = '<font>Asset Pillar</font>'
    Story.append(Paragraph(ptext, h1))
    Story.append(Spacer(1, 30))
    chart_title = '<font size="8">Return of Asset vs Asset Turnover Ratio vs Debt to Asset Ratio Chart</font>'
    Story.append(Paragraph(chart_title, styles['Center']))
    Story.append(Spacer(1, 5))
        #Draw Chart
    drawing = Drawing(400, 200)
    data = [
    (dataChart['asset']['chartsData']['return_of_asset'], dataChart['asset']['chartsData']['asset_turnover_ratio'], dataChart['asset']['chartsData']['debt_to_asset_ratio'])
    ]

    asset_bar_chart = VerticalBarChart()

    asset_bar_chart.x = 50
    asset_bar_chart.y = 50
    asset_bar_chart.height = 125
    asset_bar_chart.width = 300

    asset_bar_chart.data = data
    asset_bar_chart.strokeColor = black

    asset_bar_chart.categoryAxis.labels.boxAnchor = 'ne'
    asset_bar_chart.categoryAxis.labels.dx = 15
    asset_bar_chart.categoryAxis.labels.dy = -2
    asset_bar_chart.categoryAxis.labels.angle = 30
    asset_bar_chart.categoryAxis.categoryNames = ['Return of Asset','Asset Turnover Ratio','Debt to Asset Ratio']
    drawing.add(asset_bar_chart)
    chart_style = TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER'), ('VALIGN', (0, 0), (-1, -1), 'CENTER')])
    charts = Table([[drawing]], style=chart_style)
        #Draw Chart End

    Story.append(charts)
    Story.append(Spacer(1, 30))
    asset_comments = dataChart['asset']['comments']

    for comment in asset_comments:
        ptext = '<font size="12">%s<br/></font>' % comment.strip()
        Story.append(Paragraph(ptext))
        Story.append(Spacer(1, 8))

    ptext = '<font>Suggestion<br/></font>'
    Story.append(PageBreak())
    Story.append(Paragraph(ptext, h2))
    Story.append(Spacer(1, 15))

    asset_suggestion = dataChart['asset']['suggestions']

    for suggestion in asset_suggestion:
        ptext = '<font size="12">%s<br/></font>' % suggestion.strip()
        Story.append(Paragraph(ptext))
        Story.append(Spacer(1, 8))

    Story.append(PageBreak())
    # Asset Page End

    # Cash Page
    ptext = '<font>Cash Pillar</font>'
    Story.append(Paragraph(ptext, h1))
    Story.append(Spacer(1, 30))
    chart_title = '<font size="8">Quarterly Cash Net Flow Chart</font>'
    Story.append(Paragraph(chart_title, styles['Center']))
    Story.append(Spacer(1, 5))
        #Draw Chart
    drawing = Drawing(400, 200)
    data = [
    (dataChart['cash']['chartsData']['q1_net_cash_flow'], dataChart['cash']['chartsData']['q2_net_cash_flow'], dataChart['cash']['chartsData']['q3_net_cash_flow'], dataChart['cash']['chartsData']['q4_net_cash_flow'],),
    ]
    cash_line_chart = HorizontalLineChart()
    cash_line_chart.x = 50
    cash_line_chart.y = 50
    cash_line_chart.height = 125
    cash_line_chart.width = 300
    cash_line_chart.data = data
    cash_line_chart.joinedLines = 1

    catNames = 'Q1 Q2 Q3 Q4'.split(' ')
    cash_line_chart.categoryAxis.categoryNames = catNames

    cash_line_chart.categoryAxis.labels.boxAnchor = 'n'
    cash_line_chart.lines[0].strokeWidth = 2
    cash_line_chart.lines[1].strokeWidth = 1.5
    drawing.add(cash_line_chart)
    chart_style = TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER'), ('VALIGN', (0, 0), (-1, -1), 'CENTER')])
    charts = Table([[drawing]], style=chart_style)

    table_title = '<font size="8">Quarterly Cash Net Flow Table</font>'
        #Draw Chart End

    Story.append(charts)
    Story.append(Paragraph(table_title, styles['Center']))
    chart_table = Table([['Quater', 'Net Cash Flow'],
                        ['Q1', dataChart['cash']['chartsData']['q1_net_cash_flow']],
                        ['Q2', dataChart['cash']['chartsData']['q1_net_cash_flow']],
                        ['Q3', dataChart['cash']['chartsData']['q1_net_cash_flow']],
                        ['Q4', dataChart['cash']['chartsData']['q1_net_cash_flow']],
                        ])

    Story.append(chart_table)
    Story.append(Spacer(1, 15))
    cash_comments = dataChart['cash']['comments']

    for comment in cash_comments:
        ptext = '<font size="12">%s<br/></font>' % comment.strip()
        Story.append(Paragraph(ptext))
        Story.append(Spacer(1, 8))

    ptext = '<font>Suggestion<br/></font>'
    Story.append(PageBreak())
    Story.append(Paragraph(ptext, h2))
    Story.append(Spacer(1, 15))

    cash_suggestion = dataChart['cash']['suggestions']

    for suggestion in cash_suggestion:
        ptext = '<font size="12">%s<br/></font>' % suggestion.strip()
        Story.append(Paragraph(ptext))
        Story.append(Spacer(1, 8))

    Story.append(PageBreak())
    # Cash Page End

    # Liquidity Page
    ptext = '<font>Liquidity Pillar</font>'
    Story.append(Paragraph(ptext, h1))
    Story.append(Spacer(1, 30))
    chart_title = '<font size="8">Quick Ratio vs Current Ratio vs Cash Ratio Chart</font>'
    Story.append(Paragraph(chart_title, styles['Center']))
    Story.append(Spacer(1, 5))
        #Draw Chart
    drawing = Drawing(400, 200)
    data = [
    (dataChart['liquidity']['chartsData']['quick_ratio'], dataChart['liquidity']['chartsData']['current_ratio'], dataChart['liquidity']['chartsData']['cash_ratio'])
    ]

    liquidity_bar_chart = VerticalBarChart()

    liquidity_bar_chart.x = 50
    liquidity_bar_chart.y = 50
    liquidity_bar_chart.height = 125
    liquidity_bar_chart.width = 300

    liquidity_bar_chart.data = data
    liquidity_bar_chart.strokeColor = black

    liquidity_bar_chart.categoryAxis.labels.boxAnchor = 'ne'
    liquidity_bar_chart.categoryAxis.labels.dx = 15
    liquidity_bar_chart.categoryAxis.labels.dy = -2
    liquidity_bar_chart.categoryAxis.labels.angle = 30
    liquidity_bar_chart.categoryAxis.categoryNames = ['Quick Ratio','Current Ratio','Cash Ratio']
    drawing.add(liquidity_bar_chart)
    chart_style = TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER'), ('VALIGN', (0, 0), (-1, -1), 'CENTER')])
    charts = Table([[drawing]], style=chart_style)
        #Draw Chart End

    Story.append(charts)
    liquidity_comments = dataChart['liquidity']['comments']

    for comment in liquidity_comments:
        ptext = '<font size="12">%s<br/></font>' % comment.strip()
        Story.append(Paragraph(ptext))
        Story.append(Spacer(1, 8))

    ptext = '<font>Suggestion<br/></font>'
    Story.append(PageBreak())
    Story.append(Paragraph(ptext, h2))
    Story.append(Spacer(1, 15))

    liquidity_suggestion = dataChart['liquidity']['suggestions']

    for suggestion in liquidity_suggestion:
        ptext = '<font size="12">%s<br/></font>' % suggestion.strip()
        Story.append(Paragraph(ptext))
        Story.append(Spacer(1, 8))

    Story.append(PageBreak())

    doc.build(Story)

    uploadReport('/tmp/' + fileName, fileName)

