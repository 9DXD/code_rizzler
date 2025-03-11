import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import sys
from io import StringIO

def init_code():
    """Returns the initial code for the compiler with more variables"""
    code = """_=+([]==[]);"""
    # Extend to 32 underscores to handle larger numbers (up to 2^32)
    for i in range(2, 33):  # Changed from 9 to 32
        code += f"{'_'*i}={'_'*(i-1)}+_;"
    return code

def get_binary_factors(n):
    """Returns a list of factors of a given number in binary form"""
    return [index for index, bit in enumerate(bin(n)[:1:-1]) if bit == "1"]

def codegen(factors):
    """Generates code for a given list of factors"""
    char_code = ""
    for index, factor in enumerate(factors):
        if factor >= 32:  # Check if factor exceeds our max underscore count
            raise ValueError(f"Number too large to encode (requires {factor+1} underscores)")
        char_code += "_" if factor == 0 else f"__**{'_'*factor}"
        if index < len(factors) - 1:
            char_code += "+"
    return char_code

def wrap_exec(encoded_string_len, encoded_python_string):
    """Wraps code in exec()"""
    return f"""exec((('%'+'c̶'[[]>[]])*({encoded_string_len}))%({','.join(encoded_python_string)}))"""

def create_gui():
    root = tk.Tk()
    root.title("Python Code Rizzler")
    root.geometry("600x680")

    main_frame = ttk.Frame(root, padding="10")
    main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    ttk.Label(main_frame, text="Enter Python Code:").grid(row=0, column=0, sticky=tk.W, pady=5)
    code_input = scrolledtext.ScrolledText(main_frame, width=70, height=8, wrap=tk.WORD)
    code_input.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
    default_code = 'for i in range(3):\n    print(f"Count: {i}")\nx = 10\nprint(f"Final value: {x}")'
    code_input.insert(tk.END, default_code)

    warning_text = "Note: Works with most Python code.\nVery large scripts (>4GB) might cause memory issues."
    ttk.Label(main_frame, text=warning_text, wraplength=550, justify=tk.LEFT).grid(row=2, column=0, columnspan=2, pady=5)

    button_frame = ttk.Frame(main_frame)
    button_frame.grid(row=3, column=0, columnspan=2, pady=10)

    output_text = scrolledtext.ScrolledText(main_frame, width=70, height=15, wrap=tk.WORD)
    exec_output_text = scrolledtext.ScrolledText(main_frame, width=70, height=5, wrap=tk.WORD)

    def generate_code():
        try:
            input_code = code_input.get("1.0", tk.END).rstrip()
            encoded_python_string = [codegen(get_binary_factors(ord(char))) for char in input_code]
            encoded_string_len = codegen(get_binary_factors(len(input_code)))
            generated_code = init_code() + wrap_exec(encoded_string_len, encoded_python_string)
            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, generated_code)
            exec_output_text.delete(1.0, tk.END)
        except ValueError as e:
            messagebox.showerror("Error", f"Generation failed: {str(e)}\n\nInput too complex for current encoder.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate: {str(e)}")

    def generate_and_run():
        try:
            input_code = code_input.get("1.0", tk.END).rstrip()
            encoded_python_string = [codegen(get_binary_factors(ord(char))) for char in input_code]
            encoded_string_len = codegen(get_binary_factors(len(input_code)))
            generated_code = init_code() + wrap_exec(encoded_string_len, encoded_python_string)
            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, generated_code)
            
            old_stdout = sys.stdout
            redirected_output = sys.stdout = StringIO()
            try:
                exec(generated_code)
                output = redirected_output.getvalue()
            except Exception as e:
                output = f"Execution Error: {str(e)}"
            finally:
                sys.stdout = old_stdout
            exec_output_text.delete(1.0, tk.END)
            exec_output_text.insert(tk.END, output)
        except ValueError as e:
            messagebox.showerror("Error", f"Generation failed: {str(e)}\n\nInput too complex for current encoder.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process: {str(e)}")

    generate_btn = ttk.Button(button_frame, text="Generate Code", command=generate_code)
    generate_btn.grid(row=0, column=0, padx=5)
    run_btn = ttk.Button(button_frame, text="Generate & Run", command=generate_and_run)
    run_btn.grid(row=0, column=1, padx=5)

    ttk.Label(main_frame, text="Generated Code:").grid(row=4, column=0, sticky=tk.W, pady=5)
    output_text.grid(row=5, column=0, columnspan=2, pady=5)
    ttk.Label(main_frame, text="Execution Output:").grid(row=6, column=0, sticky=tk.W, pady=5)
    exec_output_text.grid(row=7, column=0, columnspan=2, pady=5)

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    main_frame.columnconfigure(1, weight=1)

    root.mainloop()

create_gui()
