
import tkinter

def ranking_window(self, data):
   '''渲染排行榜页面'''
   # 创建子窗口
   ranking_window = tkinter.Toplevel(self.root)
   # 窗口不可拉伸
   ranking_window.resizable(0, 0)

   # label显示记录
   for i in range(len(data)):
      score = data[i][1]
      name = data[i][2]
      label_id = tkinter.Label(ranking_window, text=i + 1, width=5)
      label_name = tkinter.Label(ranking_window, text=name, width=15, anchor='nw')
      label_score = tkinter.Label(ranking_window, text=score, width=10)
      label_id.grid(row=i, column=0)
      label_name.grid(row=i, column=1)
      label_score.grid(row=i, column=2)

   # 窗口显示位置
   ranking_window.withdraw()
   ranking_window.update_idletasks()
   x = (ranking_window.winfo_screenwidth() - ranking_window.winfo_reqwidth()) / 2
   y = (ranking_window.winfo_screenheight() - ranking_window.winfo_reqheight()) / 2
   ranking_window.geometry('+%d+%d' % (x, y))
   ranking_window.deiconify()

