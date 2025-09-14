import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.offline as pyo
import webbrowser
import tempfile
import os
import math

# Import our core algorithm module
from core_algorithm import (
    target_function, 
    bisection_method, 
    find_all_roots_target_function,
    format_iteration_table,
    format_results
)


class BisectionMethodGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Bisection Method Root Finder - f(x) = x³ - x² - 4x")
        self.root.geometry("900x800")
        self.root.configure(bg='#2c3e50')
        
        # Style configuration
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TLabel', background='#2c3e50', foreground='white', font=('Arial', 10))
        style.configure('TButton', font=('Arial', 10, 'bold'))
        style.configure('TEntry', fieldbackground='#ecf0f1', font=('Arial', 10))
        
        self.setup_ui()
        self.current_result = None
        
    def setup_ui(self):
        # Main title
        title_label = tk.Label(
            self.root, 
            text="Bisection Method Root Finder", 
            font=('Arial', 16, 'bold'), 
            bg='#2c3e50', 
            fg='#e74c3c'
        )
        title_label.pack(pady=10)
        
        subtitle_label = tk.Label(
            self.root, 
            text="Target Function: f(x) = x³ - x² - 4x", 
            font=('Arial', 12), 
            bg='#2c3e50', 
            fg='#ecf0f1'
        )
        subtitle_label.pack(pady=5)
        
        # Main frame
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Create notebook for tabs
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill='both', expand=True)
        
        # Tab 1: Single Root Finding
        self.single_root_tab(notebook)
        
        # Tab 2: All Roots Finding
        self.all_roots_tab(notebook)
        
        # Tab 3: Function Information
        self.function_info_tab(notebook)
        
    def single_root_tab(self, notebook):
        """Create tab for finding a single root"""
        single_frame = tk.Frame(notebook, bg='#2c3e50')
        notebook.add(single_frame, text="Single Root")
        
        # Input section
        input_frame = tk.LabelFrame(
            single_frame, 
            text="Input Parameters", 
            bg='#34495e', 
            fg='white', 
            font=('Arial', 12, 'bold')
        )
        input_frame.pack(fill='x', pady=5, padx=5)
        
        # Function display (read-only)
        tk.Label(input_frame, text="Function:", bg='#34495e', fg='white').grid(
            row=0, column=0, sticky='w', padx=5, pady=5
        )
        function_display = tk.Label(
            input_frame, 
            text="f(x) = x³ - x² - 4x", 
            bg='#ecf0f1', 
            fg='#2c3e50',
            font=('Arial', 10, 'bold'),
            relief='sunken',
            bd=1
        )
        function_display.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        
        # Interval inputs
        tk.Label(input_frame, text="Interval [a, b]:", bg='#34495e', fg='white').grid(
            row=1, column=0, sticky='w', padx=5, pady=5
        )
        interval_frame = tk.Frame(input_frame, bg='#34495e')
        interval_frame.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        
        self.a_entry = tk.Entry(interval_frame, width=10, font=('Arial', 10))
        self.a_entry.insert(0, "-2")
        self.a_entry.pack(side='left')
        
        tk.Label(interval_frame, text=" to ", bg='#34495e', fg='white').pack(side='left')
        
        self.b_entry = tk.Entry(interval_frame, width=10, font=('Arial', 10))
        self.b_entry.insert(0, "-1")
        self.b_entry.pack(side='left')
        
        # Preset interval buttons
        preset_frame = tk.Frame(input_frame, bg='#34495e')
        preset_frame.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        
        tk.Label(input_frame, text="Quick intervals:", bg='#34495e', fg='white').grid(
            row=2, column=0, sticky='w', padx=5, pady=5
        )
        
        preset_intervals = [
            ("Root 1: [-2, -1]", -2, -1),
            ("Root 2: [-0.5, 0.5]", -0.5, 0.5),
            ("Root 3: [2, 3]", 2, 3)
        ]
        
        for text, a, b in preset_intervals:
            btn = tk.Button(
                preset_frame, 
                text=text, 
                command=lambda a=a, b=b: self.set_interval(a, b),
                bg='#95a5a6',
                fg='white',
                font=('Arial', 8)
            )
            btn.pack(side='left', padx=2)
        
        # Tolerance and max iterations
        tk.Label(input_frame, text="Tolerance:", bg='#34495e', fg='white').grid(
            row=3, column=0, sticky='w', padx=5, pady=5
        )
        self.tolerance_entry = tk.Entry(input_frame, width=15, font=('Arial', 10))
        self.tolerance_entry.insert(0, "1e-10")
        self.tolerance_entry.grid(row=3, column=1, sticky='w', padx=5, pady=5)
        
        tk.Label(input_frame, text="Max Iterations:", bg='#34495e', fg='white').grid(
            row=4, column=0, sticky='w', padx=5, pady=5
        )
        self.max_iter_entry = tk.Entry(input_frame, width=15, font=('Arial', 10))
        self.max_iter_entry.insert(0, "100")
        self.max_iter_entry.grid(row=4, column=1, sticky='w', padx=5, pady=5)
        
        # Buttons
        button_frame = tk.Frame(input_frame, bg='#34495e')
        button_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        self.solve_button = tk.Button(
            button_frame, 
            text="Find Root", 
            command=self.find_single_root,
            bg='#27ae60', 
            fg='white', 
            font=('Arial', 11, 'bold'),
            relief='raised', 
            bd=3
        )
        self.solve_button.pack(side='left', padx=5)
        
        self.visualize_button = tk.Button(
            button_frame, 
            text="Visualize", 
            command=self.visualize_single,
            bg='#3498db', 
            fg='white', 
            font=('Arial', 11, 'bold'),
            relief='raised', 
            bd=3
        )
        self.visualize_button.pack(side='left', padx=5)
        
        self.clear_button = tk.Button(
            button_frame, 
            text="Clear", 
            command=self.clear_single,
            bg='#e74c3c', 
            fg='white', 
            font=('Arial', 11, 'bold'),
            relief='raised', 
            bd=3
        )
        self.clear_button.pack(side='left', padx=5)
        
        # Results section
        results_frame = tk.LabelFrame(
            single_frame, 
            text="Results", 
            bg='#34495e', 
            fg='white', 
            font=('Arial', 12, 'bold')
        )
        results_frame.pack(fill='both', expand=True, pady=5, padx=5)
        
        # Result display
        self.single_result_text = scrolledtext.ScrolledText(
            results_frame, 
            height=15, 
            width=90,
            bg='#ecf0f1', 
            fg='#2c3e50', 
            font=('Consolas', 9)
        )
        self.single_result_text.pack(fill='both', expand=True, padx=5, pady=5)
        
    def all_roots_tab(self, notebook):
        """Create tab for finding all roots"""
        all_frame = tk.Frame(notebook, bg='#2c3e50')
        notebook.add(all_frame, text="All Roots")
        
        # Info section
        info_frame = tk.LabelFrame(
            all_frame, 
            text="Information", 
            bg='#34495e', 
            fg='white', 
            font=('Arial', 12, 'bold')
        )
        info_frame.pack(fill='x', pady=5, padx=5)
        
        info_text = """
Function: f(x) = x³ - x² - 4x = x(x² - x - 4)
This function has three roots:
• Root 1 (negative): approximately between -2 and -1
• Root 2 (zero): exactly at x = 0  
• Root 3 (positive): approximately between 2 and 3
        """
        
        tk.Label(
            info_frame, 
            text=info_text.strip(), 
            bg='#34495e', 
            fg='white',
            justify='left',
            font=('Arial', 10)
        ).pack(padx=10, pady=10)
        
        # Button to find all roots
        find_all_button = tk.Button(
            info_frame,
            text="Find All Three Roots",
            command=self.find_all_roots,
            bg='#8e44ad',
            fg='white',
            font=('Arial', 12, 'bold'),
            relief='raised',
            bd=3
        )
        find_all_button.pack(pady=10)
        
        # Results section
        results_frame = tk.LabelFrame(
            all_frame, 
            text="All Roots Results", 
            bg='#34495e', 
            fg='white', 
            font=('Arial', 12, 'bold')
        )
        results_frame.pack(fill='both', expand=True, pady=5, padx=5)
        
        # Result display
        self.all_result_text = scrolledtext.ScrolledText(
            results_frame, 
            height=20, 
            width=90,
            bg='#ecf0f1', 
            fg='#2c3e50', 
            font=('Consolas', 9)
        )
        self.all_result_text.pack(fill='both', expand=True, padx=5, pady=5)
        
    def function_info_tab(self, notebook):
        """Create tab with function information"""
        info_frame = tk.Frame(notebook, bg='#2c3e50')
        notebook.add(info_frame, text="Function Info")
        
        # Create scrollable text with function information
        info_text_widget = scrolledtext.ScrolledText(
            info_frame,
            bg='#ecf0f1',
            fg='#2c3e50',
            font=('Consolas', 10),
            wrap=tk.WORD
        )
        info_text_widget.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Function information content
        info_content = """
FUNCTION ANALYSIS: f(x) = x³ - x² - 4x
================================================

MATHEMATICAL PROPERTIES:
• Cubic polynomial function
• Factored form: f(x) = x(x² - x - 4)
• Degree: 3 (odd degree means function goes from -∞ to +∞)
• Leading coefficient: 1 (positive, so function increases for large x)

ROOTS ANALYSIS:
1. Obvious root: x = 0 (from factor x)
2. Quadratic factor: x² - x - 4 = 0
   Using quadratic formula: x = (1 ± √17)/2
   
   Root 1: x₁ = (1 - √17)/2 ≈ -1.561553 (negative)
   Root 3: x₃ = (1 + √17)/2 ≈ 2.561553 (positive)

EXACT ROOT VALUES:
• Root 1: x₁ = (1 - √17)/2 ≈ -1.5615528128088303
• Root 2: x₂ = 0 (exactly)
• Root 3: x₃ = (1 + √17)/2 ≈ 2.5615528128088303

RECOMMENDED INTERVALS FOR BISECTION METHOD:
• Root 1: [-2, -1] or [-2, -1.5]
• Root 2: [-0.5, 0.5] or [-1, 1]  
• Root 3: [2, 3] or [2.5, 3]

FUNCTION BEHAVIOR:
• f(-∞) = -∞ (negative for very negative x)
• f(+∞) = +∞ (positive for very positive x)
• Has local extrema (maxima/minima) between roots

DERIVATIVE: f'(x) = 3x² - 2x - 4
Critical points where f'(x) = 0:
x = (2 ± √52)/6 = (1 ± √13)/3

Local maximum at x ≈ -0.869
Local minimum at x ≈ 1.536

SIGN ANALYSIS:
x < -1.56: f(x) < 0 (negative)
-1.56 < x < 0: f(x) > 0 (positive)  
0 < x < 2.56: f(x) < 0 (negative)
x > 2.56: f(x) > 0 (positive)

This sign pattern confirms the three roots and shows where
the function is positive or negative, which is crucial for
setting up proper intervals for the bisection method.
"""
        
        info_text_widget.insert(tk.END, info_content)
        info_text_widget.config(state=tk.DISABLED)  # Make read-only
        
    def set_interval(self, a, b):
        """Set the interval values in the entry fields"""
        self.a_entry.delete(0, tk.END)
        self.a_entry.insert(0, str(a))
        self.b_entry.delete(0, tk.END)
        self.b_entry.insert(0, str(b))
        
    def find_single_root(self):
        """Find a single root using the bisection method"""
        try:
            # Get input parameters
            a = float(self.a_entry.get())
            b = float(self.b_entry.get())
            tolerance = float(self.tolerance_entry.get())
            max_iterations = int(self.max_iter_entry.get())
            
            # Clear previous results
            self.single_result_text.delete(1.0, tk.END)
            
            # Display header
            self.single_result_text.insert(tk.END, "="*80 + "\n")
            self.single_result_text.insert(tk.END, "BISECTION METHOD ROOT FINDING\n")
            self.single_result_text.insert(tk.END, "="*80 + "\n\n")
            
            self.single_result_text.insert(tk.END, f"Function: f(x) = x³ - x² - 4x\n")
            self.single_result_text.insert(tk.END, f"Initial interval: [{a}, {b}]\n")
            self.single_result_text.insert(tk.END, f"Tolerance: {tolerance}\n")
            self.single_result_text.insert(tk.END, f"Maximum iterations: {max_iterations}\n\n")
            
            # Check if root is bracketed
            fa = target_function(a)
            fb = target_function(b)
            
            self.single_result_text.insert(tk.END, f"f({a}) = {fa:.6f}\n")
            self.single_result_text.insert(tk.END, f"f({b}) = {fb:.6f}\n\n")
            
            if fa * fb >= 0:
                self.single_result_text.insert(tk.END, "ERROR: Root is not bracketed in the given interval!\n")
                self.single_result_text.insert(tk.END, "f(a) and f(b) must have opposite signs.\n")
                return
            
            # Use core algorithm
            result = bisection_method(
                target_function,
                a, b,
                tolerance=tolerance,
                max_iterations=max_iterations
            )
            
            self.current_result = result
            
            self.single_result_text.insert(tk.END, "Root is bracketed. Starting iterations...\n\n")
            
            # Display iteration table
            table = format_iteration_table(result['iteration_data'])
            self.single_result_text.insert(tk.END, table + "\n\n")
            
            # Display final results
            if result['converged']:
                self.single_result_text.insert(tk.END, "="*80 + "\n")
                self.single_result_text.insert(tk.END, "CONVERGENCE ACHIEVED!\n")
                self.single_result_text.insert(tk.END, "="*80 + "\n")
            else:
                self.single_result_text.insert(tk.END, "="*80 + "\n")
                self.single_result_text.insert(tk.END, "MAXIMUM ITERATIONS REACHED!\n")
                self.single_result_text.insert(tk.END, "="*80 + "\n")
                
            results_summary = format_results(result)
            self.single_result_text.insert(tk.END, results_summary)
            
        except ValueError as e:
            self.single_result_text.delete(1.0, tk.END)
            self.single_result_text.insert(tk.END, f"Error: {str(e)}\n")
        except Exception as e:
            self.single_result_text.delete(1.0, tk.END)
            self.single_result_text.insert(tk.END, f"Unexpected error: {str(e)}\n")
    
    def find_all_roots(self):
        """Find all three roots of the target function"""
        try:
            # Clear previous results
            self.all_result_text.delete(1.0, tk.END)
            
            # Display header
            self.all_result_text.insert(tk.END, "="*80 + "\n")
            self.all_result_text.insert(tk.END, "FINDING ALL ROOTS OF f(x) = x³ - x² - 4x\n")
            self.all_result_text.insert(tk.END, "="*80 + "\n\n")
            
            # Use core algorithm to find all roots
            results = find_all_roots_target_function()
            
            for i, result in enumerate(results, 1):
                self.all_result_text.insert(tk.END, f"ROOT {i}: {result['root_name']}\n")
                self.all_result_text.insert(tk.END, "-" * 40 + "\n")
                
                if result.get('converged', False):
                    self.all_result_text.insert(tk.END, f"Initial interval: {result['initial_interval']}\n")
                    self.all_result_text.insert(tk.END, f"Root value: {result['root']:.12f}\n")
                    self.all_result_text.insert(tk.END, f"Function value: {result['function_value']:.2e}\n")
                    self.all_result_text.insert(tk.END, f"Iterations: {result['iterations']}\n")
                    self.all_result_text.insert(tk.END, f"Final error: {result['error']:.2e}\n")
                    
                    # Display some iteration details
                    if len(result['iteration_data']) > 0:
                        last_iter = result['iteration_data'][-1]
                        self.all_result_text.insert(tk.END, f"Final interval: [{last_iter['a']:.6f}, {last_iter['b']:.6f}]\n")
                else:
                    self.all_result_text.insert(tk.END, f"FAILED: {result.get('error_message', 'Unknown error')}\n")
                
                self.all_result_text.insert(tk.END, "\n")
            
            # Summary
            successful_roots = [r for r in results if r.get('converged', False)]
            self.all_result_text.insert(tk.END, "="*80 + "\n")
            self.all_result_text.insert(tk.END, f"SUMMARY: Found {len(successful_roots)} out of 3 roots\n")
            self.all_result_text.insert(tk.END, "="*80 + "\n")
            
            if len(successful_roots) == 3:
                self.all_result_text.insert(tk.END, "All roots found successfully!\n\n")
                self.all_result_text.insert(tk.END, "Final root values:\n")
                for i, result in enumerate(successful_roots, 1):
                    self.all_result_text.insert(tk.END, f"x{i} = {result['root']:.12f}\n")
            
        except Exception as e:
            self.all_result_text.delete(1.0, tk.END)
            self.all_result_text.insert(tk.END, f"Error finding all roots: {str(e)}\n")
    
    def visualize_single(self):
        """Create visualization for single root finding"""
        if not self.current_result:
            messagebox.showwarning("No Data", "Please solve for a root first!")
            return
        
        try:
            # Create visualization using the iteration data
            self.create_visualization(self.current_result)
            
        except Exception as e:
            messagebox.showerror("Visualization Error", f"Error creating visualization: {str(e)}")
    
    def create_visualization(self, result):
        """Create interactive visualization using Plotly"""
        try:
            iteration_data = result['iteration_data']
            
            # Create subplots
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=('Function Plot with Iterations', 'Root Convergence', 
                               'Error Reduction', 'Interval Narrowing'),
                specs=[[{"secondary_y": False}, {"secondary_y": False}],
                       [{"secondary_y": False}, {"secondary_y": False}]]
            )
            
            # Get plot range
            a_orig = iteration_data[0]['a']
            b_orig = iteration_data[0]['b']
            plot_margin = abs(b_orig - a_orig) * 0.5
            x_range = np.linspace(a_orig - plot_margin, b_orig + plot_margin, 1000)
            y_range = [target_function(x) for x in x_range]
            
            # Plot 1: Function with iterations
            fig.add_trace(
                go.Scatter(x=x_range, y=y_range, mode='lines', name='f(x)', 
                          line=dict(color='blue', width=2)),
                row=1, col=1
            )
            
            # Add zero line
            fig.add_trace(
                go.Scatter(x=[x_range[0], x_range[-1]], y=[0, 0], mode='lines', 
                          name='y=0', line=dict(color='black', dash='dash')),
                row=1, col=1
            )
            
            # Add iteration points
            iterations = [d['iteration'] for d in iteration_data]
            c_values = [d['c'] for d in iteration_data]
            fc_values = [d['f_c'] for d in iteration_data]
            
            fig.add_trace(
                go.Scatter(x=c_values, y=fc_values, mode='markers+lines', 
                          name='Iterations', marker=dict(color='red', size=8)),
                row=1, col=1
            )
            
            # Plot 2: Convergence plot
            fig.add_trace(
                go.Scatter(x=iterations, y=c_values, mode='markers+lines', 
                          name='Root Approximation', line=dict(color='green')),
                row=1, col=2
            )
            
            # Plot 3: Error reduction
            errors = [d['error'] for d in iteration_data]
            fig.add_trace(
                go.Scatter(x=iterations, y=errors, mode='markers+lines', 
                          name='Error', line=dict(color='orange')),
                row=2, col=1
            )
            
            # Plot 4: Interval narrowing
            a_values = [d['a'] for d in iteration_data]
            b_values = [d['b'] for d in iteration_data]
            
            fig.add_trace(
                go.Scatter(x=iterations, y=a_values, mode='markers+lines', 
                          name='Lower bound (a)', line=dict(color='purple')),
                row=2, col=2
            )
            
            fig.add_trace(
                go.Scatter(x=iterations, y=b_values, mode='markers+lines', 
                          name='Upper bound (b)', line=dict(color='brown')),
                row=2, col=2
            )
            
            # Update layout
            fig.update_layout(
                title_text="Bisection Method Visualization - f(x) = x³ - x² - 4x",
                showlegend=True,
                height=800,
                template="plotly_white"
            )
            
            # Update y-axis for error plot to log scale
            fig.update_yaxes(type="log", row=2, col=1)
            
            # Save and open the plot
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.html')
            temp_file.close()
            
            pyo.plot(fig, filename=temp_file.name, auto_open=False)
            webbrowser.open('file://' + os.path.realpath(temp_file.name))
            
            self.single_result_text.insert(tk.END, "\nVisualization opened in browser!\n")
            
        except Exception as e:
            raise Exception(f"Visualization error: {str(e)}")
    
    def clear_single(self):
        """Clear single root results"""
        self.single_result_text.delete(1.0, tk.END)
        self.current_result = None
        self.single_result_text.insert(tk.END, "Results cleared. Ready for new calculation!\n")


def main():
    root = tk.Tk()
    app = BisectionMethodGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()