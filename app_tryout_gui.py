import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from fpdf import FPDF
import os

import app  # Your custom emissions and plot functions

# Categories
categories = ["All", "Energy", "Combustion Machinery", "Vehicles", "Materials", "Soil Use Change", "Waste Treatment"]

# PDF Export Function
def export_full_pdf(title, summary, figure_list, filename="akasha_ghg_full_report.pdf"):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, title, ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(0, 10, summary)
    for i, fig in enumerate(figure_list):
        image_name = f"temp_plot_{i}.png"
        fig.savefig(image_name)
        pdf.image(image_name, x=10, w=180)
        os.remove(image_name)
    pdf.output(filename)
    sg.popup("PDF exported successfully!", filename)

# Plot Drawing
def draw_figure(canvas, figure):
    if canvas.children:
        for child in canvas.winfo_children():
            child.destroy()
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

# Layout
layout = [
    [sg.Text("GHG Emission Calculator", font=('Helvetica', 16), justification='center', expand_x=True)],
    [sg.Text("Select Excel Input File:"), sg.Input(key="-FILE-"), sg.FileBrowse(file_types=(("Excel Files", "*.xlsx"),))],
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

# Window
window = sg.Window("GHG Emission Calculator Tool", layout, finalize=True, resizable=True)

latest_summary = ""
latest_figures = []
latest_figure = None
current_plot_index = 0

# Event Loop
while True:
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
