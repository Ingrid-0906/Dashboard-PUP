import dash
from dash import dcc, html, Input, Output, callback
import dash_mantine_components as dmc
from dash_iconify import DashIconify as ic
import pandas as pd
import matplotlib.pyplot as plt
import plotly as plt
import plotly.express as px
import plotly.graph_objects as go
import dash_leaflet as dl


base = pd.read_csv("./assets/22092022_dash_allcart.csv")

#
# Opening the data - demographic
gender = pd.read_csv("./assets/demographic_data/GENDER_2021.csv")
income = pd.read_csv("./assets/demographic_data/INCOME_2021.csv")
school = pd.read_csv("./assets/demographic_data/SCHOOL_2021.csv")
race = pd.read_csv("./assets/demographic_data/RACE_2021.csv")
age = pd.read_csv("./assets/demographic_data/AGE_2021.csv")
marital = pd.read_csv("./assets/demographic_data/MARITAL_2021.csv")

# SOME FORMATING BEFORE START
gender.iloc[:,1:] = gender.iloc[:,1:].replace(r'\s*(.*?)\s*',r'\1', regex=True)
race.iloc[:,1:] = race.iloc[:,1:].replace(r'\s*(.*?)\s*',r'\1', regex=True)
income.iloc[:,1:] = income.iloc[:,1:].replace(r'\s*(.*?)\s*',r'\1', regex=True)
school.iloc[:,2:] = school.iloc[:,2:].replace(r'\s*(.*?)\s*',r'\1', regex=True)
age.iloc[:,1:] = age.iloc[:,1:].replace(r'\s*(.*?)\s*',r'\1', regex=True)
age['Label'] = age['Label'].str.strip(' years')
marital['state'] = [word.upper() for word in marital['state']]


# Setting the brand
brand = 'PEPSI'
key = base[base['fullname']==brand].reset_index(drop=True)

dex = key['state'].value_counts().index
sts = dex[0]

# Setting the gender
gex = gender[['Label', sts]].rename(columns={sts:'usa'})
gex['usa'] = pd.to_numeric(gex['usa'])

# GENDER CHART
genderChart = go.Figure(data=[go.Pie(labels=gex['Label'], values=gex['usa'], hole=.8)])
color_gender = ['#004F74','#A3E2FF']

#FORMATING CHART
genderChart.update_layout(showlegend=True,
                     legend=dict(orientation='h'),
                     margin=dict(l=0,r=0,b=0,t=0,pad=4), 
                     paper_bgcolor='#fff',
                     plot_bgcolor='#fff')

genderChart.update_traces(marker=dict(colors=color_gender), 
                     hoverinfo='label+percent',
                     selector=dict(type='pie'))

# RACE CHART
#FORMATING CHART
ran = race[['Label', sts]].rename(columns={sts:'usa'})
ran['usa'] = pd.to_numeric(ran['usa'])
ran['Label'] = ran['Label'].str.strip()

# PLOTLING
raceChart = px.funnel_area(values=ran['usa'],names=ran['Label'])

color_race = ['#004F74','#0072A7','#0092D6','#24B8FE','#5BCBFF']
#FORMATING CHART - RACE
raceChart.update_layout(showlegend=True,
              legend=dict(orientation='h'),
              margin=dict(l=0,r=0,b=0,t=0,pad=4), 
              paper_bgcolor='#fff',
              plot_bgcolor='#fff')

raceChart.update_traces(marker=dict(colors=color_race),
                         hovertemplate="%{label}<br>%{percent}")

# INCOME CHART
# Setting income
inc = income[['Label', sts]].rename(columns={sts:'usa'})
inc['usa'] = pd.to_numeric(inc['usa'])
inc = inc.drop(index=0)

# PLOTLING
incomeChart = go.Figure(data=[go.Bar(y=inc['Label'], 
	x=inc['usa'].loc[1:],orientation='h')])

#FORMATING CHART - INCOME
incomeChart.update_layout(showlegend=False,
                           bargap=0.5,
                           margin=dict(l=0,r=0,b=0,t=10,pad=4),
                           paper_bgcolor='#fff',
                           plot_bgcolor='#fff')
