
import tkinter

def ranking_window(self, data):
   ranking_window = tkinter.Toplevel(self.root)
   # TODO:名字
   # TODO: 出现的位置
   # ranking_window.title = 'rank'
   for i in range(len(data)):
      score = data[i][1]
      name = data[i][2]
      label_id = tkinter.Label(ranking_window, text=i + 1, width=5)
      label_name = tkinter.Label(ranking_window, text=name, width=10)
      label_score = tkinter.Label(ranking_window, text=score, width=10)
      label_id.grid(row=i, column=0)
      label_name.grid(row=i, column=1)
      label_score.grid(row=i, column=2)
   
