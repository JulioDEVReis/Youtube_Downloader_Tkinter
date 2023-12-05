# Youtube_Downloader_Tkinter

Demanda para uma cliente que pediu um aplicativo desktop capaz de baixar de uma só vez todos os vídeos de uma determinada playlist do Youtube automaticamente.

Para realizar essa demanda procurei um Framework que pudesse atender todos os requisitos da cliente e ainda ser leve. O Tkinter era uma boa opção principalmente porque estava bem familiarizado, já que usei com alguns projetos da escola de programação.

Criei então a janela, na cor pedida pela cliente, e inclui a possibilidade de downloads em 720p ou 1080p, tanto para links de vídeos como para links de playlists no youtube. Ainda coloquei também, por iniciativa propria, a funcionalidade de baixar todos os vídeos de um determinado canal no Youtube, bastando ter o link do canal do youtuber.

A primeira função que executo no aplicativo, importante no processo para evitar um dos erros que aconteceram durante o teste, é o de teste de conectividade da internet, onde uso o método try/except justamente para tentar conectar a internet e avisar a cliente, caso isso não seja possível.

Dessa forma, minhas funções que executam ações para baixar os vídeos executam a função de conectividade antes de qualquer outra ação.

![Youtube_downloader](https://github.com/JulioDEVReis/Youtube_Downloader_Tkinter/assets/142347463/f042de3b-d089-421e-a503-18d70e298511)

## Dificuldades e Soluções:

- Várias exceções aconteceram ao longo do projeto, e que precisei tratar com try/except justamente para não interromper a execução do aplicativo por falta de conectividade na internet, ou porque o link da playlist está incompleta ou é inexistente, ou ainda porque algum determinado vídeo dentro da playlist foi removido pelo youtuber.

## Tecnologias Usadas:

- tkinter (Framework usado para o aplicativo, por ser leve e simples)
- requests (para testar a conectividade da internet antes de seguir e fazer os downloads dos videos)
- Pytube (API usada para realizar os downloads dos vídeos de uma playlist do Youtube)
