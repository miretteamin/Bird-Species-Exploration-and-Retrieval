import tkinter as tk
from tkinter import filedialog, PhotoImage, ttk
from PIL import Image, ImageTk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Bird Species Exploration and Retrieval")
        # self.geometry("300x200")
        
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)
        
        self.frames = {}
        for F in (WelcomePage, ButtonPage, TextPage, ImagePage, ImageTextPage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame("WelcomePage")
    
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        if (page_name == 'WelcomePage'):
            self.geometry('462x571')
        else:
            self.geometry('')
        frame.tkraise()

class WelcomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        image_paths = ['data/images/001.Black_footed_Albatross/Black_Footed_Albatross_0001_796111.jpg',
                   'data/images/091.Mockingbird/Mockingbird_0003_80833.jpg',
                   'data/images/076.Dark_eyed_Junco/Dark_Eyed_Junco_0012_66932.jpg',
                   'data/images/174.Palm_Warbler/Palm_Warbler_0005_169918.jpg',
                   'data/images/143.Caspian_Tern/Caspian_Tern_0006_145594.jpg',
                   'data/images/106.Horned_Puffin/Horned_Puffin_0004_100733.jpg',
                   'data/images/105.Whip_poor_Will/Whip_Poor_Will_0005_796425.jpg',
                   'data/images/002.Laysan_Albatross/Laysan_Albatross_0033_658.jpg',
                   'data/images/021.Eastern_Towhee/Eastern_Towhee_0001_22314.jpg',]

        # Add a label at the top
        label = tk.Label(self, text="Bird Species Exploration and Retrieval", font=("Helvetica", 16))
        label.grid(row=0, column=0, columnspan=3, pady=10)

        # Load images and display them in a 3x3 grid
        self.images = []
        for i in range(9):
            img = Image.open(image_paths[i])
            
            # Resize image to fit within the grid (optional)
            img = img.resize((150, 150))  # Resize to 150x150 pixels
            
            # Convert the image to a Tkinter-compatible PhotoImage object
            img_tk = ImageTk.PhotoImage(img)
            self.images.append(img_tk)  # Store images to prevent garbage collection

            row = (i // 3) + 1  # Calculate row position
            col = i % 3  # Calculate column position

            # Create a label for each image
            img_label = tk.Label(self, image=img_tk)
            img_label.grid(row=row, column=col)

        self.start_button = tk.Button(self, text="Start", 
                                      command=lambda: controller.show_frame("ButtonPage"),
                                        bg="#4CAF50", fg="white",
                                      relief='raised', font=("Arial", 14, "bold"))
        self.start_button.bind("<Enter>", self.on_enter)
        self.start_button.bind("<Leave>", self.on_leave)
        self.start_button.grid(row=4, column=1, pady=10)
    
    def on_enter(self, e):
        self.start_button.config(bg="orange", fg="black")

    def on_leave(self, e):
        self.start_button.config(bg="#4CAF50", fg="white")

class ButtonPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        label = ttk.Label(self, text="Choose an option:", font=("Arial", 14))
        label.pack(pady=10)
        
        button1 = ttk.Button(self, text="Use Text", command=lambda: controller.show_frame("TextPage"))
        button1.pack(pady=5)
        
        button2 = ttk.Button(self, text="Use Image", command=lambda: controller.show_frame("ImagePage"))
        button2.pack(pady=5)
        
        button3 = ttk.Button(self, text="Use Both", command=lambda: controller.show_frame("ImageTextPage"))
        button3.pack(pady=5)
        
        back_button = ttk.Button(self, text="Back", command=lambda: controller.show_frame("WelcomePage"))
        back_button.pack(pady=10)


class TextPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        input_label = tk.Label(self, text="Describe the Bird:", font=("Arial", 12))
        input_label.grid(row=0, column=1, pady=10)

        # Entry box to capture text input from the user
        self.entry_box = tk.Text(self, width=40, height=5, bg='lightgray', fg='black', font=("Helvetica", 12), undo=True)
        self.entry_box.grid(row=1, column=1, pady=10, padx=40)
        self.entry_box.bind("<Return>", self.on_enter)  # Bind Enter key to capture text and show image

        submit_button = ttk.Button(self, text="Submit", command=self.print_text)
        submit_button.grid(row=2, column=1, pady=10)

        # Load and resize the image to fit the layout
        img = Image.open('data/images/001.Black_footed_Albatross/Black_Footed_Albatross_0001_796111.jpg')
        img = img.resize((300, 300))  # Resize to fit the grid
        self.img_tk = ImageTk.PhotoImage(img)

        # Create a label for the image but do not display it yet
        self.img_label = tk.Label(self, image=self.img_tk)

        back_button = ttk.Button(self, text="Back", command=self.back)
        back_button.grid(row=5, column=1, pady=10)  # Adjusted row number to avoid overlap

    def print_text(self):
        entered_text = self.entry_box.get("1.0", "end-1c")  # Get the text entered by the user
        print(f"Entered text: {entered_text}")  # Print the entered text in the console
        self.display_image()  # Display the image when Submit button is pressed

    def on_enter(self, event):
        entered_text = self.entry_box.get("1.0", "end-1c")  # Get the text entered by the user
        print(f"Entered text: {entered_text}")
        self.display_image()  # Display the image when Enter key is pressed

    def display_image(self):
        """This method displays the image only once after text is entered or submitted."""
        self.img_label.grid(row=3, column=1, pady=20) 
        # self.img_label.grid_forget()  # If the image is placed before, hide it
        # self.img_label.grid(row=3, column=1, pady=20)  # Place image again after hiding it

    def back(self):
        self.img_label.grid_forget()
        self.controller.show_frame("ButtonPage")


class ImagePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Configure the grid columns to expand and fill the available space
        self.grid_columnconfigure(0, weight=1, uniform="equal")
        self.grid_columnconfigure(1, weight=2, uniform="equal")
        self.grid_columnconfigure(2, weight=1, uniform="equal")

        input_label = tk.Label(self, text="Choose an Image:", font=("Arial", 12))
        input_label.grid(row=0, column=1, pady=10, sticky="nsew")

        # Button to open the image file dialog
        browse_button = ttk.Button(self, text="Browse Image", command=self.browse_image)
        browse_button.grid(row=1, column=1, pady=10)

        # Label to display the chosen image
        self.img_label = tk.Label(self)
        self.img_label.grid(row=2, column=1, pady=20, sticky="nsew")

        self.tgt_img_label = tk.Label(self)
        self.tgt_img_label.grid(row=3, column=1, pady=20, sticky="nsew")

        back_button = ttk.Button(self, text="Back", command=self.back)
        back_button.grid(row=4, column=1, pady=10)

    def browse_image(self):
        """Open file dialog to select an image and display it."""
        # Open file dialog to select an image
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
        
        if file_path:
            # Open and resize the image to fit within the layout
            img = Image.open(file_path)
            img = img.resize((250, 250))  # Resize to fit the grid
            img_tk = ImageTk.PhotoImage(img)
            
            # Update the image label with the selected image
            self.img_label.config(image=img_tk)
           
            # Keep a reference to the image to prevent garbage collection
            self.img_label.img_tk = img_tk  # Save the image reference
        self.show_default_image()
    
    def show_default_image(self):
        """Display a placeholder or default image in the img_label."""
        # Load and show a placeholder or default image (replace this with any default image)
        img = Image.open('data/images/001.Black_footed_Albatross/Black_Footed_Albatross_0001_796111.jpg')
        img = img.resize((250, 250))  # Resize to fit the grid
        img_tk = ImageTk.PhotoImage(img)
        
        # Update the label to show the default image
        self.tgt_img_label.config(image=img_tk)
        
        # Save the image reference to avoid garbage collection
        self.tgt_img_label.img_tk = img_tk  # Store the image to prevent it from being garbage collected
    
    def display_browsed_image(self):
        """Display the browsed image in the img_label."""
        if hasattr(self, 'browsed_image_path') and self.browsed_image_path:
            # Open and resize the browsed image
            img = Image.open(self.browsed_image_path)
            img = img.resize((300, 300))  # Resize to fit the grid
            img_tk = ImageTk.PhotoImage(img)
            
            # Update the label to show the browsed image
            self.img_label.config(image=img_tk)
            
            # Save the image reference to avoid garbage collection
            self.img_label.img_tk = img_tk  # Store the image to prevent it from being garbage collected
    def back(self):
        self.img_label.grid_forget()
        self.tgt_img_label.grid_forget()
        self.controller.show_frame("ButtonPage")

class ImageTextPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Configure the grid columns to expand and fill the available space
        self.grid_columnconfigure(0, weight=1, uniform="equal")
        self.grid_columnconfigure(1, weight=2, uniform="equal")
        self.grid_columnconfigure(2, weight=1, uniform="equal")

        input_label1 = tk.Label(self, text="Describe the Bird:", font=("Arial", 12))
        input_label1.grid(row=0, column=1, pady=10)

        # Entry box to capture text input from the user
        self.entry_box = tk.Text(self, width=40, height=5, bg='lightgray', fg='black', font=("Helvetica", 12), undo=True)
        self.entry_box.grid(row=1, column=1, pady=10, padx=40)
        self.entry_box.bind("<Return>", self.on_enter)  # Bind Enter key to capture text and show image

        submit_button = ttk.Button(self, text="Submit", command=self.print_text)
        submit_button.grid(row=2, column=1, pady=10)

        input_label2 = tk.Label(self, text="Choose an Image:", font=("Arial", 12))
        input_label2.grid(row=3, column=1, pady=10, sticky="nsew")

        # Button to open the image file dialog
        browse_button = ttk.Button(self, text="Browse Image", command=self.browse_image)
        browse_button.grid(row=4, column=1, pady=10)

        # Label to display the chosen image
        self.img_label = tk.Label(self)
        self.img_label.grid(row=5, column=1, pady=20, sticky="nsew")

        self.tgt_img_label = tk.Label(self)
        self.tgt_img_label.grid(row=6, column=1, pady=20, sticky="nsew")

        back_button = ttk.Button(self, text="Back", command=self.back)
        back_button.grid(row=7, column=1, pady=10)

    def browse_image(self):
        """Open file dialog to select an image and display it."""
        # Open file dialog to select an image
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
        
        if file_path:
            # Open and resize the image to fit within the layout
            img = Image.open(file_path)
            img = img.resize((250, 250))  # Resize to fit the grid
            img_tk = ImageTk.PhotoImage(img)
            
            # Update the image label with the selected image
            self.img_label.config(image=img_tk)
           
            # Keep a reference to the image to prevent garbage collection
            self.img_label.img_tk = img_tk  # Save the image reference
        self.show_default_image()
    
    def show_default_image(self):
        """Display a placeholder or default image in the img_label."""
        # Load and show a placeholder or default image (replace this with any default image)
        img = Image.open('data/images/001.Black_footed_Albatross/Black_Footed_Albatross_0001_796111.jpg')
        img = img.resize((250, 250))  # Resize to fit the grid
        img_tk = ImageTk.PhotoImage(img)
        
        # Update the label to show the default image
        self.tgt_img_label.config(image=img_tk)
        
        # Save the image reference to avoid garbage collection
        self.tgt_img_label.img_tk = img_tk  # Store the image to prevent it from being garbage collected
    
    def display_browsed_image(self):
        """Display the browsed image in the img_label."""
        if hasattr(self, 'browsed_image_path') and self.browsed_image_path:
            # Open and resize the browsed image
            img = Image.open(self.browsed_image_path)
            img = img.resize((300, 300))  # Resize to fit the grid
            img_tk = ImageTk.PhotoImage(img)
            
            # Update the label to show the browsed image
            self.img_label.config(image=img_tk)
            
            # Save the image reference to avoid garbage collection
            self.img_label.img_tk = img_tk  # Store the image to prevent it from being garbage collected
    def back(self):
        self.img_label.grid_forget()
        self.tgt_img_label.grid_forget()
        self.controller.show_frame("ButtonPage")

    def print_text(self):
        entered_text = self.entry_box.get("1.0", "end-1c")  # Get the text entered by the user
        print(f"Entered text: {entered_text}")  # Print the entered text in the console
        self.display_image()  # Display the image when Submit button is pressed

    def on_enter(self, e):
        entered_text = self.entry_box.get("1.0", "end-1c")  # Get the text entered by the user
        print(f"Entered text: {entered_text}")
        self.display_image()  # Display the image when Enter key is pressed

    def display_image(self):
        """This method displays the image only once after text is entered or submitted."""
        self.img_label.grid(row=3, column=1, pady=20) 
        # self.img_label.grid_forget()  # If the image is placed before, hide it
        # self.img_label.grid(row=3, column=1, pady=20)  # Place image again after hiding it

if __name__ == "__main__":
    app = App()
    app.mainloop()
