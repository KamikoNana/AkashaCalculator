'''
This file contains all necessary elements to run the GUI
More information can be found in the Akasha Guidebook avaliable in the GitHub repository
'''

import app

import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from fpdf import FPDF
import os
import pandas
import importlib 
import json


categories = ["All", "Energy", "Vehicles", "Combustion Machinery", "Materials", "Soil Use Change", "Waste Treatment"]

def export_full_pdf(title, summary, figure_list, filename="akasha_ghg_full_report.pdf"):
    '''
    Construction and export of a PDF report
    '''
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, title, ln=True)
    pdf.ln(10)

    # Section: Total
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Total Emissions Summary", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(0, 10, str(app.show_total() or ""))
    pdf.ln(5)
    total_fig = app.plot_total_peryear()
    img_path = "temp_total_plot.png"
    total_fig.savefig(img_path)
    pdf.image(img_path, x=10, w=180)
    os.remove(img_path)

    # Section: Energy
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Energy Emissions", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(0, 10, str(app.show_energy() or ""))
    energy_fig = app.plot_energy_peryear()
    img_path = "temp_energy_plot.png"
    energy_fig.savefig(img_path)
    pdf.image(img_path, x=10, w=180)
    os.remove(img_path)
    
    # Section: Vehicles
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Vehicles Emissions", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(0, 10, str(app.show_vehicles() or ""))
    for plot_func in [
        app.plot_vehicles_all_peryear,
        app.plot_vehicles_road_peryear,
        app.plot_vehicles_train_peryear,
        app.plot_vehicles_ship_peryear,
        app.plot_vehicles_air_peryear
    ]:
        fig = plot_func()
        img_path = f"temp_veh_plot_{plot_func.__name__}.png"
        fig.savefig(img_path)
        pdf.image(img_path, x=10, w=180)
        os.remove(img_path)

    # Section: Combustion Machinery
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Combustion Machinery Emissions", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(0, 10, str(app.show_combustionmachinery() or ""))
    for plot_func in [app.plot_fixedcomb_peryear, app.plot_mobilecomb_peryear]:
        fig = plot_func()
        img_path = f"temp_comb_plot_{plot_func.__name__}.png"
        fig.savefig(img_path)
        pdf.image(img_path, x=10, w=180)
        os.remove(img_path)

    # Section: Materials
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Materials Emissions", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(0, 10, str(app.show_materials() or ""))
    fig = app.plot_materialsprod_peryear()
    img_path = "temp_mat_plot.png"
    fig.savefig(img_path)
    pdf.image(img_path, x=10, w=180)
    os.remove(img_path)

    # Section: Soil Use Change
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Soil Use Change Emissions", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(0, 10, str(app.show_soilusechange() or ""))

    # Section: Waste Treatment
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Waste Treatment Emissions", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(0, 10, str(app.show_wastetreatment() or ""))
    for plot_func in [
        app.plot_waste_all_peryear,
        app.plot_waste_solids_peryear,
        app.plot_waste_water_peryear,
        app.plot_waste_gas_peryear
    ]:
        fig = plot_func()
        img_path = f"temp_waste_plot_{plot_func.__name__}.png"
        fig.savefig(img_path)
        pdf.image(img_path, x=10, w=180)
        os.remove(img_path)

    # Save PDF
    pdf.output(filename)
    sg.popup(
        "PDF exported successfully!", 
        filename, 
        "PDF saved in the same location as AkashaCalc.exe")

def draw_figure(canvas, figure):
    '''
    Display graph outputs
    '''
    if canvas.children:
        for child in canvas.winfo_children():
            child.destroy()
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

'''
Defining interface layout for each category
'''
layout = [
    [sg.Text("GHG Emission Calculator", font=('Helvetica', 16), justification='center', expand_x=True)],
    [sg.Text("Select Excel Input File:"), sg.Input(key="-FILE-"), sg.FileBrowse(file_types=(("Excel Files", "*.xlsx"),))],
    [sg.Text("Excel file selected should be named 'database_akasha' ")],
    [sg.Text("Select Emission Source:"), sg.Combo(categories, default_value="All", key="-CATEGORY-", readonly=True)],
    [sg.Text("Report Title:"), sg.Input("Akasha GHG Emissions Report", key="-TITLE-", size=(50, 1))],
    [
        sg.Button("Run Analysis", key="-RUN-"),
        sg.Button("Previous Plot", key="-PREV-"),
        sg.Button("Next Plot", key="-NEXT-"),
        sg.Button("Export PDF", key="-EXPORT-"),
        sg.Button("Exit")
    ],
    [sg.HorizontalSeparator()],
    [sg.Text("Results:", font=('Helvetica', 14))],
    [
        sg.Column([[sg.Multiline(size=(55, 20), key="-TEXT-", font=("Courier New", 10))]]),
        sg.Column([[sg.Canvas(key="-CANVAS-", size=(640, 480))]])
    ]
]

