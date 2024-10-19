"""
Extensible dashboard for project status.
"""

# Import packages
from dash import Dash, html, dcc
import pandas as pd
import plotly.express as px

# Incorporate data
df = pd.read_excel('project_data.xlsx')

# Initialize the app
app = Dash()

# App layout
app.layout = [
	html.H1(children='Project Dashboard', style={'textAlign':'center'}),
	html.Div(children = [
		dcc.Graph(
			figure=px.histogram(
				df,
				x='Preparer',
				color='High Priority?',
				title='Control Count by Preparer'
			),
			style = {'flex-grow':'1'}
		),
		dcc.Graph(
			figure=px.histogram(
				df,
				x='Preparer',
				y='Projected Hours ',
				color='Status ',
				title='Project Hours by Preparer'
			),
			style = {'flex-grow':'1'}
		)
	],
	style = {
		'display':'flex',
		'flex-wrap':'wrap',
		'justify-content':'space-between',
'align-items':'center'}),
	dcc.Graph(
		figure=px.pie(
			df,
			values = df['Preparer'].value_counts().values,
			names=df['Reviewer'].value_counts().index,
			title='Reviewer Breakdown',
			hole=0.5
		)
	)
]

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
