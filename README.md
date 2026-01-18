# Yay Bill Order Processor

This project contains both a Python script and a Vue3 web application for processing Yay bill order data.

## Project Structure

```
├── python/                    # Python scripts and data files
│   ├── yay_bill_processor.py  # Original Python script for processing orders
│   ├── 获取yay账单订单并输出.py  # Alternative Python script
│   ├── gui.py                # GUI implementation
│   ├── python_doc.py         # Python documentation
│   ├── py_demo.py            # Python demo
│   ├── gui.spec              # PyInstaller spec file
│   ├── 获取本机所有wifi密码.py   # Utility script
│   ├── 从浏览器复制出来拷贝到此.json # Sample JSON data
│   ├── 从浏览器复制出来拷贝到此.xlsx # Sample Excel data
│   ├── orders.xlsx           # Output Excel file
│   └── output.xlsx           # Output Excel file
├── src/                      # Vue3 source code
│   ├── App.vue               # Main Vue component
│   ├── main.js               # Vue application entry point
│   └── utils/                # Utility functions
│       └── dataProcessor.js  # Data processing utilities
├── public/                   # Public assets
│   └── index.html            # HTML template
├── package.json              # Node.js dependencies
├── vite.config.js            # Vite configuration
└── README.md                 # This file
```

## Python Script Features

- Reads JSON files containing order data
- Calculates total amounts
- Outputs data to Excel format
- Prints order statistics

## Vue3 Web Application Features

- Upload JSON files containing order data
- Parse and display order information in a table
- Calculate and display order statistics (total orders and total amount)
- Export processed data to Excel format
- Responsive UI with Element Plus components

## Functionality

Both implementations replicate the same core functionality:

1. Reads JSON data (expects either a `rows` property or an array of orders)
2. Calculates the total amount from the `totalBaseAmount` field
3. Displays order count and total amount
4. Exports data to Excel with a summary row

## Python Setup and Usage

```bash
cd python
python yay_bill_processor.py
```

## Vue3 Web Application Setup

```bash
npm install
npm run dev
```

### Compile and Minify for Production

```bash
npm run build
```

### Additional Notes

- The Vue3 application provides a web interface that replicates the Python script's functionality
- The upload component accepts JSON files and processes them without requiring server interaction
- Excel export is handled client-side using SheetJS library
- The UI is built with Element Plus components for a polished look and feel
