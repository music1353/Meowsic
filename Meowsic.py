# coding: utf-8

import youtube_dl
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import os

class MeowsicGUI:
    def __init__(self, root):
        # set root
        self.root = root
        root.resizable(False,False)
        root.title("Meowsic v4.1")
        root.iconbitmap('F:/Meowsic_square.ico')
        root.geometry("650x250")
        
        # set ing_root
        ing_root = Toplevel(root)
        ing_root.title("Downloading")
        ing_root.resizable(False,False)
        ing_root.iconbitmap('F:/d.ico')
        ing_root.geometry("245x0")
        ing_root.withdraw()
        
        # set menu
        menubar = Menu(root)
        filemenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="關於", menu=filemenu)
        filemenu.add_command(label="使用手冊", command=lambda:self.set_menu_use(root))
        filemenu.add_command(label='版本資訊', command=lambda:self.set_menu_version(root))
        root.config(menu=menubar) #把menu裝上去
        
        # set 右鍵功能
        rightClick_menu = Menu(root, tearoff=0)
        rightClick_menu.add_command(label="貼上 (Ctrl+V)", command=lambda:self.set_Paste(root, url))
        rightClick_menu.add_separator() #線
        rightClick_menu.add_command(label="清除", command=lambda:self.set_Delete(root, url))
        
        # set rightClick_menu的位置
        def popupmenu(event):
            rightClick_menu.post(event.x_root,event.y_root)
    
        # set input url
        downPath_label = ttk.Label(root, text="請輸入影片網址：")
        downPath_label.place(x=40, y=30)
        url = StringVar() #StringVar是Tk庫内部定義的字符串變量類型
        downPath_entry = ttk.Entry(root, width=50, textvariable=url) #網址輸入框
        downPath_entry.place(x=150, y=30)
        downPath_entry.bind("<Button-3>", popupmenu) #綁定滑鼠右鍵
        
        # set enter button
        pathOk_button = ttk.Button(root, text="確認", width=7, command=lambda:self.click_ok_button(root, url, ing_root))
        pathOk_button.place(x=520, y=27.5)
        
    def set_Paste(self, root, url):
        # 防止因為黏貼板沒有內容而報錯
        try:
            text = root.clipboard_get() # 獲得系統黏貼板內容
        except TclError:
            pass
        url.set(url.get()+str(text))
     
    def set_Delete(self, root, url):
        try:
            text = ''
            # 刪除文本框中從第一個到最后一個字符
        except TclError:
            pass
        url.set(str(text))
    
    def set_menu_use(self, root):
        useroot = Toplevel(root)
        useroot.resizable(False,False)
        useroot.title("使用手冊")
        useroot.iconbitmap('F:/Meowsic_square.ico')
        useroot.geometry("375x125")
        oneLabel = Label(useroot, text='step1.   將影片網址複製到網址欄，並按下[確認]').place(x=20, y=20)
        twoLabel = Label(useroot, text='step2.   選取愈下載的格式，並按下[下載]選擇要存取的位置').place(x=20, y=40)
        threeLabel = Label(useroot, text='step3.   等待下載完成').place(x=20, y=60)
        fourLabel = Label(useroot, text='step4.   享受影片&音樂').place(x=20, y=80)
        
    def set_menu_version(self, root):
        versionroot = Toplevel(root)
        versionroot.resizable(False,False)
        versionroot.title('版本資訊')
        versionroot.iconbitmap('F:/Meowsic_square.ico')
        versionroot.geometry("375x180")
        oneLabel = Label(versionroot, text='程式名稱：   Meowsic 影片&音樂下載器(For Win10)').place(x=40, y=20)
        twoLabel = Label(versionroot, text='版本：  4.1').place(x=40, y=40)
        threeLabel = Label(versionroot, text='開發平台：  python3.6').place(x=40, y=60)
        fourLabel = Label(versionroot, text='影音支援格式：  mp3, mp4').place(x=40, y=80)
        fiveLabel = Label(versionroot, text='影音支援平台：  youtube, bilibili, 愛奇藝, Dailymotion,').place(x=40, y=100)
        five2Label = Label(versionroot, text='Xuite隨意窩, Facebook, Twitter, niconico').place(x=130, y=120)
        sixLabel = Label(versionroot, text='作者：  ㄈㄓ貝爾').place(x=40, y=140)
    
    # 按下pathOK_button時執行
    def click_ok_button(self, root, url, ing_root):
        if( url.get()==''):
            messagebox.showerror('Error', '請輸入網址')
            
        # 處理niconico影片
        elif "nicovideo" in url.get():
            print('niconico')
            self.loginNico(root, url, ing_root) # 登入nico帳戶視窗
            
        else:
            info_dict = videoInfo.getInfo_dict(url)
            video_title = videoInfo.getVideoTitle(info_dict)
            video_formatList = videoInfo.setFormatList(info_dict)
            
            # 顯示影片名稱
            vNameSay = ttk.Label(root, text='影片名稱：').place(x=75, y=70)
            videoName_label = ttk.Label(root, text=video_title, width=len(video_title)+200)
            videoName_label.place(x=145, y=70) 
    
            vQSay = ttk.Label(root, text='檔案格式：').place(x=75, y=110)
            QChosen = ttk.Combobox(root) # 下拉列表
            QChosen.state(['readonly'])
            QChosen['values'] = video_formatList # 影片格式放入combobox
            QChosen.place(x=145, y=100, width=200, height=40)  # 設置下拉列表位置
            QChosen.current(0) # 設置下拉列表默認的初始值
            
            saveButton = ttk.Button(root, text='下載', width=7, command=lambda:self.click_saveButton(root, QChosen, video_title, url, ing_root))
            saveButton.place(x=380, y=105)
            
    def loginNico(self, root, url, ing_root):
        loginroot = Toplevel(root)
        loginroot.resizable(False,False)
        loginroot.title("登入Nico")
        loginroot.iconbitmap('F:/Meowsic_square.ico')
        loginroot.geometry("300x125")
        loginNico_label = ttk.Label(loginroot, text="登入您Nico帳戶")
        loginNico_label.place(x=40, y=20)
        username = StringVar() # StringVar是Tk庫内部定義的字符串變量類型
        password = StringVar() # StringVar是Tk庫内部定義的字符串變量類型
        loginNico_username_label = ttk.Label(loginroot, text="帳號:")
        loginNico_username_entry = ttk.Entry(loginroot, width=20, textvariable=username) # Nico帳號輸入框
        loginNico_password_label = ttk.Label(loginroot, text="密碼:")
        loginNico_password_entry = ttk.Entry(loginroot, width=20, textvariable=password) # Nico密碼輸入框
        loginNico_username_label.place(x=40, y=50)
        loginNico_username_entry.place(x=80, y=50)
        loginNico_password_label.place(x=40, y=80)
        loginNico_password_entry.place(x=80, y=80)
    
        confirmButton = ttk.Button(loginroot, width=5, text='確認', command=lambda:self.confirmNicoAccount(root, url, ing_root, loginroot, username, password))
        confirmButton.place(x=235, y=78)
        
    def confirmNicoAccount(self, root, url, ing_root, loginroot, username, password):
        nicoUsername = username.get()
        nicoPassword = password.get()
    
        loginroot.destroy()
    
        ydl_opts = {
               'username': nicoUsername,
               'password': nicoPassword,
        }

        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url.get(), download=False)
                video_title = info_dict.get('title', None)
        except:
            messagebox.showerror('Error', 'Nico帳號或密碼錯誤') 
        else:
            #把提供的format放進F_list
            F=[]
            F.append('nicovideo最佳畫質(mp4)')
            F.append('音樂檔(mp3)')        
            
            vNameSay = ttk.Label(root, text='影片名稱：').place(x=75, y=70)
            videoName_label = ttk.Label(root, text=video_title, width=len(video_title)+200).place(x=145, y=70) # 顯示影片名稱
    
            vQSay = ttk.Label(root, text='檔案格式：').place(x=75, y=110)
            QChosen = ttk.Combobox(root) # 下拉列表
            QChosen.state(['readonly'])
            QChosen['values'] = F # 影片格式放入combobox
        
            print(F)
            QChosen.place(x=145, y=100, width=200, height=40)  # 設置下拉列表位置
            QChosen.current(0) # 設置下拉列表默認的初始值
    
            nicoSaveButton = ttk.Button(root, text='下載', width=7, command=lambda:self.nico_save(root, QChosen, video_title, ing_root, url, nicoUsername, nicoPassword))
            nicoSaveButton.place(x=380, y=105)
            
    # 按下saveButton時執行
    def click_saveButton(self, root, QChosen, video_title, url, ing_root):
        if(QChosen.get()=='音樂檔(mp3)'):
            targetPath = filedialog.asksaveasfilename(title='儲存位置', initialdir='C:/', initialfile=video_title, defaultextension='.mp3', filetypes=[('mp3', '*.mp3')])
            if(targetPath==''):
                print('沒選存取位置')
            else:
                mp3_opts = downloadInfo.setMP3_opts(targetPath)
                downloadInfo.setDownloadingSurface(root, ing_root)
                try:
                    downloadInfo.doDownload(mp3_opts, url)
                except:
                    downloadInfo.setDownloadErrorSurface(root, ing_root)
                else:
                    downloadInfo.setDownloadCompleteSurface(root, ing_root)
                    
        elif(QChosen.get()=='youtube影片(mp4-1080p)'):
            targetPath = filedialog.asksaveasfilename(title='儲存位置', initialdir='C:/', initialfile=video_title, defaultextension='.mp4', filetypes=[('mp4', '*.mp4')])
            if(targetPath==''):
                print('沒選存取位置')
            else:
                mp41080_opts = downloadInfo.setYT1080Pvideo_opts(targetPath)
                downloadInfo.setDownloadingSurface(root, ing_root)
                try:
                    downloadInfo.doDownload(mp41080_opts, url)
                except:
                    downloadInfo.setDownloadErrorSurface(root, ing_root)
                else:
                    downloadInfo.setDownloadCompleteSurface(root, ing_root)
                               
        elif(QChosen.get()=='youtube影片(mp4-1440p)'):
            targetPath = filedialog.asksaveasfilename(title='儲存位置', initialdir='C:/', initialfile=video_title, defaultextension='.mp4', filetypes=[('mp4', '*.mp4')])
            if(targetPath==''):
                print('沒選存取位置')
            else:
                mp41440_opts = downloadInfo.setYT1440Pvideo_opts(targetPath)
                downloadInfo.setDownloadingSurface(root, ing_root)
                try:
                    downloadInfo.doDownload(mp41440_opts, url)
                except:
                    downloadInfo.setDownloadErrorSurface(root, ing_root)
                else:
                    downloadInfo.setDownloadCompleteSurface(root, ing_root)
                    
        elif(QChosen.get()=='youtube影片(mp4-4K)'):
            targetPath = filedialog.asksaveasfilename(title='儲存位置', initialdir='C:/', initialfile=video_title, defaultextension='.mp4', filetypes=[('mp4', '*.mp4')])
            if(targetPath==''):
                print('沒選存取位置')
            else:
                mp44K_opts = downloadInfo.setYT4Kvideo_opts(targetPath)
                downloadInfo.setDownloadingSurface(root, ing_root)
                try:
                    downloadInfo.doDownload(mp44K_opts, url)
                except:
                    downloadInfo.setDownloadErrorSurface(root, ing_root)
                else:
                    downloadInfo.setDownloadCompleteSurface(root, ing_root)
                    
        else:
            targetPath = filedialog.asksaveasfilename(title='儲存位置', initialdir='C:/', initialfile=video_title, defaultextension='.mp4', filetypes=[('mp4', '*.mp4')])
            if(targetPath==''):
                print('沒選存取位置')
            else:
                ydl_opts = downloadInfo.setVideo_opts(targetPath, QChosen)
                downloadInfo.setDownloadingSurface(root, ing_root)
                try:
                    downloadInfo.doDownload(ydl_opts, url)
                except:
                    downloadInfo.setDownloadErrorSurface(root, ing_root)
                else:
                    downloadInfo.setDownloadCompleteSurface(root, ing_root)
                    
    def nico_save(self, root, QChosen, video_title, ing_root, url, nicoUsername, nicoPassword):
        # 特別處理mp3
        if(QChosen.get()=='音樂檔(mp3)'):
            targetPath = filedialog.asksaveasfilename(title='儲存位置', initialdir='C:/', initialfile=video_title, defaultextension='.mp3', filetypes=[('mp3', '*.mp3')])
            if(targetPath==''):
                print('沒選存取位置')
            else:
                ydl_opts = downloadInfo.setNicoMP3_opts(targetPath, nicoUsername, nicoPassword)
                downloadInfo.setDownloadingSurface(root, ing_root)
                try:
                    downloadInfo.doDownload(ydl_opts, url)
                except:
                    downloadInfo.setDownloadErrorSurface(root, ing_root)
                else:
                    downloadInfo.setDownloadCompleteSurface(root, ing_root)
                    
        elif(QChosen.get()=='nicovideo最佳畫質(mp4)'):
            targetPath = filedialog.asksaveasfilename(title='儲存位置', initialdir='C:/', initialfile=video_title, defaultextension='.mp4', filetypes=[('mp4', '*.mp4')])
            if(targetPath==''):
                print('沒選存取位置')
            else:
                ydl_opts = downloadInfo.setNicovideo_opts(targetPath, nicoUsername, nicoPassword)
                downloadInfo.setDownloadingSurface(root, ing_root)
                try:
                    downloadInfo.doDownload(ydl_opts, url)
                except:
                    downloadInfo.setDownloadErrorSurface(root, ing_root)
                else:
                    downloadInfo.setDownloadCompleteSurface(root, ing_root)    
                
