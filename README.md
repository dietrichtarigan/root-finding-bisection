# Bisection Method Root Finder Application

A comprehensive application for finding roots of the function f(x) = x³ - x² - 4x using the bisection method. This project demonstrates proper separation of concerns by separating core algorithms from GUI and additional features.

## Function Analysis

**Target Function**: f(x) = x³ - x² - 4x

**Factored Form**: f(x) = x(x² - x - 4)

**Three Roots**:
- Root 1 (negative): x₁ = (1 - √17)/2 ≈ -1.5615528
- Root 2 (zero): x₂ = 0 (exactly)
- Root 3 (positive): x₃ = (1 + √17)/2 ≈ 2.5615528

## Project Structure

```
code-metode-komputasi/
├── bisection_core.py           # Core bisection method algorithms
├── function_plotter.py         # Function visualization utilities
├── root_finder_gui.py          # Main GUI application (no emojis)
├── excel_generator.py          # Excel manual calculation generator
├── workflow_app.py             # Comprehensive workflow demonstration
├── root-finding-bisection.py   # Original GUI (with emojis)
├── README.md                   # This documentation file
└── pdf/
    └── Chapter-1-False-Position-Method.pdf
```

## File Descriptions

### Core Algorithm (`bisection_core.py`)
- **Purpose**: Contains pure bisection method algorithm separated from GUI
- **Key Functions**:
  - `target_function(x)`: Evaluates f(x) = x³ - x² - 4x
  - `bisection_method()`: Core bisection algorithm
  - `find_all_roots_target_function()`: Finds all three roots automatically
  - `format_iteration_table()`: Formats results for display

### Function Plotter (`function_plotter.py`)
- **Purpose**: Visualization utilities for understanding the function
- **Features**:
  - Plot function with root regions highlighted
  - Interactive function explorer
  - Detailed analysis and reporting
  - Save plots and analysis reports

### GUI Application (`root_finder_gui.py`)
- **Purpose**: Clean GUI without emojis, integrated with core algorithms
- **Features**:
  - Three tabs: Single Root, All Roots, Function Info
  - Pre-defined interval buttons for each root
  - Comprehensive results display
  - Interactive visualizations
  - Uses separated core algorithms

### Excel Generator (`excel_generator.py`)
- **Purpose**: Creates Excel files for manual calculation practice
- **Outputs**:
  - Individual Excel files for each root
  - Step-by-step calculation tables
  - Comprehensive learning guide
  - Manual calculation templates

### Workflow Application (`workflow_app.py`)
- **Purpose**: Demonstrates complete root-finding workflow
- **Steps**:
  1. Function analysis and plotting
  2. Interval determination
  3. Root calculation using bisection method
  4. Results verification against exact values
  5. Excel manual calculation generation

## Installation Requirements

```bash
# Core requirements
pip install numpy matplotlib plotly pandas openpyxl

# For GUI
pip install tkinter  # Usually included with Python

# Optional for enhanced plotting
pip install seaborn
```

## Usage Instructions

### 1. Quick Start - GUI Application
```bash
python root_finder_gui.py
```
- Use the "Single Root" tab to find one root at a time
- Use the "All Roots" tab to find all three roots automatically
- Check "Function Info" tab for mathematical background

### 2. Complete Workflow Demonstration
```bash
# Interactive mode
python workflow_app.py

# Automatic complete workflow
python workflow_app.py --auto
```

### 3. Function Analysis and Plotting
```bash
python function_plotter.py
```
This will:
- Analyze the function mathematically
- Create plots showing all three roots
- Generate analysis report
- Optionally start interactive explorer

### 4. Generate Excel Manual Calculations
```bash
python excel_generator.py
```
Creates Excel files with step-by-step manual calculations for educational purposes.

### 5. Test Core Algorithms
```bash
python bisection_core.py
```
Tests the core bisection method algorithms and displays results.

## Recommended Learning Workflow

1. **Start with Function Analysis**:
   ```bash
   python function_plotter.py
   ```
   This helps you understand where the roots are located.

2. **Try the Complete Workflow**:
   ```bash
   python workflow_app.py --auto
   ```
   This demonstrates the entire process from analysis to final results.

3. **Practice with GUI**:
   ```bash
   python root_finder_gui.py
   ```
   Use different intervals and settings to understand the method.

4. **Study Manual Calculations**:
   ```bash
   python excel_generator.py
   ```
   Open the generated Excel files to see step-by-step calculations.

## Root Finding Intervals

Based on function analysis, use these intervals for best results:

| Root | Interval | Description |
|------|----------|-------------|
| Root 1 | [-2, -1] | Negative root |
| Root 2 | [-0.5, 0.5] | Zero root |
| Root 3 | [2, 3] | Positive root |

## Key Learning Points

1. **Function Bracketing**: Understand why f(a) × f(b) < 0 is required
2. **Convergence**: Learn about tolerance settings and iteration limits
3. **Error Analysis**: See how error decreases with each iteration
4. **Manual Calculation**: Practice the method by hand using Excel guides

## Features Highlights

### ✅ Separation of Concerns
- Core algorithms separated from GUI
- Modular design for easy maintenance
- Reusable components

### ✅ Educational Value
- Step-by-step Excel calculations
- Function analysis and visualization
- Interactive learning tools

### ✅ No AI Emojis
- Clean, professional interface
- Focus on mathematical content
- Academic-appropriate presentation

### ✅ Comprehensive Workflow
- Complete process demonstration
- Multiple ways to use the application
- Suitable for different learning styles

## Output Files

When you run the applications, various files will be created:

**Plots**:
- `target_function_plot.png` - Main function visualization
- `workflow_function_plot.png` - Workflow demonstration plot

**Excel Files**:
- `bisection_manual_Root_1_Negative.xlsx`
- `bisection_manual_Root_2_Zero.xlsx`
- `bisection_manual_Root_3_Positive.xlsx`
- `bisection_comprehensive_guide.xlsx`

**Analysis**:
- `function_analysis_report.txt` - Detailed mathematical analysis

## Mathematical Background

The function f(x) = x³ - x² - 4x can be factored as:

f(x) = x(x² - x - 4)

This gives us:
- One obvious root at x = 0
- Two additional roots from x² - x - 4 = 0

Using the quadratic formula:
x = (1 ± √17)/2

Therefore:
- x₁ = (1 - √17)/2 ≈ -1.5615528128088303
- x₂ = 0
- x₃ = (1 + √17)/2 ≈ 2.5615528128088303

## Troubleshooting

### Common Issues:

1. **Import Errors**: Make sure all required packages are installed
2. **Plot Not Showing**: Check matplotlib backend settings
3. **Excel Files Not Created**: Install openpyxl and pandas
4. **GUI Not Opening**: Ensure tkinter is available

### Solutions:

```bash
# Install missing packages
pip install matplotlib plotly pandas openpyxl numpy

# For Linux users who might need tkinter
sudo apt-get install python3-tk
```

## Contributing

This is an educational project demonstrating bisection method implementation. Feel free to:
- Add more functions to analyze
- Improve visualization features
- Enhance the Excel templates
- Add more numerical methods

## License

Educational use. Suitable for academic purposes and learning numerical methods.
