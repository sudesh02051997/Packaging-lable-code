# Suppress logs during installation
!pip install reportlab PyPDF2 ipywidgets > /dev/null 2>&1

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import mm
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.graphics.barcode import code128
from PyPDF2 import PdfMerger
from google.colab import files
import os
import requests
from datetime import datetime

# ===============================================
#           ONLY FOR AMPLE STORE
# ===============================================

# Download the font from a URL
font_url = "https://drive.google.com/uc?id=1Y_RH0UhLtqyoMcWwV9kXFFQN_aICTKmp"
font_path = "/content/Poppins-Regular.ttf"

response = requests.get(font_url)
if response.status_code == 200:
    with open(font_path, "wb") as font_file:
        font_file.write(response.content)
else:
    raise Exception(f"Failed to download font. HTTP status code: {response.status_code}")

# Register the font
pdfmetrics.registerFont(TTFont("Poppins", font_path))

# Ensure Output Directory
output_dir = "/content/Output"
os.makedirs(output_dir, exist_ok=True)




def get_sku_details(sku, customer_type):
    last_two_digits = sku[-2:]

    if "H" in sku:
        mrp = "₹ 22999.00(Inclusive of all taxes)"
        weight = "1160g"

        if last_two_digits == "11":
            if customer_type == "Customer":
                box_contents = [
                    "In box contents with quantity: Headphone 1N, User Manual 1N,",
                    "Boom Mic 1N, USB Cable 1N, Card 1N, Travel Case 1N,",
                    "Quick Start Guide 1N, Jute bag 1N"
                ]
            else:  # Ample Store
                box_contents = [
                    "In box contents with quantity: Headphone 1N, User Manual 1N,",
                    "Boom Mic 1N, USB Cable 1N, Card 1N, Travel Case 1N,",
                    "Quick Start Guide 1N"
                ]
        elif last_two_digits == "10":
            if customer_type == "Customer":
                box_contents = [
                    "In box contents with quantity: Headphone 1N, User Manual 1N,",
                    "USB Cable 1N, Card 1N, Travel Case 1N, Quick Start Guide 1N,",
                    "Jute bag 1N"
                ]
            else:  # Ample Store
                box_contents = [
                    "In box contents with quantity: Headphone 1N, User Manual 1N,",
                    "USB Cable 1N, Card 1N, Travel Case 1N, Quick Start Guide 1N"
                ]
        elif last_two_digits == "01":
            if customer_type == "Customer":
                box_contents = [
                    "In box contents with quantity: Headphone 1N, User Manual 1N,",
                    "Boom Mic 1N, Card 1N, Travel Case 1N, Quick Start Guide 1N,",
                    "Jute bag 1N"
                ]
            else:  # Ample Store
                box_contents = [
                    "In box contents with quantity: Headphone 1N, User Manual 1N,",
                    "Boom Mic 1N, Card 1N, Travel Case 1N, Quick Start Guide 1N"
                ]
        elif last_two_digits == "00":
            if customer_type == "Customer":
                box_contents = [
                    "In box contents with quantity: Headphone 1N, User Manual 1N,",
                    "Card 1N, Travel Case 1N, Quick Start Guide 1N, Jute bag 1N"
                ]
            else:  # Ample Store
                box_contents = [
                    "In box contents with quantity: Headphone 1N, User Manual 1N,",
                    "Card 1N, Travel Case 1N, Quick Start Guide 1N"
                ]
        else:
            box_contents = ["Box contents information not available"]

    elif "J" in sku:
        mrp = "₹ 21999.00(Inclusive of all taxes)"
        weight = "975g"

        if last_two_digits == "11":
            box_contents = [
                "In box contents with quantity: Headphone 1N, User Manual 1N,",
                "Boom Mic 1N, USB Cable 1N, Card 1N, Jute bag 1N,",
                "Quick Start Guide 1N"
            ]
        elif last_two_digits == "10":
            box_contents = [
                "In box contents with quantity: Headphone 1N, User Manual 1N,",
                "USB Cable 1N, Card 1N, Jute bag 1N,","Quick Start Guide 1N"
            ]
        elif last_two_digits == "01":
            box_contents = [
                "In box contents with quantity: Headphone 1N, User Manual 1N,",
                "Boom Mic 1N, Card 1N, Jute bag 1N, Quick Start Guide 1N"
            ]
        elif last_two_digits == "00":
            box_contents = [
                "In box contents with quantity: Headphone 1N, User Manual 1N,",
                "Card 1N, Jute bag 1N, Quick Start Guide 1N"
            ]
        else:
            box_contents = ["Box contents information not available"]
    else:
        mrp = "UNKNOWN"
        weight = "UNKNOWN"
        box_contents = ["Box contents information not available"]

    return mrp, weight, box_contents