class videoInfo:
    def __init__(self, url):
        self.url = url
        
    def getInfo_dict(url):
        with youtube_dl.YoutubeDL() as ydl:
            info_dict = ydl.extract_info(url.get(), download=False)
        return info_dict
    
    def getVideoTitle(info_dict):
        video_title = info_dict.get('title', None)
        return video_title
    
    def setFormatList(info_dict):
        # 影片格式字典
        format_d = {# youtube
                    '18':'youtube影片(mp4-360p)',
                    '22':'youtube影片(mp4-720p)',
                    '137':'youtube影片(mp4-1080p)',
                    '264':'youtube影片(mp4-1440p)',
                    '266':'youtube影片(mp4-4K)',
                    # bilibili+愛奇藝
                    '0':'影片檔-流暢(mp4)',
                    '1':'影片檔-高清(mp4)',
                    '2':'影片檔-超清(mp4)',
                    # 愛奇藝
                    '4':'影片檔-藍光(mp4-1080p)',
                    # Dailymotion
                    'http-144':'Dailymotion影片(mp4-144p)',
                    'http-240':'Dailymotion影片(mp4-240p)',
                    'http-380':'Dailymotion影片(mp4-380p)',
                    'http-480':'Dailymotion影片(mp4-480p)',
                    'http-720':'Dailymotion影片(mp4-720p)',
                    'http-1080':'Dailymotion影片(mp4-1080p)',
                    # Facebook
                    'dash_sd_src_no_ratelimit':'Facebook影片-標清SD(mp4)',
                    'dash_hd_src_no_ratelimit':'Facebook影片-高清HD(mp4)',
                    # 隨意窩Xuite影音
                    '360':'Xuite影片(mp4-360p)',
                    '720':'Xuite影片(mp4-720p)',
                    # Twitter影片
                    'hls-320':'Twitter影片(mp4-180p)',
                    'hls-832':'Twitter影片(mp4-360p)',
                    'hls-2176':'Twitter影片(mp4-720p)'}
        
        video_format = info_dict.get('formats', None)
            
        FormatList = []
        for i in range( len(video_format) ):
            if video_format[i]['format_id'] in format_d:
                FormatList.append( format_d[ video_format[i]['format_id'] ])
        FormatList.append('音樂檔(mp3)')
        
        return FormatList

    
