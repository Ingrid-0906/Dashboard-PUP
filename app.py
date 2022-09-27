import dash
from dash import dcc, html, Input, Output
import dash_mantine_components as dmc
from dash_iconify import DashIconify as ic

app = dash.Dash(__name__, use_pages=True,
	meta_tags=[{'name':'viewport','content':'width=devide-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,'}])

server = app.server
server.secret_key=os.environ.get('secret_key','secret')
app.config.suppress_callback_exceptions=True


app.layout = html.Div([
	html.Div(id='locs'),

	# MAIN APP FRAMEWORK
	html.Div(className='bar-search', children=[
		dmc.Group(class_name='bar-bar', children=[
			dmc.Select(id='multi-select',
				data=[page['name'] for page in dash.page_registry.values()],
				searchable=True,
				placeholder='Select a Brand',
				nothingFound="No options found",
				icon=[ic(icon="akar-icons:search")],
				rightSection=[ic(icon="dashicons:arrow-down")]),
			dmc.Avatar(src="https://avatars.githubusercontent.com/u/91216500?v=4",
				radius="xl"),
			html.Div(className='profile', children=[
				html.H4("User_0906", className='user0906'),
				html.H5("Guest", className='guest0906')
			])
		])
	]),
	dash.page_container
	
])

@app.callback(Output('locs','children'),
	[Input('multi-select','value')])
def update_value(value):
	if value == None:
		pass
	else:
		for page in dash.page_registry.values():
			if page['name'] == value:
				return dcc.Location(pathname=page['path'], id="best")
			else:
				pass



if __name__ == '__main__':
    app.run_server(debug=True)