#Open GUI window
window = sg.Window("GHG Emission Calculator Tool", layout, finalize=True, resizable=True)

latest_summary = ""
latest_figures = []
latest_figure = None
current_plot_index = 0


while True:
    '''
    Loop to define the outputs to be displayed for each category
    '''
    event, values = window.read()

    if event == sg.WINDOW_CLOSED or event == "Exit":
        break

    elif event == "-RUN-":
        file_path = values["-FILE-"]
        selected_category = values["-CATEGORY-"]
        window["-TEXT-"].update("")

        if not os.path.exists(file_path):
            sg.popup_error("Please select a valid Excel file.")
            continue

        try:
            xls = pandas.ExcelFile(file_path)
            app.create_objects(xls, file_path) 
            app.create_database()
            
            app.init_calculations_services()
            
            summary_text = ""
            figures = []

            if selected_category == "All":
                summary_text += "Total GHG Emissions Summary:\n"
                summary_text += str(app.show_total() or "") + "\n"
                summary_text += "\n"
                summary_text += str(app.show_energy() or "") + "\n"
                summary_text += "\n"
                summary_text += str(app.show_vehicles() or "") + "\n"
                summary_text += "\n"
                summary_text += str(app.show_combustionmachinery() or "") + "\n"
                summary_text += "\n"
                summary_text += str(app.show_materials() or "") + "\n"
                summary_text += "\n"
                summary_text += str(app.show_soilusechange() or "") + "\n"
                summary_text += "\n"
                summary_text += str(app.show_wastetreatment() or "") + "\n"

                figures = [
                    app.plot_total_peryear(),
                    app.plot_energy_peryear(),
                    app.plot_vehicles_all_peryear(),
                    app.plot_fixedcomb_peryear(),
                    app.plot_mobilecomb_peryear(),
                    app.plot_materialsprod_peryear(),
                    app.plot_waste_all_peryear()
                ]

            elif selected_category == "Energy":
                summary_text = str(app.show_energy() or "") + "\n"
                figures = [app.plot_energy_peryear()]

            elif selected_category == "Combustion Machinery":
                summary_text = str(app.show_combustionmachinery() or "") + "\n"
                figures = [app.plot_fixedcomb_peryear(), app.plot_mobilecomb_peryear()]

            elif selected_category == "Vehicles":
                summary_text = str(app.show_vehicles() or "") + "\n"
                figures = [
                    app.plot_vehicles_all_peryear(),
                    app.plot_vehicles_road_peryear(),
                    app.plot_vehicles_train_peryear(),
                    app.plot_vehicles_ship_peryear(),
                    app.plot_vehicles_air_peryear()
                ]

            elif selected_category == "Materials":
                summary_text = str(app.show_materials() or "") + "\n"
                figures = [app.plot_materialsprod_peryear()]

            elif selected_category == "Soil Use Change":
                summary_text = str(app.show_soilusechange() or "") + "\n"
                figures = []

            elif selected_category == "Waste Treatment":
                summary_text = str(app.show_wastetreatment() or "") + "\n"
                figures = [
                    app.plot_waste_all_peryear(),
                    app.plot_waste_solids_peryear(),
                    app.plot_waste_water_peryear(),
                    app.plot_waste_gas_peryear()
                ]

            latest_summary = summary_text
            latest_figures = figures
            latest_figure = figures[0] if figures else None
            current_plot_index = 0

            window["-TEXT-"].update(latest_summary)
            if latest_figure:
                draw_figure(window["-CANVAS-"].TKCanvas, latest_figure)

        except Exception as e:
            sg.popup_error("Error during processing:", str(e))

    elif event == "-NEXT-":
        if latest_figures and current_plot_index < len(latest_figures) - 1:
            current_plot_index += 1
            latest_figure = latest_figures[current_plot_index]
            draw_figure(window["-CANVAS-"].TKCanvas, latest_figure)

    elif event == "-PREV-":
        if latest_figures and current_plot_index > 0:
            current_plot_index -= 1
            latest_figure = latest_figures[current_plot_index]
            draw_figure(window["-CANVAS-"].TKCanvas, latest_figure)

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

