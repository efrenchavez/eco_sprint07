"""Entry point for the StreamLit app"""
import plotly.express as px
import streamlit as st
import utils.management as aux


# load the data
data = aux.load_clean_data_into_main()

# GUI stuff
# radio button
radio_button_title = 'Select chart type to create'
radio_button_names = ['Histogram', 'Scatter plot', 'Donut chart']
radio_button_captions = ['Odometer readings',
                         'Price vs Odometer correlation', 'Most common fuel type']

# button
button_legend = 'Chart data'

# checkbox
checkbox_legend = 'Orange?'

# write header and description
st.header('Sprint 07 Project - Dummy Data App')
st.write('This app fulfills the requirement of Sprint 07 project:')
st.write("""
- At least one header with text.
- At least one histogram.
- At least one scatter plot.
- At least one button OR checkbox.
""")
# streamlit radio menu
chart_type = st.radio(radio_button_title, radio_button_names,
                      captions=radio_button_captions, index=None)
# streamlit checkbox
orange = st.checkbox(checkbox_legend)
# streamlit button
chart_button = st.button(button_legend)


# when button is pressed
if chart_button:
    # check for radio button
    if chart_type is None:
        st.write('No chart type selected, choose from radio menu.')
    elif chart_type is radio_button_names[0]:
        hist_odometer = px.histogram(data, x='odometer',
                                     labels={
                                         'odometer': 'Odometer reading (total distance traveled) in millions of miles*'},
                                     title='<b>How long a distance do our vehicles travel?</b>')
        hist_odometer.update_traces(
            marker_color=('orange' if orange else 'teal'))
        st.plotly_chart(hist_odometer, width='stretch')
    elif chart_type is radio_button_names[1]:
        scatter_price_vs_odometer = px.scatter(data, x='odometer', y='price',
                                               labels={'odometer': 'Odometer reading (total distance traveled) in millions of miles',
                                                       'price': 'Price in USD'},
                                               title='<b>Does heavy use depreciate vehicles?</b>')
        scatter_price_vs_odometer.update_traces(
            marker_color=('orange' if orange else 'teal'))
        st.plotly_chart(scatter_price_vs_odometer, width='stretch')
    elif chart_type is radio_button_names[2]:
        donut_data = data.groupby('fuel', observed=True)['cylinders'].count(
        ).reset_index().rename(columns={'cylinders': 'unit_count'})
        donut_fuel = px.pie(donut_data, values='unit_count', names='fuel', hole=0.4,
                            title='<b>Which fuel types are more common among the vehicles we sell?</b>',
                            color_discrete_sequence=(['orange'] if orange else ['teal']))
        st.plotly_chart(donut_fuel, width='stretch')
