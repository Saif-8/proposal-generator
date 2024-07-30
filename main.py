import tkinter as tk
from tkinter import filedialog, scrolledtext, colorchooser
from fpdf import FPDF, XPos, YPos
from PIL import Image, ImageTk  # Requires Pillow library

NAMED_COLORS = {
    "white": "#FFFFFF",
    "black": "#000000",
    "red": "#FF0000",
    "green": "#00FF00",
    "blue": "#0000FF",
}

class ProposalGeneratorApp:
    """
        A class to create a Proposal Generator application using Tkinter.
        This application allows users to input project details, add objectives, and save the information as a PDF.

        Attributes:
            root (tk.Tk): The root window of the Tkinter application.
            main_frame (tk.Frame): The main frame that contains all widgets.
            canvas (tk.Canvas): The canvas to allow scrolling of the main content.
            scrollbar (tk.Scrollbar): The scrollbar for vertical scrolling of the canvas.
            scrollable_frame (tk.Frame): The frame that is scrollable within the canvas.
            toolbar (tk.Frame): The frame containing text formatting buttons.
            objectives_frame (tk.Frame): The frame containing project objectives and related buttons.
            about_frame (tk.Frame): The frame for the "About" section where project details are entered.
            about_bg_color (str): Background color of the "About" section.
            about_font_color (str): Font color of the "About" section.
            goal_font_color (str): Font color for goal entries.
            goal_row_color (str): Background color for goal rows.
            tables (list): List to store tuples of problem and goal entries.
            text_alignment (str): Alignment setting for the text in the "About" section.
            color_preview_label (tk.Label): Label to preview selected goal row colors.
            bold_btn, italic_btn, underline_btn, bullet_btn, heading_btn, left_align_btn, center_align_btn, right_align_btn (tk.Button): Buttons for text formatting.
            add_table_button, save_pdf_button, bg_color_btn, about_font_color_btn, row_color_btn, goal_font_color_btn (tk.Button): Buttons for adding tables, saving PDF, and setting colors.
            about_label (tk.Label): Label for the "About" section.
            about_text (scrolledtext.ScrolledText): Text area for entering project details.
        """
    def __init__(self, root):
        """
                Initializes the ProposalGeneratorApp with the main Tkinter window and sets up the initial layout and widgets.

                Parameters:
                    root (tk.Tk): The root window of the Tkinter application.
                """
        self.root = root
        self.root.title("Proposal Generator")
        icon_image = Image.open('proposal-icon.png')  # Set your .png file path here
        self.root.iconphoto(True, ImageTk.PhotoImage(icon_image))
        self.set_initial_geometry()

        # Create main frame with canvas and scrollbar
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.main_frame)
        self.scrollbar = tk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.config(yscrollcommand=self.scrollbar.set)

        # Create and place widgets
        self.create_widgets()

    def set_initial_geometry(self):
        """Sets the initial geometry of the root window to 80% of the screen size."""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = int(screen_width * 0.8)
        window_height = int(screen_height * 0.8)
        self.root.geometry(f"{window_width}x{window_height}")

    def create_widgets(self):
        """Creates and places all widgets in the application."""
        # Toolbar for text formatting
        self.toolbar = tk.Frame(self.scrollable_frame)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        self.bold_btn = self.create_tool_button("Bold", self.make_bold)
        self.italic_btn = self.create_tool_button("Italic", self.make_italic)
        self.underline_btn = self.create_tool_button("Underline", self.make_underline)
        self.bullet_btn = self.create_tool_button("Bullet", self.make_bullet)
        self.heading_btn = self.create_tool_button("Heading", self.make_heading)
        self.left_align_btn = self.create_tool_button("Left Align", lambda: self.set_alignment("left"))
        self.center_align_btn = self.create_tool_button("Center Align", lambda: self.set_alignment("center"))
        self.right_align_btn = self.create_tool_button("Right Align", lambda: self.set_alignment("right"))

        # Right side - Project Objectives section
        self.objectives_frame = tk.Frame(self.scrollable_frame)
        self.objectives_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Add buttons for adding objectives and saving PDF
        self.add_table_button = self.create_bootstrap_button("Add Objective Table", self.add_table)
        self.add_table_button.pack(pady=5)

        self.save_pdf_button = self.create_bootstrap_button("Save as PDF", self.save_as_pdf)
        self.save_pdf_button.pack(pady=10)

        # Color buttons
        self.bg_color_btn = self.create_bootstrap_button("Set About BG Color", self.set_about_bg_color)
        self.bg_color_btn.pack(pady=2)

        self.about_font_color_btn = self.create_bootstrap_button("Set About Font Color", self.set_about_font_color)
        self.about_font_color_btn.pack(pady=2)

        self.row_color_btn = self.create_bootstrap_button("Set Goal Row Color", self.set_goal_row_color)
        self.row_color_btn.pack(pady=2)

        self.goal_font_color_btn = self.create_bootstrap_button("Set Goal Font Color", self.set_goal_font_color)
        self.goal_font_color_btn.pack(pady=2)

        # Color preview label
        self.color_preview_label = tk.Label(self.objectives_frame, text="Goal Row Color Preview", bg='white', width=20, height=2)
        self.color_preview_label.pack(pady=10)

        # Left side - About section
        self.about_bg_color = 'black'
        self.about_font_color = 'white'
        self.goal_font_color = 'black'
        self.goal_row_color = '#ffffff'
        self.about_frame = tk.Frame(self.scrollable_frame, bg=self.about_bg_color)
        self.about_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.about_label = tk.Label(self.about_frame, text="Details About the Project", font=("Noto Sans", 16, "bold"),
                                    fg=self.about_font_color, bg=self.about_bg_color)
        self.about_label.pack(anchor=tk.W, padx=10, pady=5)

        self.about_text = scrolledtext.ScrolledText(self.about_frame, bg='white', fg='black', wrap=tk.WORD)
        self.about_text.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        self.tables = []
        self.text_alignment = "L"

        # Add an initial table
        self.add_table()
        self.update_color_preview()

    def create_tool_button(self, text, command):
        """
                Creates a toolbar button for text formatting.

                Parameters:
                    text (str): The text to display on the button.
                    command (function): The function to call when the button is clicked.

                Returns:
                    tk.Button: The created button.
                """
        btn = tk.Button(self.toolbar, text=text, command=command, bg='#007bff', fg='white', relief=tk.FLAT, padx=10,
                        pady=5)
        btn.config(font=("Noto Sans", 12))
        btn.pack(side=tk.LEFT, padx=2, pady=2)
        return btn

    def create_bootstrap_button(self, text, command):
        """
                Creates a button styled like a Bootstrap button.

                Parameters:
                    text (str): The text to display on the button.
                    command (function): The function to call when the button is clicked.

                Returns:
                    tk.Button: The created button.
                """
        btn = tk.Button(self.objectives_frame, text=text, command=command, bg='#007bff', fg='white', relief=tk.FLAT,
                        padx=10, pady=5)
        btn.config(font=("Noto Sans", 12))
        return btn

    def make_bold(self):
        """Makes the selected text bold in the 'About' text area."""
        self.about_text.tag_add("bold", "sel.first", "sel.last")
        self.about_text.tag_config("bold", font=("Noto Sans", 12, "bold"))

    def make_italic(self):
        """Makes the selected text italic in the 'About' text area."""
        self.about_text.tag_add("italic", "sel.first", "sel.last")
        self.about_text.tag_config("italic", font=("Noto Sans", 12, "italic"))

    def make_underline(self):
        """Makes the selected text underlined in the 'About' text area."""
        self.about_text.tag_add("underline", "sel.first", "sel.last")
        self.about_text.tag_config("underline", font=("Noto Sans", 12, "underline"))

    def make_bullet(self):
        """Adds a bullet point to the selected line(s) in the 'About' text area."""
        if self.about_text.tag_ranges(tk.SEL):
            start_index = self.about_text.index(tk.SEL_FIRST)
            end_index = self.about_text.index(tk.SEL_LAST)
            selected_text = self.about_text.get(start_index, end_index)

            lines = selected_text.split('\n')
            bulleted_lines = ["\u2022 " + line for line in lines]

            bulleted_lines = [" " + line for line in bulleted_lines]

            self.about_text.delete(start_index, end_index)
            self.about_text.insert(start_index, '\n'.join(bulleted_lines))

    def make_heading(self):
        """Formats the selected text as a heading in the 'About' text area."""
        if self.about_text.tag_ranges(tk.SEL):
            start_index = self.about_text.index(tk.SEL_FIRST)
            end_index = self.about_text.index(tk.SEL_LAST)
            selected_text = self.about_text.get(start_index, end_index).upper()

            self.about_text.delete(start_index, end_index)
            self.about_text.insert(start_index, selected_text)
            self.about_text.tag_add("heading", start_index, f"{start_index} + {len(selected_text)}c")
            self.about_text.tag_config("heading", font=("Noto Sans", 16, "bold"))

    def set_alignment(self, align):
        """
                Sets the text alignment for the 'About' text area.

                Parameters:
                    alignment (str): The alignment to set ("left", "center", "right").
                """
        self.text_alignment = {"left": "L", "center": "C", "right": "R"}[align]
        if self.about_text.tag_ranges(tk.SEL):
            start_index = self.about_text.index(tk.SEL_FIRST)
            end_index = self.about_text.index(tk.SEL_LAST)

            self.about_text.tag_add(align, start_index, end_index)
            self.about_text.tag_configure("left", justify=tk.LEFT)
            self.about_text.tag_configure("center", justify=tk.CENTER)
            self.about_text.tag_configure("right", justify=tk.RIGHT)

    def limit_entry_length(self, sv, max_length=105):
        """Limits the characters entry in the table to 105 characters"""
        text = sv.get()
        if len(text) > max_length:
            sv.set(text[:max_length])

    def add_table(self):
        """Adds a new problem-goal entry table to the objectives frame."""
        table_frame = tk.Frame(self.objectives_frame)
        table_frame.pack(pady=10)

        tk.Label(table_frame, text="Problem").grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        tk.Label(table_frame, text="Goal").grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        problem_var = tk.StringVar()
        problem_var.trace("w", lambda name, index, mode, sv=problem_var: self.limit_entry_length(sv))
        problem_entry = tk.Entry(table_frame, width=50, font=("Noto Sans", 12), textvariable=problem_var)
        problem_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        goal_var = tk.StringVar()
        goal_var.trace("w", lambda name, index, mode, sv=goal_var: self.limit_entry_length(sv))
        goal_entry = tk.Entry(table_frame, width=50, font=("Noto Sans", 12), textvariable=goal_var)
        goal_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        self.tables.append((problem_entry, goal_entry))

    def set_about_bg_color(self):
        """"Updates the background color of project box"""
        color = colorchooser.askcolor(title="Select Background Color")[1]
        if color:
            self.about_bg_color = color
            self.about_frame.config(bg=self.about_bg_color)
            self.about_label.config(bg=self.about_bg_color)
            self.about_text.config(bg='white')

    def set_about_font_color(self):
        """"Updates the font color of the project box fonts"""
        color = colorchooser.askcolor(title="Select Font Color")[1]
        if color:
            self.about_font_color = color
            self.about_label.config(fg=self.about_font_color)

    def set_goal_row_color(self):
        """"Updates the color of goal row"""
        color = colorchooser.askcolor(title="Select Goal Row Color")[1]
        if color:
            self.goal_row_color = color
            self.update_color_preview()

    def set_goal_font_color(self):
        """"Updates the font color of goal row"""
        color = colorchooser.askcolor(title="Select Goal Font Color")[1]
        if color:
            self.goal_font_color = color
            self.update_color_preview()

    def update_color_preview(self):
        """"Gives the preview of how the second row that is goal color will look like"""
        self.color_preview_label.config(bg=self.goal_row_color, fg=self.goal_font_color, text="Goal Row Color Preview")

    def hex_to_rgb(self, color):
        """
                Opens a color chooser dialog and returns the selected color.

                Parameters:
                    initial_color (str): The initial color to show in the color chooser.

                Returns:
                    str: The selected color in hex format, or None if no color was selected.
                """
        if isinstance(color, str):
            color = NAMED_COLORS.get(color.lower(), color)
            if color.startswith('#'):
                color = color.lstrip('#')

            if len(color) not in (3, 6):
                raise ValueError("Invalid hex color format")

            try:
                if len(color) == 3:
                    color = ''.join([c * 2 for c in color])
                return tuple(int(color[i:i + 2], 16) for i in range(0, 6, 2))
            except ValueError as e:
                raise ValueError("Invalid hex color value") from e
        else:
            raise ValueError("Color must be a string")

    def save_as_pdf(self):
        """Saves the project details and objectives as a PDF file."""
        pdf = FPDF()

        pdf.add_font("NotoSans", "", "NotoSans-Regular.ttf")
        pdf.add_font("NotoSans", "B", "NotoSans-Bold.ttf")

        pdf.add_page()

        pdf.set_font("NotoSans", 'B', 20)
        pdf.cell(0, 10, "Details About the Project:", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='L')
        pdf.ln(10)

        pdf.set_fill_color(*self.hex_to_rgb(self.about_bg_color))
        pdf.set_text_color(*self.hex_to_rgb(self.about_font_color))
        pdf.set_font("NotoSans", size=12)

        pdf.set_left_margin(15)
        pdf.set_right_margin(15)
        pdf.set_top_margin(15)
        pdf.set_auto_page_break(auto=True, margin=15)

        pdf.multi_cell(0, 10, self.about_text.get("1.0", tk.END).strip(), border=0, fill=True,
                       align=self.text_alignment)

        pdf.add_page()

        # Add centered heading on the second page with black font color
        pdf.set_font("NotoSans", 'B', 20)
        pdf.set_text_color(0, 0, 0)  # Set text color to black
        pdf.set_y(20)  # Adjust vertical position as needed
        pdf.cell(0, 10, "Project Objectives", 0, 1, 'C')
        pdf.ln(10)

        def adjust_font_size(pdf, text, max_width, initial_font_size=12):
            font_size = initial_font_size
            while pdf.get_string_width(text) > max_width and font_size > 6:
                font_size -= 1
                pdf.set_font("NotoSans", size=font_size)
            return font_size

        cell_width_problem = 30
        cell_width_text = 150
        cell_height = 10

        for idx, (problem_entry, goal_entry) in enumerate(self.tables):
            problem_text = problem_entry.get()
            goal_text = goal_entry.get()

            # Header row settings
            pdf.set_fill_color(255, 255, 255)  # Background color for header row (white)
            pdf.set_text_color(0, 0, 0)  # Text color for header row (black)
            pdf.set_font("NotoSans", 'B', 12)
            pdf.cell(cell_width_problem, cell_height, "Problem:", border=1, fill=True)
            pdf.set_font("NotoSans", size=12)
            problem_font_size = adjust_font_size(pdf, problem_text if problem_text else "N/A", cell_width_text)
            pdf.set_font("NotoSans", size=problem_font_size)
            pdf.cell(cell_width_text, cell_height, problem_text if problem_text else "N/A", border=1, new_x=XPos.RIGHT,
                     new_y=YPos.TOP, fill=True)

            pdf.ln(cell_height)

            pdf.set_fill_color(*self.hex_to_rgb(self.goal_row_color))  # Background color for goal rows
            pdf.set_text_color(*self.hex_to_rgb(self.goal_font_color))  # Font color for goal rows
            pdf.set_font("NotoSans", 'B', 12)
            pdf.cell(cell_width_problem, cell_height, "Goal:", border=1, fill=True)
            pdf.set_font("NotoSans", size=12)
            goal_font_size = adjust_font_size(pdf, goal_text if goal_text else "N/A", cell_width_text)
            pdf.set_font("NotoSans", size=goal_font_size)
            pdf.cell(cell_width_text, cell_height, goal_text if goal_text else "N/A", border=1, new_x=XPos.RIGHT,
                     new_y=YPos.TOP, fill=True)

            pdf.ln(cell_height * 2)  # Add extra space between tables

        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if file_path:
            pdf.output(file_path)
            self.reset_application()

    def reset_application(self):
        """"Reset the layout"""
        self.about_text.delete('1.0', tk.END)
        self.about_bg_color = 'black'
        self.about_font_color = 'white'
        self.goal_font_color = 'black'
        self.goal_row_color = '#ffffff'

        self.about_frame.config(bg=self.about_bg_color)
        self.about_label.config(bg=self.about_bg_color, fg=self.about_font_color)
        self.about_text.config(bg='white', fg='black')

        if self.tables:
            first_table = self.tables[0]
            for widget in first_table[0].master.winfo_children():
                if isinstance(widget, tk.Entry):
                    widget.delete(0, tk.END)

            for table in self.tables[1:]:
                for widget in table[0].master.winfo_children():
                    widget.destroy()
            self.tables = [first_table]

        self.update_color_preview()

if __name__ == "__main__":
    """Runs the Tkinter main loop."""
    root = tk.Tk()
    app = ProposalGeneratorApp(root)
    root.mainloop()
