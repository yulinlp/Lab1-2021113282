import os
from tkinter import *
from tkinter import ttk, messagebox, filedialog, simpledialog
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from graph import WordGraph

# modify on B2

def cli():
    while True:
        choice = int(input("""
操作列表: 
        1. 展示有向图
        2. 查询桥接词
        3. 生成新文本
        4. 计算最短路径
        5. 随机游走
        6. 退出
输入操作: """))
        if choice == 1:
            graph.showDirectedGraph()
            pic = plt.imread(os.path.join('output', 'graph.jpg'))
            plt.imshow(pic)
            plt.axis('off')
            plt.show()
        elif choice == 2:
            w1 = input('word1: ')
            w2 = input('word2: ')
            print(graph.queryBridgeWords(w1, w2))
        elif choice == 3:
            txt1 = input("输入文本: ")
            print(graph.generateNewText(txt1))
        elif choice == 4:
            w1 = input('word1: ')
            w2 = input('word2(输入#计算word1到所有单词的最短路径): ')
            if w2 != '#':
                print(graph.calcShortestPath(w1, w2))
                pic = plt.imread(os.path.join('output', 'shortest_path.jpg'))
                plt.imshow(pic)
                plt.axis('off')
                plt.show()
            else:
                print(graph.calcShortestPathAll(w1))
        elif choice == 5:
            print(graph.randomWalk())
        elif choice == 6:
            break


class WordGraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Word Graph App")
        self.create_widgets()
        # 添加选择文件的功能
        file_path = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select Text File", filetypes=[("Text files", "*.txt")])
        if file_path == '':
            # 如果用户没有选择文件，则退出应用程序
            messagebox.showwarning("Warning", "No text file selected. Closing the application.")
            self.root.destroy()
            exit()
        with open(file_path, 'r', encoding='utf-8') as f:
            txt = f.read()
        self.graph = WordGraph(txt)
            
    
    def create_widgets(self):
        frame = ttk.Frame(self.root, padding="10 10 10 10")
        frame.grid(row=0, column=0, sticky=(N, W, E, S))
        
        self.text_output = Text(frame, wrap="word", height=10, width=60, font=("Helvetica", 12))
        self.text_output.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky=(N, S, E, W))
        
        scrollbar = ttk.Scrollbar(frame, orient=VERTICAL, command=self.text_output.yview)
        scrollbar.grid(row=0, column=2, sticky=(N, S))
        self.text_output['yscrollcommand'] = scrollbar.set
        
        button_frame = ttk.LabelFrame(frame, text="Operations", padding="10 10 10 10")
        button_frame.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky=(N, S, E, W))
        
        ttk.Button(button_frame, text="Show Directed Graph", command=self.show_directed_graph).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(button_frame, text="Query Bridge Words", command=self.query_bridge_words).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(button_frame, text="Generate New Text", command=self.generate_new_text).grid(row=1, column=0, padx=5, pady=5)
        ttk.Button(button_frame, text="Calculate Shortest Path", command=self.calc_shortest_path).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(button_frame, text="Random Walk", command=self.random_walk).grid(row=2, column=0, padx=5, pady=5)
        ttk.Button(button_frame, text="Quit", command=self.quit).grid(row=2, column=1, padx=5, pady=5)
        
        self.image_frame = ttk.Frame(self.root, padding="10 10 10 10")
        self.image_frame.grid(row=2, column=0, sticky=(N, W, E, S))
        
        self.image_index = 0
        self.image_paths = []

    def show_directed_graph(self):
        self.graph.showDirectedGraph()
        img_path = os.path.join('output', 'graph.jpg')
        self.show_image(img_path)
    
    def query_bridge_words(self):
        w1 = self.prompt_user("word1")
        w2 = self.prompt_user("word2")
        result = self.graph.queryBridgeWords(w1, w2)
        self.display_output(result)
    
    def generate_new_text(self):
        txt1 = self.prompt_user("Input Text")
        result = self.graph.generateNewText(txt1)
        self.display_output(result)
    
    def calc_shortest_path(self):
        w1 = self.prompt_user("word1")
        w2 = self.prompt_user("word2 (Enter # to calculate the shortest path from word1 to all words)")
        if w2 != '#':
            result = self.graph.calcShortestPath(w1, w2)
            self.display_output(result)
            img_path = os.path.join('output', 'shortest_path.jpg')
            self.show_image(img_path)
        else:
            result = self.graph.calcShortestPathAll(w1)
            self.display_output(result)
            num = (len(result.split('\n')) - 1) // 2
            # 展示所有最短路径图片
            self.image_paths = [os.path.join('output', f'shortest_path_{i}.jpg') for i in range(num)]
            self.image_index = 1
            self.show_image(self.image_paths[self.image_index])
            self.create_navigation_buttons()
    
    def random_walk(self):
        result = self.graph.randomWalk()
        self.display_output(result)
    
    def prompt_user(self, prompt):
        return simpledialog.askstring("Input", prompt)
    
    def display_output(self, text):
        self.text_output.delete(1.0, END)
        self.text_output.insert(END, text)
    
    def show_image(self, img_path):
        img = plt.imread(img_path)
        fig, ax = plt.subplots()
        ax.imshow(img)
        ax.axis('off')
        
        # 清除之前的 canvas
        for widget in self.image_frame.winfo_children():
            widget.destroy()
        
        self.canvas = FigureCanvasTkAgg(fig, master=self.image_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky=(N, W, E, S))
        
        self.image_frame.grid_rowconfigure(0, weight=1)
        self.image_frame.grid_columnconfigure(0, weight=1)
    
    def create_navigation_buttons(self):
        # 添加导航按钮
        nav_frame = ttk.Frame(self.image_frame, padding="10 10 10 10")
        nav_frame.grid(row=1, column=0, sticky=(E, W))
        
        ttk.Button(nav_frame, text="Previous", command=self.show_previous_image).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(nav_frame, text="Next", command=self.show_next_image).grid(row=0, column=1, padx=5, pady=5)
    
    def show_next_image(self):
        if self.image_paths and self.image_index < len(self.image_paths) - 1:
            self.image_index += 1
            self.show_image(self.image_paths[self.image_index])
            self.create_navigation_buttons()
    
    def show_previous_image(self):
        if self.image_paths and self.image_index > 0:
            self.image_index -= 1
            self.show_image(self.image_paths[self.image_index])
            self.create_navigation_buttons()
            
    def quit(self):
        # 清除 output/ 下的所有图片
        for f in os.listdir('output'):
            if f.endswith('.jpg'):
                os.remove(os.path.join('output', f))
        self.root.quit()

if __name__ == '__main__':
    root = Tk()
    app = WordGraphApp(root)
    root.mainloop()
