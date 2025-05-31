
# Akasha GHG Emissions Calculator

_AkashaCalculator_ is a lightweight and adaptable tool developed for simplified greenhouse gas (GHG) emissions assessment within Environmental Impact Assessment (EIA) workflows. Created as part of a Master’s Dissertation at Técnico Lisboa, this tool targets contexts where advanced LCA software may be inaccessible or impractical, such as early-stage project development, small-scale projects, or regions with limited technical infrastructure.

---

## 🌍 Project Scope

This project was developed in the academic context of a Master’s Dissertation in Environmental Engineering. The main goal was to create a transparent, customizable tool that supports:

- GHG quantification during the **construction** and **operation** phases of infrastructure projects
- Data-limited environments, particularly for **developing regions** such as **Cabo Verde**
- Users with little or no programming experience

---

## 📁 Repository Structure

Below is a breakdown of all the key files and folders included in this repository:

### `Entity/`  
Contains the **Entity Classes** for each GHG emissions category. These classes represent individual data objects and define the structure for their attributes and emissions calculation methods.

- `energy_entity.py`  
- `vehicles_entity.py`  
- `materials_entity.py`  
- `combustion_entity.py`  
- `waste_entity.py`  
- `soil_entity.py`  
- `projectphases_entity.py`

Each class includes a `from_dict()` method for loading JSON input and methods to calculate GHG emissions from element-level data.

---

### `Services/`  
Contains the **Service Classes** responsible for higher-level calculations and aggregation:

- `Energy/energy_service.py`
- `Vehicles/vehicles_service.py`
- `Combustion/combustion_service.py`
- `Materials/materials_service.py`
- `Waste/waste_service.py`
- `Soil/soil_service.py`
- `ProjectPhases/projectphases_service.py`
- `TotalEmissions/totalemissions_service.py`

Each service uses its corresponding entity classes to compute emissions by phase, year, and category.

---

### `app.py`  
Central file that:

- Reads the Excel input file
- Creates the internal `.json` GHG database (`ghg_database.json`)
- Instantiates all service classes
- Calls plotting and calculation methods
- Provides the core logic that `interface.py` depends on

---

### `interface.py`  
The graphical user interface (GUI) was created using **PySimpleGUI**. Allows users to:

- Select Excel input file
- Choose emissions category
- Visualise numerical and graphic results
- Export emissions report as a PDF

---

### `requirements.txt`  
Lists all required Python packages to run the tool using the `.py` files:

```
pandas  
matplotlib  
PySimpleGUI
```

Install using:

```bash
pip install -r requirements.txt
```

---

### Input Templates & Case Study Files

- `database_akasha_template.xls`  
  Excel input template for creating your own database

- `database_akasha_PSPcasestudy.xls`  
  Full Excel input used to generate the AI-assisted case study database (PSP project)

- `APACalculator_PSPcasestudy.xls`  
  Excel file formatted for the **APA GHG calculator**, used to validate AkashaCalculator's results

- `GHG_Calculator_Input_Database_CaboVerde_AI_generated_database.xls`  
  Raw AI-generated data based on available project documentation and used to build the JSON database for testing

---

## 🛠️ How to Use

### ✅ Option 1: Using the Executable File - Only for Windows OS (Recommended for Non-Developers)

> 🔹 No Python installation required

1. Download `interface.exe` from the Releases tab.
2. Place `interface.exe` in the same folder as your Excel input file.
3. Run the `.exe` file.
4. Use the interface to upload the `.xls` input file.
5. Browse results or export them to a PDF.

---

### 💻 Option 2: Using the Python Scripts (Developers & Advanced Users)

> 🔹 Requires Python 3.8+ and dependencies listed in `requirements.txt`

1. Clone this repository.
2. Install the requirements:

```bash
pip install -r requirements.txt
```

3. Run the interface:

```bash
python interface.py
```

---

## 📦 Output

- **Numeric results**: GHG emissions by category and project phase
- **Graphical results**: Emissions evolution over time
- **PDF Report**: Exportable report including all visual and numeric data

---

## ⚠️ Known Limitations

- Only `.exe` for **Windows** is currently supported
- No built-in uncertainty or sensitivity analysis
- No breakdown of GHG by pollutant (CO₂, CH₄, N₂O only aggregated in CO₂eq)
- Does not support pre-construction or end-of-life emissions phases
- Manual input of emission factors required

---

## 🌱 Future Development Suggestions

- Drop-down menu for emission factors based on public datasets (IPCC, Ecoinvent)
- Dynamic uncertainty and sensitivity analysis
- Expansion to full project life cycle phases
- Interoperability with web platforms and planning software
- Linux/macOS executable support
- Improved GUI/UX for more intuitive navigation

---

## 🧠 Citation & Academic Use

This tool was created as part of a Master’s Dissertation at [Técnico Lisboa](https://tecnico.ulisboa.pt/). You may cite it as:

> AkashaCalculator. (2025). Lightweight Tool for GHG Emissions Estimation in Environmental Impact Assessment. Developed at Técnico Lisboa. [GitHub Repository Link]

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change or improve.

---

## 📃 License

MIT License – Free to use, modify, and distribute.

---

Thank you for your interest in the Akasha GHG Calculator! 💚  
Built to make sustainable impact assessments more accessible and adaptable.
