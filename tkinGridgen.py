import tkinter as tk
import random

# Global variables to manage the game state
current_number_to_find = 1
cell_data = {} # Stores information about each cell's number and IDs

def create_grid():
    """Generates and draws a grid with unique, shuffled numbers."""
    global current_number_to_find, cell_data

    try:
        rows = int(rows_var.get())
        cols = int(cols_var.get())
        if rows <= 0 or cols <= 0:
            raise ValueError
    except ValueError:
        status_label.config(text="Error: Please enter positive integers.", fg="red")
        return

    # Reset game state
    current_number_to_find = 1
    cell_data = {}
    status_label.config(text=f"Find {current_number_to_find}", fg="black")
    canvas.delete("all")
    
    # Re-bind the click event in case it was unbound
    canvas.bind("<Button-1>", on_click)

    # Generate a list of unique random numbers
    total_cells = rows * cols
    numbers = list(range(1, total_cells + 1))
    random.shuffle(numbers)
    
    # Calculate cell dimensions
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    
    cell_width = canvas_width / cols
    cell_height = canvas_height / rows
    
    for row in range(rows):
        for col in range(cols):
            x1 = col * cell_width
            y1 = row * cell_height
            x2 = x1 + cell_width
            y2 = y1 + cell_height
            
            # Get the next number
            number = numbers.pop()

            # Draw the rectangle
            rect_id = canvas.create_rectangle(x1, y1, x2, y2, fill="lightgray", outline="black")

            # Draw the number
            text_x = x1 + cell_width / 2
            text_y = y1 + cell_height / 2
            text_id = canvas.create_text(text_x, text_y, text=str(number), font=("Arial", 16, "bold"))
            
            # Store the rectangle and text IDs with the number
            cell_data[rect_id] = {'number': number, 'text_id': text_id}

def on_click(event):
    """Handles the user's click on a grid cell."""
    global current_number_to_find
    
    # Get the ID of the item clicked. `find_closest` returns a tuple.
    item_id = canvas.find_closest(event.x, event.y)[0]

    # Check if the clicked item is one of our grid rectangles
    if item_id in cell_data:
        clicked_number = cell_data[item_id]['number']

        if clicked_number == current_number_to_find:
            # Correct click: change color to green
            canvas.itemconfig(item_id, fill="green")
            
            # Check if the game is over
            if current_number_to_find == len(cell_data):
                status_label.config(text="Congratulations! You won!", fg="green")
                # Unbind the click event to prevent further clicks
                canvas.unbind("<Button-1>")
            else:
                current_number_to_find += 1
                status_label.config(text=f"Great! Now find {current_number_to_find}", fg="black")
        else:
            # Incorrect click: flash the cell red
            canvas.itemconfig(item_id, fill="red")
            canvas.after(200, lambda: canvas.itemconfig(item_id, fill="lightgray"))
            status_label.config(text=f"Incorrect! Find {current_number_to_find}", fg="red")


# --- Main Application Setup ---
root = tk.Tk()
root.title("Ascending Number Grid Game")

# Frame for input widgets
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

# Input variables
rows_var = tk.StringVar()
cols_var = tk.StringVar()

# Row input
rows_label = tk.Label(input_frame, text="Rows:")
rows_label.pack(side=tk.LEFT, padx=5)
rows_entry = tk.Entry(input_frame, textvariable=rows_var, width=10)
rows_entry.pack(side=tk.LEFT, padx=5)
rows_var.set("5")

# Column input
cols_label = tk.Label(input_frame, text="Columns:")
cols_label.pack(side=tk.LEFT, padx=5)
cols_entry = tk.Entry(input_frame, textvariable=cols_var, width=10)
cols_entry.pack(side=tk.LEFT, padx=5)
cols_var.set("5")

# Button to generate grid
generate_button = tk.Button(root, text="Generate Grid", command=create_grid)
generate_button.pack(pady=5)

# Label to display status or errors
status_label = tk.Label(root, text="Find 1", fg="black")
status_label.pack()

# Canvas to draw the grid
canvas = tk.Canvas(root, width=600, height=600, bg="white")
canvas.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Bind the click event to the canvas
canvas.bind("<Button-1>", on_click)

# Run the application
root.mainloop()