incomeChart.update_xaxes(visible=False)

incomeChart.update_traces(marker_color='#004f74', 
                           width=0.3,
                           hovertemplate="<extra>INCOME</extra> %{x}",
                           selector=dict(type='bar'))


# AGE CHART
# Setting the age
ages = age[['Label', sts]].rename(columns={sts:'usa'})
ages['usa'] = pd.to_numeric(ages['usa'])
ages['Label'] = ages['Label'].str.strip()

# PLOTLING
ageChart = go.Figure(data=[go.Bar(x=ages['Label'], y=ages['usa'])])

#FORMATING CHART - INCOME
ageChart.update_layout(bargap=0.5,
                        showlegend=False,
                        margin=dict(l=0,r=0,b=0,t=0,pad=4), 
                        paper_bgcolor='#fff',
                        plot_bgcolor='#fff')

ageChart.update_traces(marker_color='#004F74',
                        hovertemplate="<extra>AGE</extra> %{x}",
                        width=0.3,
                        selector=dict(type='bar'))



# MARITAL CHART
# Setting the marital
mar = marital[marital['state']==sts]

# PLOTLING
maritalChart = go.Figure(data=[go.Pie(labels=mar['status'], values=mar['percent'], hole=.8)])

color_marital = ['#004F74','#0072A7','#0092D6','#24B8FE','#5BCBFF']

#FORMATING CHART - GENDER
maritalChart.update_layout(showlegend=True,
                            legend=dict(orientation='h'),
                            margin=dict(l=0,r=0,b=0,t=0,pad=4), 
                            paper_bgcolor='#fff',
                            plot_bgcolor='#fff')

maritalChart.update_traces(marker=dict(colors=color_marital), 
                     hoverinfo='label+percent',
                     selector=dict(type='pie'))


# SCHOOL CHART
# Setting the school
scl = school[['Label', sts]].rename(columns={sts:'usa'})
scl['usa'] = pd.to_numeric(scl['usa'])
scl['Label'] = scl['Label'].str.strip()

# PLOTLING
schoolChart = px.funnel_area(names=scl['Label'], values=scl['usa'])

color_school = ['#004F74','#0072A7','#0092D6','#24B8FE','#5BCBFF']

#FORMATING CHART - RACE
schoolChart.update_layout(showlegend=True,
              legend=dict(orientation='h'),
              margin=dict(l=0,r=0,b=0,t=0,pad=4), 
              paper_bgcolor='#fff',
              plot_bgcolor='#fff')

schoolChart.update_traces(marker=dict(colors=color_school),
                           hovertemplate="%{label}<br>%{percent}")

# MAP CHART HERE
markers = []
for i in range(0,len(key)):
    if key.iloc[i]['latitude'] > 0:
    	markers.append(
	    	dl.Marker(title=key.iloc[i]['name_store'],
	    		position=(key.iloc[i]['latitude'], key.iloc[i]['longitude']),
	    		children=[
	    			dl.Tooltip([html.H5(key.iloc[i]['name_store']), html.H5(key.iloc[i]['name']), html.H5(f"Price: ${key.iloc[i]['price']}")])
	    		]
	    	)
	    )
cluster = dl.MarkerClusterGroup(id='markers', children=markers)

# PRICE TABLE
# Product range price (first 5)
pricing = key.sort_values(by=['price'], ascending=True)
pricing = pricing.loc[:,['name','name_store','price','inventory_price','abb_state']].copy()


# COMPETITORS
cating = key['category_2'].value_counts().index
cating = cating[0]


# FILTERING THE DATA
bells = base[base['category_2'].isin([cating])]

# REMOVING THE PRODUCT FROM THERE
cats = bells.drop(bells[bells['fullname'].isin([brand])].index, axis=0)

# Creating allcart rating based on price
mean = cats['price'].mean()
std = cats['price'].std()

# Creating allcart rating based on price
cats['price_diff'] = round(((cats['price']-mean)/std),2)

# Variables price
min_price = cats['price'].min()
mean_price = cats['price'].mean()
price = cats['price']
rating = cats['rating']
cats['allcart_rank'] = round((price/(price+min_price)*rating)+(min_price/(price+min_price)*mean_price),1)

