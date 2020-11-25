"""
Layout: Top row
Contains the title, changelog, and notes.
"""

# Third party imports
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html


notes_text = dcc.Markdown(
    '''
    The notes below pertain to the department profiles.

    Please note the following about Faculty Type:
    - NTBOT stands for non-tenured but on track. NTBOT counts include term professors with the exception of Mathematics and Statistics where those are called Term Asst. Prof.
    - Lecturers stand for renewable Lecturers in Discipline and Associates in Discipline and Associates in Music Performance
    - Other Full-time stands for non-renewable lecturers
    - Adjunct stands for part-time instructional faculty
    - Graduate St. stands for graduate student instructors

    **Faculty**

    - Full Time Equivalent (FTE) counts are the official Arts and Sciences counts. FTE counts in the Faculty charts are rounded to the nearest whole number. Additional detail can be found by hovering over the relevant FTE count.
    - Instructional FTE (IFTE) accounts for instructional leaves such as sabbaticals.  They are the FTE count in the department minus an estimate of the decrease in instructional obligations.  IFTE calculations are estimates.
    - Underrepresented Minority (URM) are faculty who have self-identified as at least one of the following: Hispanic or Latino, American Indian or Alaska Native, Black or African American, or Native Hawaiian or Other Pacific Islander.

    **Students**

    - Program enrollments are for the fall term of each year. 
    - Each undergraduate program declaration including majors, concentrations, and minors, are counted as 1 student.  
    - Inter-departmental program declarations are counted as 1 student in each department.  In the divisional profiles, inter-departmental programs are counted as 0.5 in each department. 
    - Graduate PhD program are counted as 1 student regardless of what level of the degree they are currently working towards (MA, MPhil, or PhD). 

    **Classes  **

    - Total enrollments for department offered classes include all classes offered by the department, excluding core and laboratory classes.  
    - Class enrollments are included once if co-taught.
    - Graduate Student Appointment: Instructors with graduate student appointments such as Graduate Research Assistant, Preceptor, Teaching Assistant/Fellow, etc. 

    For questions, please contact Timur Gulyamov (<tg2648@columbia.edu>).
    '''
)

changelog_text = dcc.Markdown(
    '''
    **v0.1** *2020-03-24*
    * Initial alpha
    '''
)

contact_text = dcc.Markdown(
    '''
    For any questions, please contact Timur Gulyamov (<tg2648@columbia.edu>) or Rose Razaghian (<rr222@columbia.edu>).
    '''
)

notes_button = dbc.Button(
    "Notes",
    id="notes-popup-button",
    color="link",
    outline=False
)

notes_popup = dbc.Modal(
    [
        dbc.ModalHeader(html.Span('Notes', className='text-info')),
        dbc.ModalBody(notes_text),
        dbc.ModalFooter(dbc.Button("Close", id="close-notes", className="ml-auto", size='sm')),
    ],
    id="notes-popup",
    size="lg",
    scrollable=True
)

changelog_button = dbc.Button(
    "Changelog",
    id="changelog-popup-button",
    color="link",
    outline=False
)

changelog_popup = dbc.Modal(
    [
        dbc.ModalHeader(html.Span('Changelog', className='text-info')),
        dbc.ModalBody(changelog_text),
        dbc.ModalFooter(
            dbc.Button("Close", id="close-changelog", className="ml-auto", size='sm')
        ),
    ],
    id="changelog-popup",
    scrollable=True
)

contact_button = dbc.Button(
    "Contact us",
    id="contact-popup-button",
    color="link",
    outline=False
)

contact_popup = dbc.Modal(
    [
        dbc.ModalHeader(html.Span('Contact us', className='text-info')),
        dbc.ModalBody(contact_text),
        dbc.ModalFooter(
            dbc.Button("Close", id="close-contact", className="ml-auto", size='sm')
        ),
    ],
    id="contact-popup"
)

button_group = dbc.Col(
    dbc.ButtonGroup(
        [
            contact_button,
            changelog_button,
            notes_button
        ],
        size='sm'
    ),
    className='pt-1',
    width='auto'
)

warning_badge = dbc.Col(
    html.Div(
        [
            html.Span('CONFIDENTIAL'),
            html.Span('—For intended recipients only', className='small font-weight-bold')
        ],
        className='mt-2 text-warning font-weight-bold'
    )
)

title = html.H3(
    'Department Profile',
    className='text-info'
)

header = html.Div(
    [
        dbc.Row(
            [
                warning_badge,
                button_group,
                contact_popup,
                changelog_popup,
                notes_popup,
            ],
            justify='between',
            className='mt-2'
        ),
        title
    ]
)
