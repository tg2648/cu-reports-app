"""
Color definitions for various charts

https://htmlcolorcodes.com/color-chart/
"""

colors = {
    'blue1': '#295783',
    'blue2': '#6798C1',
    'blue3': '#92C0DF',
    'blue4': '#89B8DA',
    'blue5': '#B9DDF1',
    'gray1': '#57606C',
    'gray2': '#C7C7C7',
    'gray3': '#ABABAB',
    'gray4': '#57606C',
    'orange1': '#D75521',
    'orange2': '#FFAE34',
    'yellow1': '#F7A84A',
    'yellow2': '#D3C95F',
    'green1': '#146C36',
    'green2': '#67A956',
    'green3': '#A3BD5A',
    'red1': '#EF6F6A',
    'teal1': '#8CC2CA',
}


faculty_colors = {
    'Tenured': colors.get('blue1'),
    'NTBOT': colors.get('blue2'),
    'NTBOT-professor-term': colors.get('blue3'),
    'Lecturers': colors.get('gray1'),
    'Other Full-Time': colors.get('gray2'),
    'Adjunct': colors.get('gray3'),
}

students_ug_colors = {
    'maj': colors.get('blue1'),
    'conc': colors.get('blue2'),
    'intdmaj': colors.get('blue3'),
    'min': colors.get('gray3'),
}

students_grad_colors = {
    'existing': colors.get('blue1'),
    'cohort': colors.get('blue2'),
    'selectivity': colors.get('orange1'),
    'yield': colors.get('yellow1'),
}

enrollments_colors = {
    'Tenured': colors.get('blue1'),
    'NTBOT': colors.get('blue2'),
    'NTBOT-professor-term': colors.get('blue4'),
    'Lecturer': colors.get('blue5'),
    'Supplemental': colors.get('gray2'),
    'Part-time': colors.get('gray3'),
    'Graduate-student': colors.get('gray4'),
}

classes_colors = {
    'Tenured': colors.get('green1'),
    'NTBOT': colors.get('green2'),
    'NTBOT-professor-term': colors.get('green3'),
    'Lecturer': colors.get('yellow2'),
    'Supplemental': colors.get('gray2'),
    'Part-time': colors.get('gray3'),
    'Graduate-student': colors.get('gray4'),
}
