import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from fpdf import FPDF
import os

import app

categories = ["All", "Energy", "Combustion Machinery", "Vehicles", "Materials", "Soil Use Change", "Waste Treatment"]

'''''
def export_full_pdf(title, summary, figure_list, filename="akasha_ghg_full_report.pdf"):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Calibri", 'B', 14)
    pdf.cell(0, 10, title, ln=True)
    
    title = "AkashaCalc GHG Emissions Report"

    pdf.set_font("Calibri", '', 12)
    pdf.multi_cell(0, 10, summary)

    summary_text = "Total GHG Emissions Summary:", app.show_total()

    figures = [
        app.plot_energy_peryear(),
        app.plot_fixedcomb_peryear(),
        app.plot_mobilecomb_peryear(),
        app.plot_materialsprod_peryear(),
        app.plot_vehicles_all_peryear(),
        app.plot_vehicles_road_peryear(),
        app.plot_vehicles_train_peryear(),
        app.plot_vehicles_ship_peryear(),
        app.plot_vehicles_air_peryear(),
        app.plot_waste_all_peryear(),
        app.plot_waste_solids_peryear(),
        app.plot_waste_water_peryear(),
        app.plot_waste_gas_peryear()
    ]
    
    for i, fig in enumerate(figure_list):
        image_name = f"temp_plot_{i}.png"
        fig.savefig(image_name)
        pdf.image(image_name, x=10, w=180)
        os.remove(image_name)

    pdf.output(filename)
    sg.popup("PDF exported successfully!", filename)

'''''


def draw_figure(canvas, figure):
    if canvas.children:
        for child in canvas.winfo_children():
            child.destroy()
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

layout = [
    [sg.Text("GHG Emission Calculator", font=('Helvetica', 16), justification='center', expand_x=True)],
    [sg.Text("Select Excel Input File:"), sg.Input(key="-FILE-"), sg.FileBrowse(file_types=(("Excel Files", "*.xlsx"),))],
    [sg.Text("Select Emission Source:"), sg.Combo(categories, default_value="All", key="-CATEGORY-", readonly=True)],
    [sg.Text("Report Title:"), sg.Input("Akasha GHG Emissions Report", key="-TITLE-", size=(50, 1))],
    [sg.Button("Run Analysis", key="-RUN-"), sg.Button("Export PDF", key="-EXPORT-"), sg.Button("Exit")],
    [sg.HorizontalSeparator()],
    [sg.Text("Results:", font=('Helvetica', 14))],
    [sg.Output(size=(100, 10), key='-OUTPUT-')],
    [sg.Canvas(key='-CANVAS-')]
]

window = sg.Window("GHG Emission Calculator Tool", layout, finalize=True, resizable=True)

latest_summary = ""
latest_figures = []
latest_figure = None

while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED or event == "Exit":
        break

    elif event == "-RUN-":
        file_path = values["-FILE-"]
        selected_category = values["-CATEGORY-"]
        window['-OUTPUT-'].update("")

        if not os.path.exists(file_path):
            sg.popup_error("Please select a valid Excel file.")
            continue

#categories = ["All", "Energy", "Combustion Machinery", "Vehicles", "Materials", "Soil Use Change", "Waste Treatment"]

        try:
            if selected_category == "All":
                print("Running full emissions analysis...")

                summary_text = "Total GHG Emissions Summary:"
                summary_text += app.show_total()
                summary_text += "- Energy:"
                summary_text += app.show_energy()
                summary_text += "- Vehicles:"
                summary_text += app.show_vehicles()
                summary_text += "- Combustion Machinery"
                summary_text += app.show_combustionmachinery()
                summary_text += "- Materials:"
                summary_text += app.show_materials()
                summary_text += "- Soil Use Change:"
                summary_text += app.show_soilusechange()
                summary_text += "- Waste Treatment:"
                summary_text += app.show_wastetreatment()

                latest_summary = summary_text
                print(latest_summary)

                figures = []
                
                fig1 = app.plot_energy_peryear()
                figures.append(fig1)
                fig2 = app.plot_vehicles_all_peryear()
                figures.append(fig2)
                fig3 = app.plot_fixedcomb_peryear()
                figures.append(fig3)
                fig4 = app.plot_mobilecomb_peryear()
                figures.append(fig4)
                fig5 = app.plot_materialsprod_peryear()
                figures.append(fig5)
                fig6 = app.plot_waste_all_peryear()
                figures.append(fig6)

                latest_figures = figures
                draw_figure(window['-CANVAS-'].TKCanvas, latest_figure)

            elif selected_category == "Energy":
                print(f"Running partial analysis for: {selected_category}")

                summary_text = "Total Energy GHG Emissions Summary:"
                summary_text += app.show_energy()

                latest_summary = summary_text
                print(latest_summary)

                figures = []
                
                fig1 = app.plot_energy_peryear()
                figures.append(fig1)

                latest_figures = figures
                draw_figure(window['-CANVAS-'].TKCanvas, latest_figure)
                
            elif selected_category == "Combustion Machinery":
                print(f"Running partial analysis for: {selected_category}")

                summary_text = "Total Combustion Machinery GHG Emissions Summary:"
                summary_text += app.show_combustionmachinery()

                latest_summary = summary_text
                print(latest_summary)

                figures = []

                fig3 = app.plot_fixedcomb_peryear()
                figures.append(fig3)
                fig4 = app.plot_mobilecomb_peryear()
                figures.append(fig4)

                latest_figures = figures
                draw_figure(window['-CANVAS-'].TKCanvas, latest_figure)
                
            elif selected_category == "Vehicles":
                print(f"Running partial analysis for: {selected_category}")
                
                summary_text = "Total Vehicles GHG Emissions Summary:"
                summary_text += app.show_vehicles()

                latest_summary = summary_text
                print(latest_summary)

                figures = []
                
                fig1 = app.plot_energy_peryear()
                figures.append(fig1)
                fig2 = app.plot_vehicles_all_peryear()
                figures.append(fig2)
                fig3 = app.plot_fixedcomb_peryear()
                figures.append(fig3)
                fig4 = app.plot_mobilecomb_peryear()
                figures.append(fig4)
                fig5 = app.plot_materialsprod_peryear()
                figures.append(fig5)
                fig6 = app.plot_waste_all_peryear()
                figures.append(fig6)

                latest_figures = figures
                draw_figure(window['-CANVAS-'].TKCanvas, latest_figure)

        except Exception as e:
            sg.popup_error("Error during processing:", str(e))

    elif event == "-EXPORT-":
        if values["-CATEGORY-"] != "All":
            sg.popup_error("PDF export is only available when 'All' is selected.")
            continue

        if not latest_figures:
            sg.popup_error("Please run the analysis first.")
            continue

        report_title = values["-TITLE-"] or "GHG Emissions Report"
        export_full_pdf(report_title, latest_summary, latest_figures)

window.close()