# RANKING BY ALLCART_RANK
cats_order = cats.sort_values(by=['allcart_rank'], ascending=False)[:5]
cats_order = cats_order.reset_index(drop=True)


dash.register_page(__name__, name='PEPSI')
layout = html.Div(children=[
	html.Div(className='motherboard', children=[
		html.Div(className='child-side', children=[
			html.Div(className='child-child', style={'backgroundColor':'#A3E2FF'},  children=[
				html.Div(className='child-text', children=[
					html.H3("50%", style={'color':'#FFF', 'font-weight': '900', 'padding-bottom':'0.5rem'}),
					html.H5('PRODUCT USAGE', style={'color':'#FFF'})
				]),
				html.Div(className='child-icon', children=[
					ic(icon="carbon:user-favorite", width=90,
						style={'color':'#BFECFF'})
				])
			]),
			html.Div(className='child-child', style={'backgroundColor':'#5BCBFF'},  children=[
				html.Div(className='child-text', children=[
					html.H3("Back to the Future (1985)", style={'color':'#FFF', 'font-weight': '900', 'padding-bottom':'0.5rem'}),
					html.H5('MOVIE/SERIES MENTIONED IN', style={'color':'#FFF'})
				]),
				html.Div(className='child-icon', children=[
					ic(icon="bx:camera-movie", width=90,
						style={'color':'#BFECFF'})
				])
			]),
			html.Div(className='child-child', style={'backgroundColor':'#23B8FD'}, children=[
				html.Div(className='child-text', children=[
					html.H3("Beyounce", style={'color':'#FFF', 'font-weight': '900', 'padding-bottom':'0.5rem'}),
					html.H5('CELEBRITY USAGE', style={'color':'#FFF'})
				]),
				html.Div(className='child-icon', children=[
					ic(icon="fluent:person-star-20-regular", width=90,
						style={'color':'#BFECFF'})
				])
			]),
			html.Div(className='child-child', style={'backgroundColor':'#0092D6'},  children=[
				html.Div(className='child-text', children=[
					html.H3("50%", style={'color':'#FFF', 'font-weight': '900', 'padding-bottom':'0.5rem'}),
					html.H5('COMPETING PRODUCT USAGE', style={'color':'#FFF'})
				]),
				html.Div(className='child-icon', children=[
					ic(icon="carbon:user-data", width=90,
						style={'color':'#BFECFF'})
				])
			]),
			html.Div(className='child-child', style={'backgroundColor':'#0072A7'}, children=[
				html.Div(className='child-text', children=[
					html.H3("Texas", style={'color':'#FFF', 'font-weight': '900', 'padding-bottom':'0.5rem'}),
					html.H5('LOCATION COMPETITORS ARE SELLING MORE', style={'color':'#FFF'})
				]),
				html.Div(className='child-icon', children=[
					ic(icon="carbon:location-hazard", width=90,
						style={'color':'#BFECFF'})
				])
			]),
			html.Div(className='child-child', style={'backgroundColor':'#004F74'}, children=[
				html.Div(className='child-text', children=[
					html.H3("Coca-Cola", style={'color':'#FFF', 'font-weight': '900', 'padding-bottom':'0.5rem'}),
					html.H5('COMPETING PRODUCT CELEBRITY USAGE', style={'color':'#FFF'})
				]),
				html.Div(className='child-icon', children=[
					ic(icon="carbon:star-review", width=90,
						style={'color':'#BFECFF'})
				])
			])
		]),
		html.Div(className='child-main', children=[
			dmc.Breadcrumbs(children=[dcc.Link("Home", href="/"), dcc.Link("PUP", href="/"), dcc.Link("Pepsi", href="#")]),
			html.H3(className='dashboard', children=["DASHBOARD"]),
			html.Div(className='row-1', children=[
				html.Div(className="gender-div", children=[
					html.H4(className="chart-title", children=['Gender']),
					dcc.Graph(style={'height':'50vh','padding':'1rem'}, 
						figure=genderChart, 
						responsive=True)
				]),
				html.Div(className="race-div", children=[
					html.H4(className="chart-title", children=['Race']),
					dcc.Graph(style={'height':'50vh','padding':'1rem'}, 
						figure=raceChart, 
						responsive=True)
				]),
				html.Div(className="income-div", children=[
					html.H4(className="chart-title", children=['Income']),
					dcc.Graph(style={'height':'50vh','padding':'1rem'}, 
						figure=incomeChart, 
						responsive=True)
				])#
			]),
			html.Div(className='row-2', children=[
				html.Div(className="age-div", children=[
					html.H4(className="chart-title", children=['Age']),
					dcc.Graph(style={'height':'50vh','padding':'1rem'}, 
						figure=ageChart, 
						responsive=True)
				]),
				html.Div(className="marital-div", children=[
					html.H4(className="chart-title", children=['Marital Status']),
					dcc.Graph(style={'height':'50vh','padding':'1rem'}, 
						figure=maritalChart, 
						responsive=True)
				]),
				html.Div(className="school-div", children=[
					html.H4(className="chart-title", children=['Education']),
					dcc.Graph(style={'height':'50vh','padding':'1rem'}, 
						figure=schoolChart, 
						responsive=True)
				])
			])
		])
	]),
	html.Div(className="map-side", children=[
		html.Div(className='mapUSA', children=[
			html.H4(className="chart-title", children=['Sales per Location']),
			html.Div(style={'height':'70vh'}, children=[
				dl.Map([dl.TileLayer(),cluster], zoom=2, center=(38,-103))
			])
		]),
		html.Div(className="board-suntable", children=[
			html.Div(className='sales-menu-title', children=[
				html.H4(className="chart-title", children=['Price per State']),
				dmc.Select(data=[x for x in pricing['abb_state']], value='AL', 
					id='cont-pepsi',
					rightSection=[ic(icon="dashicons:arrow-down")])
			]),
			html.Div(className="chart-table", children=[
				html.Div(className="div-pie-chart", children=[
					dcc.Graph(style={'height':'30vh', 'width':'50%'}, id='priceChart-pepsi', responsive=True),
					dcc.Graph(style={'height':'30vh', 'width':'50%'}, id='storeChart-pepsi', responsive=True)
				]),
				html.Div(className='table-style', children=[
					dmc.Table(highlightOnHover=True,
						verticalSpacing='xs',
						id='tablePrice-pepsi')
				])
			])
		])
	]),
	html.Div(className='salesboard', children=[
		html.H4(className="chart-title", children=['Competitors']),
		html.Div(className='groups-win', children=[
			html.Div(className='groups-hidden', children=[
				html.Span(className='rank-titles', style={'font-weight':'900'}, children=["Place"]),
				html.Span(className='rank-titles', style={'font-weight':'900'}, children=['Product']),
				html.Span(className='rank-titles-num', style={'font-weight':'900'}, children=['Price']),
				html.Span(className='rank-titles', style={'font-weight':'900'}, children=['Store']),
				html.Span(className='rank-titles-num', style={'font-weight':'900'}, children=['Price Diff']),
				html.Span(className='rank-titles-num', style={'font-weight':'900'}, children=['Valuation'])
			]),
			html.Div(className='groups', children=[
				html.Span(className='rank-titles', children=["#1st Place"]),
				html.Span(className='rank-titles', children=[cats_order['lower_name'][0].title()]),
				html.Span(className='rank-titles-num', children=[f"${cats_order['price'][0]}"]),
				html.Span(className='rank-titles', children=[cats_order['name_store'][0].title()]),
				html.Span(className='rank-titles-num', children=[f"{cats_order['price_diff'][0]}%"]),
				html.Span(className='rank-titles-num', children=[cats_order['allcart_rank'][0]])
			]),
			html.Div(className='groups', children=[
				html.Span(className='rank-titles', children=["#2nd Place"]),
				html.Span(className='rank-titles', children=[cats_order['lower_name'][1].title()]),
				html.Span(className='rank-titles-num', children=[f"${cats_order['price'][1]}"]),
				html.Span(className='rank-titles', children=[cats_order['name_store'][1].title()]),
				html.Span(className='rank-titles-num', children=[f"{cats_order['price_diff'][1]}%"]),
				html.Span(className='rank-titles-num', children=[cats_order['allcart_rank'][1]])
			]),
			html.Div(className='groups', children=[
				html.Span(className='rank-titles', children=["#3rd Place"]),
				html.Span(className='rank-titles', children=[cats_order['lower_name'][2].title()]),
				html.Span(className='rank-titles-num', children=[f"${cats_order['price'][2]}"]),
				html.Span(className='rank-titles', children=[cats_order['name_store'][2].title()]),
				html.Span(className='rank-titles-num', children=[f"{cats_order['price_diff'][2]}%"]),
				html.Span(className='rank-titles-num', children=[cats_order['allcart_rank'][2]])
			]),
			html.Div(className='groups', children=[
				html.Span(className='rank-titles', children=["#4th Place"]),
				html.Span(className='rank-titles', children=[cats_order['lower_name'][3].title()]),
				html.Span(className='rank-titles-num', children=[f"${cats_order['price'][3]}"]),
				html.Span(className='rank-titles', children=[cats_order['name_store'][3].title()]),
				html.Span(className='rank-titles-num', children=[f"{cats_order['price_diff'][3]}%"]),
				html.Span(className='rank-titles-num', children=[cats_order['allcart_rank'][3]])
			]),
			html.Div(className='groups', children=[
				html.Span(className='rank-titles', children=["#5th Place"]),
				html.Span(className='rank-titles', children=[cats_order['lower_name'][4].title()]),
				html.Span(className='rank-titles-num', children=[f"${cats_order['price'][4]}"]),
				html.Span(className='rank-titles', children=[cats_order['name_store'][4].title()]),
				html.Span(className='rank-titles-num', children=[f"{cats_order['price_diff'][4]}%"]),
				html.Span(className='rank-titles-num', children=[cats_order['allcart_rank'][4]])
			])
		])
	]),
	html.Div(className="foot", children=[
		html.H6(className="rights", children=["Market Intent AI - 2022 .(c). All Rights Reserved."])
	])
])