# Update the function call in create_label_pdf
def create_label_pdf(output_path, serial, mac, sku, customer_type):
    mrp, weight, box_contents = get_sku_details(sku, customer_type)

    # Rest of your PDF generation logic remains unchanged

    canvas_width, canvas_height = 100 * mm, 100 * mm
    pdf_canvas = canvas.Canvas(output_path, pagesize=(canvas_width, canvas_height))
    pdf_canvas.setFont("Poppins", 8)

    def from_top(y_distance):
        return canvas_height - y_distance


    # Determine the model number based on the serial number
    if "OB" in serial:
        model_number = "SL2310OB"
    elif "EG" in serial:
        model_number = "SL2300EG"
    elif "MW" in serial:
        model_number = "SL2300MW"
    else:
        model_number = "UNKNOWN"

    # Get the current month and year
    current_month_year = datetime.now().strftime("%m / %Y")  # e.g., "09 / 2025"



    # Add label content
    pdf_canvas.drawString(5 * mm, from_top(7 * mm), "Sonic lamb")
    pdf_canvas.drawString(5 * mm, from_top(11.7 * mm), f"Serial Number: {serial}")
    pdf_canvas.drawString(5 * mm, from_top(23.9 * mm), f"Model Name: {model_number}")
    pdf_canvas.drawString(5 * mm, from_top(36.1 * mm), f"SKU No: {sku}")
    pdf_canvas.drawString(5 * mm, from_top(48 * mm), f"MAC ID: {mac}")

    base_y = 48 * mm
    line_spacing = 4.7 * mm
    pdf_canvas.drawString(5 * mm, from_top(base_y + line_spacing), f"Month and Year of Manufacture: {current_month_year}")
    pdf_canvas.drawString(5 * mm, from_top(base_y + 2 * line_spacing), "FCC ID: 2AMWO-FSCBT1026")
    pdf_canvas.drawString(5 * mm, from_top(base_y + 3 * line_spacing), "IC ID: 23872-FSCBT1026")
    pdf_canvas.drawString(5 * mm, from_top(base_y + 4 * line_spacing), "JATE & TELC: R210-163280")
    pdf_canvas.drawString(5 * mm, from_top(base_y + 5 * line_spacing), "Customer Care: +91 90081 48509 | support@soniclamb.com")
    pdf_canvas.drawString(5 * mm, from_top(base_y + 6 * line_spacing), f"Maximum Retail Price: {mrp}")
    pdf_canvas.drawString(5 * mm, from_top(base_y + 7 * line_spacing), f"Weights: {weight}")
    # Add box contents
    for i, content in enumerate(box_contents):
        pdf_canvas.drawString(5 * mm, from_top(base_y + (8 + i) * line_spacing), content)

    # Generate and place the serial number barcode
    serial_barcode = code128.Code128(serial, barHeight=7 * mm, barWidth=0.25 * mm)
    serial_barcode.drawOn(pdf_canvas, 0 * mm, from_top(18 * mm) - 1.5 * mm)

    # Generate and place the model number barcode
    model_barcode = code128.Code128(model_number, barHeight=7 * mm, barWidth=0.25 * mm)
    model_barcode.drawOn(pdf_canvas, 0 * mm, from_top(30.5 * mm) - 1.5 * mm)

    # Generate and place the SKU barcode
    sku_barcode = code128.Code128(sku, barHeight=7 * mm, barWidth=0.25 * mm)
    sku_barcode.drawOn(pdf_canvas, 0 * mm, from_top(42.5 * mm) - 1.5 * mm)

    # Save the PDF
    pdf_canvas.save()