class downloadInfo:
    def __init__(self, targetPath, root, ing_root, QChosen, nicoUsername, nicoPassword):
        self.targetPath = targetPath
        self.root = root
        self.ing_root = ing_root
        self.QChosen = QChosen
        self.nicoUsername = nicoUsername
        self.nicoPassword = nicoPassword
    
    def setMP3_opts(targetPath):
        ydl_opts = {
            'outtmpl': targetPath,
            'format': 'bestaudio[acodec=opus]/best',
            'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
            }],
        }
        return ydl_opts
    
    def setYT1080Pvideo_opts(targetPath):
        ydl_opts = {
            'outtmpl': targetPath,
            'format': '137+bestaudio[ext=m4a]',
        }
        return ydl_opts
    
    def setYT1440Pvideo_opts(targetPath):
        ydl_opts = {
            'outtmpl': targetPath,
            'format': '264+bestaudio[ext=m4a]',
        }
        return ydl_opts
    
    def setYT4Kvideo_opts(targetPath):
        ydl_opts = {
            'outtmpl': targetPath,
            'format': '266+bestaudio[ext=m4a]',
        }
        return ydl_opts
    
    def setNicoMP3_opts(targetPath, nicoUsername, nicoPassword):
        ydl_opts = {
            'outtmpl': targetPath,
            'username': nicoUsername,
            'password': nicoPassword,
            'format': 'bestaudio/best',
            'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
            }],
        }
        return ydl_opts
    
    def setNicovideo_opts(targetPath, nicoUsername, nicoPassword):
        ydl_opts = {
            'outtmpl': targetPath,
            'username': nicoUsername,
            'password': nicoPassword,
            'format': 'best'
        }
        return ydl_opts
    
    def setVideo_opts(targetPath, QChosen):
        ftocode_d = {#youtube
                     'youtube影片(mp4-360p)':'18',
                     'youtube影片(mp4-720p)':'22',
                     #bilibili+愛奇藝
                     '影片檔-流暢(mp4)':'0',
                     '影片檔-高清(mp4)':'1',
                     '影片檔-超清(mp4)':'2',
                     #愛奇藝
                     '影片檔-藍光(mp4-1080p)':'4',
                     #Dailymotion
                     'Dailymotion影片(mp4-144p)':'http-144',
                     'Dailymotion影片(mp4-240p)':'http-240',
                     'Dailymotion影片(mp4-380p)':'http-380',
                     'Dailymotion影片(mp4-480p)':'http-480',
                     'Dailymotion影片(mp4-720p)':'http-720',
                     'Dailymotion影片(mp4-1080p)':'http-1080',
                     #Facebook
                     'Facebook影片-標清SD(mp4)':'dash_sd_src_no_ratelimit',
                     'Facebook影片-高清HD(mp4)':'dash_hd_src_no_ratelimit',
                     #隨意窩Xuite影音
                     'Xuite影片(mp4-360p)':'360',
                     'Xuite影片(mp4-720p)':'720',
                     #Twitter影片
                     'Twitter影片(mp4-180p)':'hls-320',
                     'Twitter影片(mp4-360p)':'hls-832',
                     'Twitter影片(mp4-720p)':'hls-2176'}
        
        ydl_opts = {
            'outtmpl': targetPath,
            'format': ftocode_d[QChosen.get()],
        }
        return ydl_opts
    
    def setDownloadingSurface(root, ing_root):
        print('setDownloadingSurface')
        root.withdraw() #隱藏根面板
        ing_root.update()
        ing_root.deiconify()
        
    def setDownloadErrorSurface(root, ing_root):
        messagebox.showerror('Error', '下載錯誤')
        ing_root.withdraw()
        root.update() #再顯示root面板
        root.deiconify()
        print('影片下載錯誤')
        
    def setDownloadCompleteSurface(root, ing_root):
        messagebox.showinfo('Complete', '下載完成!')
        ing_root.withdraw()
        root.update() #再顯示root面板
        root.deiconify()
        print('完成')
        
    def doDownload(ydl_opts, url):
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url.get()])
            
        
def main(): 
    root = Tk()
    meowsic_app = MeowsicGUI(root)
    root.mainloop()
    

if __name__ == '__main__':
    os.environ['PATH'] = os.environ['PATH']+os.path.abspath('.')+r'\ffmpeg\bin'
    print(os.environ['PATH'])
    main()