@callback([Output('priceChart-pepsi','figure'),
	Output('storeChart-pepsi','figure'),
	Output('tablePrice-pepsi','children')],Input('cont-pepsi','value'))
def update_sunburst(value):
	delta = pricing[pricing['abb_state']==value]
	#price = px.sunburst(delta, path=['abb_state','price','name'])

	list_price=delta['price'].value_counts()

	price = go.Figure(data=[go.Pie(labels=list_price.index, 
		values=list_price.values, title='Price', hole=.8)])
	color_p = ['#004F74','#0072A7','#0092D6','#24B8FE','#5BCBFF']

	#FORMATING CHART
	price.update_layout(showlegend=False,
		margin=dict(l=0,r=0,b=0,t=0,pad=4), 
		paper_bgcolor='#fff',
		plot_bgcolor='#fff')

	price.update_traces(marker=dict(colors=color_p), 
                     hoverinfo='label+percent',
                     selector=dict(type='pie'))

	# 
	list_store=delta['name_store'].value_counts()
	color_s = ['#004F74','#0072A7','#0092D6','#24B8FE','#5BCBFF']
	store = go.Figure(data=[go.Pie(labels=list_store.index, 
		values=list_store.values, title='Store', hole=.8)])
	#FORMATING CHART
	store.update_layout(showlegend=False,
		margin=dict(l=0,r=0,b=0,t=0,pad=4), 
		paper_bgcolor='#fff',
		plot_bgcolor='#fff')

	store.update_traces(marker=dict(colors=color_p), 
                     hoverinfo='label+percent',
                     selector=dict(type='pie'))


	# TABLE PLOT
	tix = delta.loc[:,['name','price','inventory_price']].copy()
	tix = tix.rename(columns={'name': 'Product','price':'Price','inventory_price':'Inventory'})
	header = [html.Tr([html.Th(col) for col in tix.columns])]
	rows = [html.Tr([html.Td(cell) for cell in row]) for row in tix.values]
	table = [html.Thead(header), html.Tbody(rows)]
	return price,store,table