# Define a text area for input
from ipywidgets import widgets

# Customer selection dropdown
customer_dropdown = widgets.Dropdown(
    options=['', 'Customer', 'Ample Store'],
    value='',
    description='Select Customer Type:',
    style={'description_width': 'initial'},
    layout=widgets.Layout(width='300px')
)

# Add red border styling for empty selection
def update_dropdown_style(change):
    if change['new'] == '':
        customer_dropdown.style = {'description_width': 'initial', 'border': '2px solid red'}
    else:
        customer_dropdown.style = {'description_width': 'initial'}

customer_dropdown.observe(update_dropdown_style, names='value')

input_textarea = widgets.Textarea(
    value="",
    placeholder="Paste your data here (space-separated rows, e.g., Serial MAC SKU)",
    description="Input:",
    layout=widgets.Layout(width='100%', height='300px')  # Larger input area
)

# Define a button to trigger processing
process_button = widgets.Button(
    description="Generate Labels",
    button_style="success",  # 'success', 'info', 'warning', 'danger'
    tooltip="Click to process data and generate labels",
    icon="check"
)

# Display output message
output_label = widgets.Output()

# Processing function
def process_data(b):
    with output_label:
        output_label.clear_output()  # Clear previous output
        
        # Check if customer type is selected
        if customer_dropdown.value == '':
            print("❌ Please select Customer Type (Customer or Ample Store) before generating labels!")
            customer_dropdown.style = {'description_width': 'initial', 'border': '2px solid red'}
            return
        
        input_data = input_textarea.value.strip()  # Get user input
        if not input_data:
            print("No data entered. Please paste your data.")
            return

        # Parse input data
        rows = input_data.split("\n")  # Split rows by line
        parsed_data = [row.strip().split() for row in rows if len(row.strip().split()) == 3]

        if not parsed_data:
            print("No valid data provided. Please check your input format.")
            return

        # Generate PDFs and merge them
        merger = PdfMerger()
        individual_files = []
        serial_numbers = []  # To collect serial numbers for naming the merged file

        for serial, mac, sku in parsed_data:
            output_file = os.path.join(output_dir, f"{serial}.pdf")
            create_label_pdf(output_file, serial, mac, sku, customer_dropdown.value)
            merger.append(output_file)  # Add the file to the merger
            individual_files.append(output_file)
            serial_numbers.append(serial)  # Collect serial number

        # Create a name for the merged file using serial numbers
        merged_file_name = f"Merged_Labels_{customer_dropdown.value.replace(' ', '_')}_{'_'.join(serial_numbers)}.pdf"
        merged_file_path = os.path.join(output_dir, merged_file_name)

        # Save the merged PDF
        merger.write(merged_file_path)
        merger.close()

        # Trigger download of merged PDF only
        print(f"✅ Downloading the merged PDF: {merged_file_path}")
        print(f"📋 Customer Type: {customer_dropdown.value}")
        files.download(merged_file_path)

        # Clean up individual files to avoid clutter
        for file in individual_files:
            try:
                if os.path.exists(file):
                    os.remove(file)
            except Exception as e:
                print(f"Error deleting file {file}: {e}")

# Link the button to the function
process_button.on_click(process_data)

# Display the interface
display(customer_dropdown, input_textarea, process_button, output_label)
