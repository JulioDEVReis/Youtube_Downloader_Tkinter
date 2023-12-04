import tkinter
from tkinter import *
from tkinter import messagebox, ttk
import requests
from pytube import YouTube, Playlist, Channel, Search


class Application:
    def __init__(self):
        self.root = root
        self.janela()
        self.widgets_frame1()
        # self.widgets_frame2()
        self.menu_app()

    def janela(self):
        self.root.title('Youtube Downloader')
        self.root.configure(background='#ffcccc')
        self.root.geometry('1200x800')
        self.root.resizable(False, False)
        # Frames do Ecrã
        self.frame1 = Frame(self.root, bd=4, highlightbackground='#FF9999', highlightthickness=2)
        self.frame1.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.25)
        self.frame2 = Frame(self.root, bd=4, highlightbackground='#FF9999', highlightthickness=2)
        self.frame2.place(relx=0.05, rely=0.33, relwidth=0.9, relheight=0.61)

    def widgets_frame1(self):
        self.label_frame1 = Label(self.frame1, text='Youtube Downloader', font=('verdana', 14, 'bold'))
        self.label_frame1.place(relx=0.385, rely=0.07)
        # Botão para baixar apenas um video no youtube
        self.botao_baixar_video = Button(self.frame1, text="Baixar um Vídeo", command=self.youtube_video_download)
        self.botao_baixar_video.place(relx=0.08, rely=0.32, relwidth=0.17)
        # Botão para baixar todos os videos de uma playlist
        self.botao_baixar_playlist = Button(self.frame1, text="Baixar toda Playlist", command=self.youtube_playlist_download)
        self.botao_baixar_playlist.place(relx=0.30, rely=0.32, relwidth=0.17)
        # Botão para baixar todos os vídeos de um canal
        self.botao_baixar_canal = Button(self.frame1, text="Baixar vídeos do Canal",command=self.youtube_channel_download)
        self.botao_baixar_canal.place(relx=0.52, rely=0.32, relwidth=0.17)
        # Botão de pesquisa no Youtube
        self.botao_procurar = Button(self.frame1, text="Procurar Vídeo no Youtube", command=self.pesquisar_youtube)
        self.botao_procurar.place(relx=0.74, rely=0.32, relwidth=0.17)

    def widgets_frame2(self):
        # Criação da Scrool Bar
        self.scrool_frame = Scrollbar(self.frame_2, orient='vertical')
        self.lista_search.configure(yscroolcommand=self.scrool_frame.set)
        self.scrool_frame.place(relx=0.96, rely=0.1, relwidth=0.04, relheight=0.85)
        # Fazer um link entre o duplo clique e a lista search do youtube
        self.lista_search.bind("<Double-1>", self.OnDoubleClick)

    def menu_app(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        filemenu = Menu(menubar)

        # criando uma função para sair do app
        def quit():
            self.root.destroy()

        # criando uma função para apagar a entry
        def apagar_entry():
            self.entry_link_video.delete(0, END)

        # Adicionando as labels do menu
        menubar.add_cascade(label="Opções", menu=filemenu)
        # Adicionando os comandos a label
        filemenu.add_command(label="Limpar campo do link", command=apagar_entry)
        filemenu.add_command(label="Sair", command=quit)

    def OnDoubleClick(self, event):  # importante que tenha o evento para que funcione
        self.entry_link_video.delete(0, END)
        self.lista_search.selection()  # para a seleção que for feita na tabela ser capturada

        for n in self.lista_search.selection():  # iterar sobre seleção e suas colunas
            col1, col2, col3, col4 = self.lista_search.item(n, 'values')  # atribuir uma coluna a cada valor
            self.entry_link_video.insert(END, col1)  # Atribuir a coluna do link ao valor do entry

    def conectividade_internet(self):
        url='https://www.google.com/'
        timeout = 5
        try:
            req = requests.get(url, timeout=timeout)
            req.raise_for_status()
            print("You are connected to the internet!")
            return True

        except requests.HTTPError as e:
            print("Internet Connection failed, status code{0}".format(e.response.status_code))

        except requests.ConnectionError:
            print("No connection available")
            return False

    def youtube_video_download(self):
        # Entry para o link do Youtube
        self.label_entry_video = Label(self.frame1,
                                       text='Cole aqui o link do vídeo do Youtube que você quer baixar:')
        self.label_entry_video.place(relx=0.08, rely=0.56)
        self.entry_link_video = Entry(self.frame1)
        self.entry_link_video.place(relx=0.08, rely=0.67, relwidth=0.83)

        def baixar_agora_720p():
            if self.conectividade_internet():
                try:
                    print('recebendo o link que foi digitado')
                    link_youtube = self.entry_link_video.get()  # Usamos .get() para conseguir obter o valor colocado pelo usuário
                    print('tentando baixar o video')
                    # tentativa usando o pytube
                    yt_object_video = YouTube(link_youtube)
                    filters = yt_object_video.streams.filter(progressive=True, file_extension='mp4')  # streams lista todos os tipos de videos armazenados, adaptativos e progressivos, com itags para diferenciar um do outro. Cada itag possui tipo, resolução, fps, etc, diferentes.
                    filters.get_highest_resolution().download()  # com o get_highest_resolution podemos buscar a resolução 720p, maxima para progressive
                    # Limpar o frame 2
                    for widget in self.frame2.winfo_children():
                        widget.destroy()
                    mensagem_video1 = Label(self.frame2, text='Baixando o vídeo:')
                    mensagem_video1.place(relx=0.05, rely=0.02)
                    titulo_video = yt_object_video.title
                    mensagem_video2 = Label(self.frame2, text=titulo_video)
                    mensagem_video2.place(relx=0.05, rely=0.1)
                    descricao_video = yt_object_video.description
                    mensagem_video3 = Label(self.frame2, text=descricao_video)
                    mensagem_video3.place(relx=0.05, rely=0.15)
                    messagebox.showinfo('Atenção!', 'O vídeo já foi baixado com sucesso!')

                except Exception as e:
                    messagebox.showerror('Atenção!', 'Erro ao baixar vídeo.')
                    print(e)
            else:
                messagebox.showerror('Atenção!', 'Você está com problemas de conexão com a internet.')
            self.entry_link_video.delete(0, END)

        def baixar_agora_1080p():
            if self.conectividade_internet():
                try:
                    print('recebendo o link que foi digitado')
                    link_youtube = self.entry_link_video.get()
                    print(link_youtube)
                    print('tentando baixar o video')
                    # tentativa usando o pytube
                    yt_object_video = YouTube(link_youtube)
                    # Limpar o frame 2
                    for widget in self.frame2.winfo_children():
                        widget.destroy()
                    mensagem_video1 = Label(self.frame2, text='Baixando o vídeo e audio:')
                    mensagem_video1.place(relx=0.05, rely=0.02)
                    try:
                        filters_video = yt_object_video.streams.filter(adaptive=True, res="1080p", file_extension="mp4")
                        for videos in filters_video:
                            itag_video = videos.itag
                            filters_video.get_by_itag(itag_video).download()
                    except Exception as e:
                        messagebox.showerror('Atenção!',
                                             'Não há vídeo(s) em 1080p. Recomendo então usar o botão de baixar em 720p pois o audio já vem incorporado no arquivo de vídeo.')
                        print(e)
                    else:
                        print('video ok - baixado')

                    filters_audio = yt_object_video.streams.filter(adaptive=True, abr='160kbps')
                    print(filters_audio)
                    for audios in filters_audio:
                        itag_audio = audios.itag
                        filters_audio.get_by_itag(itag_audio)
                    print('audio ok - baixado')

                    titulo_video = yt_object_video.title
                    mensagem_video2 = Label(self.frame2, text=titulo_video)
                    mensagem_video2.place(relx=0.05, rely=0.1)
                    descricao_video = yt_object_video.description
                    mensagem_video3 = Label(self.frame2, text=descricao_video)
                    mensagem_video3.place(relx=0.05, rely=0.15)
                    messagebox.showinfo('Atenção!', 'O vídeo e áudio já foram baixados com sucesso! Foram 2 arquivos separados, um de vídeo e outro de audio, que precisam ser juntados em um App de edição.')

                except Exception as e:
                    messagebox.showerror('Atenção!', 'Erro ao tentar baixar os arquivos. Tente novamente ou tente um novo link')
                    print(e)
            else:
                messagebox.showerror('Atenção!', 'Você está com problemas de conexão com a internet.')
            self.entry_link_video.delete(0, END)

        # Botão para ativar a função baixar_agora_720p()
        self.botao_baixar_link_video_720 = Button(self.frame1, text='Baixar agora em 720p!', command=baixar_agora_720p)
        self.botao_baixar_link_video_720.place(relx=0.08, rely=0.80, relwidth=0.17)
        # Botão para ativar a função baixar_agora_1080p()
        self.botao_baixar_link_video_1080 = Button(self.frame1, text='Baixar agora em 1080p!', command=baixar_agora_1080p)
        self.botao_baixar_link_video_1080.place(relx=0.3, rely=0.80, relwidth=0.17)


    def youtube_playlist_download(self):
        # Entry para o link do Youtube
        self.label_entry_playlist = Label(self.frame1,
                                       text='Cole aqui o link da playlist do Youtube que você quer baixar:')
        self.label_entry_playlist.place(relx=0.08, rely=0.56)
        self.entry_link_playlist = Entry(self.frame1)
        self.entry_link_playlist.place(relx=0.08, rely=0.67, relwidth=0.83)

        def baixar_agora_720p():
            if self.conectividade_internet():
                try:
                    print('recebendo o link que foi digitado')
                    link_youtube = self.entry_link_playlist.get()  # Usamos .get() para conseguir obter o valor colocado pelo usuário
                    print(link_youtube)
                    print('tentando baixar a playlist')
                    # tentativa usando o pytube
                    yt_object_playlist = Playlist(link_youtube)
                    print(yt_object_playlist)
                    print(yt_object_playlist.video_urls)  # Mesma coisa que apenas imprimir a variavel yt_object_playlist, são instâncias de classe
                    print(yt_object_playlist.videos)  # Instância da classe Youtube
                    tamanho_playlist = len(yt_object_playlist.videos)
                    print(f"A playlist tem {tamanho_playlist} vídeos")
                    # Limpar o frame 2
                    for widget in self.frame2.winfo_children():
                        widget.destroy()
                    mensagem_video1 = Label(self.frame2, text='Baixando os vídeos da playlist:')
                    mensagem_video1.place(relx=0.05, rely=0.02)
                    for video in yt_object_playlist.videos:
                        print(video.title)
                        rely = 0.1
                        titulo_video = video.title
                        mensagem_video2 = Label(self.frame2, text=titulo_video)
                        mensagem_video2.place(relx=0.05, rely=rely)
                        rely += 0.1
                        filters = video.streams.filter(progressive=True, file_extension='mp4')  # streams lista todos os tipos de videos armazenados, adaptativos e progressivos, com itags para diferenciar um do outro. Cada itag possui tipo, resolução, fps, etc, diferentes.
                        filters.get_highest_resolution().download()  # com o get_highest_resolution podemos buscar a resolução 720p, maxima para progressive
                    messagebox.showinfo('Atenção!', 'Os vídeos já foram baixados com sucesso!')

                except Exception as e:
                    messagebox.showerror('Atenção!', 'Erro ao tentar baixar algum dos vídeo da Playlist.')
                    print(e)
            else:
                messagebox.showerror('Atenção!', 'Você está com problemas de conexão com a internet.')
            self.entry_link_playlist.delete(0, END)

        def baixar_agora_1080p():
            if self.conectividade_internet():
                try:
                    print('recebendo o link que foi digitado')
                    link_youtube = self.entry_link_playlist.get()
                    print('tentando baixar a playlist')
                    print(link_youtube)
                    # tentativa usando o pytube
                    yt_object_playlist = Playlist(link_youtube)
                    print(yt_object_playlist)
                    print(yt_object_playlist.video_urls)  # Mesma coisa que apenas imprimir a variavel yt_object_playlist, são instâncias de classe
                    print(yt_object_playlist.videos)  # Instância da classe Youtube
                    tamanho_playlist = len(yt_object_playlist.videos)
                    print(f"A playlist tem {tamanho_playlist} vídeos")
                    # Limpar o frame 2
                    for widget in self.frame2.winfo_children():
                        widget.destroy()
                    mensagem_video1 = Label(self.frame2, text='Baixando os vídeos da Playlist:')
                    mensagem_video1.place(relx=0.05, rely=0.02)
                    for video in yt_object_playlist.videos:
                        print(video.title)
                        try:
                            filters_video = video.streams.filter(adaptive=True, res="1080p", file_extension="mp4")
                            for videos in filters_video:
                                itag_video = videos.itag
                                filters_video.get_by_itag(itag_video).download()
                                rely = 0.1
                                titulo_video = yt_object_playlist.title
                                mensagem_video2 = Label(self.frame2, text=titulo_video)
                                mensagem_video2.place(relx=0.05, rely=rely)
                                rely += 0.1
                        except Exception as e:
                            messagebox.showerror('Atenção!',
                                                 'Não há vídeo(s) em 1080p. Recomendo então usar o botão de baixar em 720p pois o audio já vem incorporado no arquivo de vídeo.')
                            print(e)
                        else:
                            print(f'video {videos} ok - baixado')

                    for audio in yt_object_playlist.videos:
                        filters_audio = audio.streams.filter(adaptive=True, abr='160kbps')
                        for audios in filters_audio:
                            itag_audio = audios.itag
                            filters_audio.get_by_itag(itag_audio)
                        print(f'audio {audios} ok - baixado')
                    messagebox.showinfo('Atenção!', 'Os vídeos e áudios já foram baixados com sucesso! Foram 2 arquivos separados para cada video da playlist, um de vídeo e outro de audio, que precisam ser juntados em um App de edição.')

                except Exception as e:
                    messagebox.showerror('Atenção!', 'Erro ao tentar baixar os arquivos. Tente novamente ou tente um novo link')
                    print(e)
            else:
                messagebox.showerror('Atenção!', 'Você está com problemas de conexão com a internet.')
            self.entry_link_playlist.delete(0, END)

        # Botão para ativar a função baixar_agora_720p()
        self.botao_baixar_link_video_720 = Button(self.frame1, text='Baixar agora em 720p!', command=baixar_agora_720p)
        self.botao_baixar_link_video_720.place(relx=0.08, rely=0.80, relwidth=0.17)
        # Botão para ativar a função baixar_agora_1080p()
        self.botao_baixar_link_video_1080 = Button(self.frame1, text='Baixar agora em 1080p!', command=baixar_agora_1080p)
        self.botao_baixar_link_video_1080.place(relx=0.3, rely=0.80, relwidth=0.17)

    def youtube_channel_download(self):
        # Entry para o link do Youtube
        self.label_entry_channel = Label(self.frame1,
                                       text='Cole aqui o link da playlist do Youtube que você quer baixar:')
        self.label_entry_channel.place(relx=0.08, rely=0.56)
        self.entry_link_channel = Entry(self.frame1)
        self.entry_link_channel.place(relx=0.08, rely=0.67, relwidth=0.83)

        def baixar_agora_720p():
            if self.conectividade_internet():
                try:
                    print('recebendo o link que foi digitado')
                    link_youtube = self.entry_link_channel.get()  # Usamos .get() para conseguir obter o valor colocado pelo usuário
                    print(link_youtube)
                    print('tentando baixar o canal')
                    # tentativa usando o pytube
                    yt_object_channel = Channel(link_youtube)
                    print(yt_object_channel)
                    print(yt_object_channel.video_urls)  # Mesma coisa que apenas imprimir a variavel yt_object_playlist, são instâncias de classe
                    print(yt_object_channel.videos)  # Instância da classe Youtube
                    tamanho_channel = len(yt_object_channel.videos)
                    print(f"O Canal tem {tamanho_channel} vídeos")
                    # Limpar o frame 2
                    for widget in self.frame2.winfo_children():
                        widget.destroy()
                    mensagem_video1 = Label(self.frame2, text='Baixando os vídeos do canal:')
                    mensagem_video1.place(relx=0.05, rely=0.02)
                    for video in yt_object_channel.videos:
                        print(video.title)
                        titulo_video = video.title
                        rely = 0.1
                        mensagem_video2 = Label(self.frame2, text=titulo_video)
                        mensagem_video2.place(relx=0.05, rely=rely)
                        rely += 0.1
                        filters = video.streams.filter(progressive=True, file_extension='mp4')  # streams lista todos os tipos de videos armazenados, adaptativos e progressivos, com itags para diferenciar um do outro. Cada itag possui tipo, resolução, fps, etc, diferentes.
                        filters.get_highest_resolution().download()  # com o get_highest_resolution podemos buscar a resolução 720p, maxima para progressive
                    messagebox.showinfo('Atenção!', 'Os vídeos já foram baixados com sucesso!')

                except Exception as e:
                    messagebox.showerror('Atenção!', 'Erro ao tentar baixar algum dos vídeo do Canal.')
                    print(e)
            else:
                messagebox.showerror('Atenção!', 'Você está com problemas de conexão com a internet.')
            self.entry_link_channel.delete(0, END)

        def baixar_agora_1080p():
            if self.conectividade_internet():
                try:
                    print('recebendo o link que foi digitado')
                    link_youtube = self.entry_link_channel.get()
                    print('tentando baixar a playlist')
                    print(link_youtube)
                    # tentativa usando o pytube
                    yt_object_channel = Channel(link_youtube)
                    print(yt_object_channel)
                    print(yt_object_channel.video_urls)  # Mesma coisa que apenas imprimir a variavel yt_object_playlist, são instâncias de classe
                    print(yt_object_channel.videos)  # Instância da classe Youtube
                    tamanho_channel = len(yt_object_channel.videos)
                    print(f"O Canal tem {tamanho_channel} vídeos")
                    # Limpar o frame 2
                    for widget in self.frame2.winfo_children():
                        widget.destroy()
                    for video in yt_object_channel.videos:
                        print(video.title)
                        try:
                            filters_video = video.streams.filter(adaptive=True, res="1080p", file_extension="mp4")
                            mensagem_video1 = Label(self.frame2, text='Baixando os vídeos e audios do Canal:')
                            mensagem_video1.place(relx=0.05, rely=0.02)
                            for videos in filters_video:
                                itag_video = videos.itag
                                filters_video.get_by_itag(itag_video).download()
                                titulo_video = yt_object_channel.title
                                rely = 0.1
                                mensagem_video2 = Label(self.frame2, text=titulo_video)
                                mensagem_video2.place(relx=0.05, rely=rely)
                                rely += 0.1
                        except Exception as e:
                            messagebox.showerror('Atenção!', 'Não há vídeo(s) em 1080p. Recomendo então usar o botão de baixar em 720p pois o audio já vem incorporado no arquivo de vídeo.')
                            print(e)
                        else:
                            print(f'video {videos} ok - baixado')
                    for audio in yt_object_channel.videos:
                        filters_audio = audio.streams.filter(adaptive=True, abr='160kbps')
                        for audios in filters_audio:
                            itag_audio = audios.itag
                            filters_audio.get_by_itag(itag_audio)
                        print(f'audio {audios} ok - baixado')
                    messagebox.showinfo('Atenção!', 'Os vídeos e áudios já foram baixados com sucesso! Foram 2 arquivos separados para cada video do Canal, um de vídeo e outro de audio, que precisam ser juntados em um App de edição.')

                except Exception as e:
                    messagebox.showerror('Atenção!', 'Erro ao tentar baixar os arquivos. Tente novamente ou tente um novo link')
                    print(e)
            else:
                messagebox.showerror('Atenção!', 'Você está com problemas de conexão com a internet.')
            self.entry_link_channel.delete(0, END)

        # Botão para ativar a função baixar_agora_720p()
        self.botao_baixar_link_video_720 = Button(self.frame1, text='Baixar agora em 720p!', command=baixar_agora_720p)
        self.botao_baixar_link_video_720.place(relx=0.08, rely=0.80, relwidth=0.17)
        # Botão para ativar a função baixar_agora_1080p()
        self.botao_baixar_link_video_1080 = Button(self.frame1, text='Baixar agora em 1080p!', command=baixar_agora_1080p)
        self.botao_baixar_link_video_1080.place(relx=0.3, rely=0.80, relwidth=0.17)

    def pesquisar_youtube(self):
        # Entry para a pesquisa no Youtube
        self.label_entry_search = Label(self.frame1,
                                         text='Digite no campo abaixo qual pesquisa gostaria de fazer no Youtube:')
        self.label_entry_search.place(relx=0.08, rely=0.56)
        self.entry_link_search = Entry(self.frame1)
        self.entry_link_search.place(relx=0.08, rely=0.67, relwidth=0.83)

        def pesquisar_agora():
            if self.conectividade_internet():
                try:
                    serch_youtube = self.entry_link_search.get()  # Usamos .get() para conseguir obter o valor colocado pelo usuário
                    yt_object_search = Search(serch_youtube)
                    # Limpar o frame 2
                    for widget in self.frame2.winfo_children():
                        widget.destroy()

                    # Adicionar titulos dos videos pesquisados no frame 2
                    rely = 0.08
                    for video in yt_object_search.results:
                        print(video)
                        label_search = Label(self.frame2, text=video.title)
                        label_search.place(relx=0.08, rely=rely)
                        rely += 0.05

                    # criar botão para pesquisar mais
                    yt_object_search.get_next_results()
                    print(yt_object_search.results)
                    # Inserir um campo de sugestões de pesquisa
                    print(yt_object_search.completion_suggestions)
                except Exception as e:
                    messagebox.showerror('Atenção!',
                                         'Não conseguimos encontrar resultados para os dados colocados. Favor alterar a pesquisa.')
                    print(e)

            else:
                messagebox.showerror('Atenção!', 'Você está com problemas de conexão com a internet.')
            self.entry_link_search.delete(0, END)

        # Botão para ativar a função pesquisar_agora()
        self.botao_pesquisar_agora = Button(self.frame1, text='Pesquisar!', command=pesquisar_agora)
        self.botao_pesquisar_agora.place(relx=0.08, rely=0.80, relwidth=0.17)


if __name__ == '__main__':
    root = Tk()
    app = Application()
    root.mainloop()