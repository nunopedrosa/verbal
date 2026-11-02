# Verbal — v1.3.1

Jogo de palavras instalável, local e offline. Palavras portuguesas de 4, 5, 6, 7 ou 8 letras, seis tentativas, desafio diário por tamanho, modo livre, estatísticas por tamanho e partilha sem revelar a resposta. Interface em português europeu e inglês. **Mudar a interface para inglês mantém as palavras portuguesas.** As respostas vêm de listas editoriais; as tentativas aceitam um vocabulário português alargado, incluindo plurais e conjugações. Não é um dicionário completo.

## Colocar no repositório

Extrair o conteúdo desta pasta para `/Users/nfp/github/pwa/verbal`, preservando o `.git` que já existe. Não copiar para uma subpasta adicional. O pacote não inclui a identidade ou autenticação do protótipo Sites.

```bash
cd /Users/nfp/github/pwa/verbal
python3 -m http.server 8000 --directory public
```

Abrir `http://localhost:8000`. Não é necessário instalar npm ou dependências. O service worker funciona em localhost ou HTTPS; `file://` não serve para testar a PWA. Para testar num iPhone, usar um alojamento HTTPS; HTTP através do endereço LAN do Mac não permite service workers.

Depois de verificar, fazer commit e push pelos meios habituais. Não foram feitos commits ou pushes no teu GitHub por esta entrega.

## DreamHost

Destino previsto: `https://verbal.basecentral.link`. Criar o domínio e HTTPS no painel. O checkout Git do servidor deve ficar **fora** do diretório público. Precisa de Bash 3+, Git, curl e sha256sum (ou shasum); nenhum runtime Python/Node/PHP é necessário no alojamento. Python 3 é usado apenas na preparação local da release.

No servidor, clonar o teu repositório e configurar uma branch com upstream, usando as tuas credenciais habituais. A partir desse checkout:

```bash
bash scripts/deploy.sh --dry-run /home/basecentral/verbal.basecentral.link
bash scripts/deploy.sh --verify /home/basecentral/verbal.basecentral.link
```

O diretório de destino deve já existir. Adaptar o caminho ao utilizador/domínio configurados. O script faz fetch e `git pull --ff-only`, recusa alterações locais, ficheiros não rastreados, branch detached, divergência ou commits apenas no servidor. Não altera credenciais e nunca faz reset/clean/stash/push.

Usa o mesmo motor Bash local da coleção (`scripts/deploy-core.sh`), com o contrato próprio em `scripts/deploy-profile.sh`. Publica apenas os 24 ficheiros de `PUBLIC_FILES`, todos presentes em `public/`. Valida a lista e os hashes SHA-256 de `scripts/deploy-hashes.txt` antes e depois da preparação. `--dry-run` só lê o inventário local: não faz fetch, pull, escritas ou verificações HTTP. `--verify` verifica HTTP após publicar. Sem argumento, o destino é `${DEPLOY_SITE:-$HOME/verbal.basecentral.link}`. `--no-pull` é reservado ao checkout cujo upstream já foi atualizado; o comando normal faz sempre fetch/pull. Se o pull alterar o motor ou perfil, o deploy recusa publicar até rever e executar novamente. Verifica fontes e destinos antes de publicar, recusa symlinks e diretórios sobrepostos, prepara cópias no destino e usa substituição atómica **por ficheiro**, com permissões 0644. O conjunto da publicação não é uma transação: uma falha durante as substituições pode deixar recursos de versões diferentes. `sw.js` é o último ficheiro, e a cache de instalação só fica pronta se todos os recursos forem obtidos e os seus hashes SHA-256 corresponderem à release. Publicar numa janela calma e voltar a executar após corrigir uma falha. Preserva ficheiros alheios e o `.htaccess` existente.

`hosting/dreamhost.htaccess` é um exemplo opcional. Rever e copiar manualmente para o webroot como `.htaccess`; o deploy não o instala nem substitui. A pasta hosting nunca deve ser pública. Não é preciso reescrever rotas: é uma aplicação de uma só página sem rotas no servidor.

## Dados, privacidade e portabilidade

Dados num só registo `verbal:data:v1` de localStorage. Sem conta, analytics, CDN ou transmissão de jogos. As respostas estão no código local: sem proteção contra batota. Dados pertencem ao dispositivo/navegador/origem; o protótipo privado e o domínio final não partilham armazenamento. O novo pacote não migra automaticamente dados do protótipo Letra.

Definições → Dados e cópias de segurança: exportar JSON antes de mudar de navegador/dispositivo ou limpar dados. O backup `format: verbal`, `schema: 1` inclui todos os jogos concluídos/em curso, rascunhos, preferências de modo/tamanho/idioma e contador do modo livre. Resultados e estatísticas são reconstruídos a partir desses jogos. Não inclui caches, permissões nem o momento da última exportação da sessão. Importação até 5 MiB/10 000 jogos, com validação e pré-visualização. **Substitui** a coleção; não faz fusão. Restaurar preferências vem marcado; desmarcar preserva as preferências atuais. Backups com outro formato/versão são recusados, sem modificação. Dados com falha de gravação podem ser exportados da sessão.

## Instalação, offline e atualizações

iPhone: Safari → Partilhar → Adicionar ao ecrã principal. Nos restantes navegadores, usar Instalar quando existir. A interface verifica os recursos antes de mostrar Pronto para jogar offline; sem service worker é possível jogar online, mas não há promessa de offline.

Definições → Procurar atualizações. Atualizar aplicação só aparece quando há uma versão instalada em espera. A ativação é explícita e preserva o progresso guardado; janelas com trabalho não gravado não são recarregadas automaticamente. Antes de cada release alterar VERSION em app.js e sw.js em conjunto. Executar `python3 scripts/prepare-release.py` depois de qualquer alteração aos recursos públicos e antes de fazer commit. Esta operação verifica a lista pública explícita e regenera `release.json`, o hash esperado pelo service worker e `scripts/deploy-hashes.txt`, sem dependências externas. Cada cache contém uma release completa; as anteriores são conservadas para janelas antigas e podem ocupar espaço. Não há remoção automática de dados ou caches para corrigir problemas.

## Palavras e testes

Listas em `public/words.js`, selecionadas manualmente para este projeto. Acentos/cedilhas são normalizados. As listas de respostas mantêm o conteúdo e a ordem publicados. As tentativas de todos os tamanhos usam `public/guesses.js`: 1 807 palavras de 4 letras, 6 429 de 5, 14 015 de 6, 26 311 de 7 e 41 339 de 8. **São aceites plurais e formas verbais válidos que constem da lista**, com o tamanho escolhido; não se acrescenta um S arbitrariamente. Acentos e cedilhas são normalizados, por exemplo MÃES → MAES. O vocabulário inclui formas pouco frequentes; a lista não promete aceitar todas as palavras portuguesas. O desafio usa uma função determinística da data em Lisboa e do tamanho; sem dependência de serviços externos.

```bash
node scripts/test-core.cjs
node scripts/test-paper.cjs
node scripts/test-variants.cjs
node scripts/test-variant-regressions.cjs
node scripts/test-vocabulary.cjs
node scripts/test-sw.cjs
python3 scripts/test-deploy.py
```

Os testes precisam de Node apenas na máquina de desenvolvimento; não no alojamento. Ver `docs/VERIFICATION.md` para evidência e limitações. Alvo: iPhone 6 / iOS 12.5.x / Safari 12. A compatibilidade com esse dispositivo físico ainda não foi verificada.

## Controlos partilhados e regressões de interface

A release 1.0.1 usa cópias locais de `shared-controls.css`, `shared-icons.svg` e `shared-chevron.svg`, com os desenhos SVG comuns embutidos nos botões. O teclado e as pistas do jogo mantêm o desenho específico da aplicação. O idioma usa o mesmo select nativo de bandeiras no cabeçalho e nas Definições; a mudança é imediata, sem trocar a resposta ou o rascunho. O tabuleiro adapta as células ao espaço disponível, com letras legíveis e intervalos de 2px; o teclado mantém três filas QWERTY sem quebra. Em ecrãs estreitos as teclas são mais estreitas que 44px, por decisão específica de 2026-11-02, mas mantêm 44px de altura. O modo e o tamanho ficam na mesma linha; o modal usa top/right/bottom/left compatíveis com Safari 12.

No checkout da coleção: `python3 ../pwa/scripts/sync-controls.py --check verbal` e `python3 ../pwa/scripts/sync-deploy.py --check verbal`. Para o teste opcional de navegador: instalar Playwright apenas no ambiente de desenvolvimento e executar `node scripts/test-browser.cjs`; `PLAYWRIGHT_PATH` pode indicar o módulo instalado e `CHROMIUM_PATH` um Chromium existente. Não são dependências da aplicação ou do alojamento.

## Origem e reprodução do vocabulário

`vendor/dictionary/` contém as fontes pt-PT do Projecto Natura, através de wooorm/dictionaries, fixadas na revisão `8cfea406b505e4d7df52d5a19bce525df98c54ab`. Para gerar as tentativas: `python3 scripts/build-vocabulary.py`, com Node, Hunspell e unmunch instalados apenas na máquina de desenvolvimento. Não faz pedidos de rede. Expande apenas entradas minúsculas sem pontuação/hífens, valida as formas expandidas com o Hunspell, normaliza acentos/cedilhas, filtra 4–8 letras, elimina duplicados e inclui todas as tentativas antigas. Não altera as respostas nem a seleção diária. O resultado está limitado a 1 MB (atualmente cerca de 729 kB, sem compressão) e fica totalmente disponível offline.

O ficheiro derivado `guesses.js` usa a opção MPL 1.1 da licença do dicionário. `public/dictionary-license.txt` inclui autoria, alterações, indicação das fontes e texto integral da licença; Como jogar tem uma ligação para esse ficheiro. Para atualizar fontes, rever a nova revisão e regenerar o vocabulário, testes e metadados da release. O alojamento não necessita de Hunspell nem de um serviço de dicionário.

## Variações — menu Jogos

- **Clássico:** mantém o desafio diário e o modo livre, de 4–8 letras e seis tentativas. As respostas diárias existentes não mudam.
- **Rigoroso:** seis tentativas que respeitam todas as pistas anteriores, incluindo posições proibidas e limites de letras repetidas. Tem progresso separado do Clássico; a resposta diária coincide.
- **Duas palavras:** duas respostas diferentes do mesmo tamanho, oito tentativas partilhadas. Palavra 1/2 alterna a grelha e as pistas do teclado em ecrãs compactos; em ecrãs largos veem-se ambas. Uma grelha resolvida deixa de mudar.
- **Temas:** natureza, comida ou objetos, com respostas selecionadas em cada tamanho. Qualquer tentativa portuguesa aceite continua a ser válida.
- **Progressivo:** uma série de cinco etapas, de 4 a 8 letras, com seis tentativas em cada. Uma vitória permite escolher Próximo tamanho; uma derrota termina a série. Há séries diárias e livres.
- **Escada de palavras:** muda exatamente uma letra por passo até ao destino mostrado, em até doze passos, sem repetir palavras. Os percursos têm soluções verificadas. A grelha mostra os passos recentes e Regras mostra todo o teu percurso.
- **Desafio a amigos:** escolhe uma palavra válida de 4–8 letras, cria a ligação e partilha-a explicitamente. Quem a abre confirma Jogar desafio e tem seis tentativas. A mesma ligação retoma o progresso anterior. A resposta está codificada no fragmento da ligação, sem conta ou servidor; não é proteção contra inspeção.
- **Uma pista:** quatro tentativas com uma letra fixa já revelada. A escrita salta essa posição e a letra é incluída automaticamente ao enviar.

Mudar de jogo, tamanho, tema ou idioma preserva os rascunhos de cada desafio. As estatísticas distinguem os modos; a partilha de resultados identifica a variação sem revelar a resposta. Progressivo e Desafio a amigos fixam o tamanho do desafio atual. O menu mantém Definições e Idioma juntos no topo. Em ecrãs muito curtos pode ser preciso deslocar a página; não se reduzem as letras a dimensões ilegíveis.

As novas entradas ficam numa extensão opcional `variants` do mesmo registo `verbal:data:v1`, mantendo `format: verbal`, `schema: 1`. Os jogos clássicos continuam em `games`. Os backups antigos são aceites como Clássico; os novos incluem todos os modos, etapas, rascunhos e preferências. A validação repete as jogadas e verifica respostas/identidades antes da substituição. O limite combinado é 10 000 jogos e 5 MiB por importação. Restaurar sem preferências mantém a seleção do dispositivo e pode reconstruir o desafio selecionado a partir da sua semente/ligação válida. Sem payload de amigo, regressa ao Clássico. Aplicações antigas não sabem jogar estas variações, embora possam conservar os campos adicionais.

Ficheiros principais: `variants.js` contém as regras puras e a validação; `challenges.js` contém temas e percursos; `app.js` gere a interface e a gravação atómica. Para a regressão de navegador adicional, executar `node scripts/test-variations-browser.cjs` com as mesmas variáveis Playwright/Chromium do teste existente. Não há novas dependências de execução.

Os temas e percursos publicados são definições estáveis dos desafios. Não alterar as listas/ordem em produção sem manter as definições antigas através de uma versão própria ou de uma migração explícita e testada.

## Verbal em papel - jogar a solo

`output/pdf/verbal-paper-solo-en.pdf` e `output/pdf/verbal-papel-solo-pt.pdf` são edições A4 independentes da aplicação: 12 desafios de dedução, com palavras portuguesas de 4–8 letras e instruções EN ou pt-PT. Cada desafio inclui tentativas já classificadas e uma lista finita de respostas possíveis. Riscam-se candidatas incompatíveis com as pistas até restar uma. Só são precisos papel e lápis; não é necessário dispositivo, dicionário ou alguém que conheça a resposta. As pistas usam símbolos monocromáticos e respeitam as ocorrências das letras repetidas.

Imprimir as páginas 1–3 para jogar; a página 4 contém as soluções e deve ficar separada. A impressão não é um backup nem uma reprodução das partidas guardadas. Não lê nem altera dados pessoais do navegador.

Para regenerar: `python3 scripts/build-paper-pack.py`, com ReportLab e Node disponíveis apenas na máquina de desenvolvimento. Os PDFs estão incluídos e não exigem instalação de ferramentas para imprimir. O gerador verifica uma única solução por lista, que todas as pistas são necessárias, e compara a classificação com o core da aplicação. Estes exemplos fixos continuam disponíveis; a integração na aplicação é descrita abaixo.

## Dedução e impressão na aplicação — 1.2.0

**Jogos → Dedução** abre a modalidade de pistas já classificadas e lista finita de palavras. Toca nas candidatas para riscar/repor, escolhe a resposta e confirma. Uma resposta incorreta não consome tentativas nem acrescenta pistas. As notas e a seleção ficam guardadas no mesmo armazenamento e nos backups. Há desafios diários e livres, de 4–8 letras. O teclado QWERTY fica oculto apenas nesta modalidade; a lista usa controlos de 44px e pode deslocar-se naturalmente em ecrãs curtos.

**Jogos → Imprimir desafios**, ou o botão correspondente em Dedução, prepara 4 ou 12 desafios, com tamanhos variados ou um tamanho escolhido. Permite escolher o idioma do documento e incluir/omitir as soluções, sempre numa última página separada. Há 1700 desafios verificados para impressão, com respostas diferentes de 4 a 8 letras. Nova seleção escolhe outra combinação deste catálogo finito; não promete desafios infinitos. As folhas são independentes das partidas e não são backups. Preparar, imprimir ou descarregar não modifica jogos, respostas ou preferências do dispositivo.

Tudo funciona offline depois da cache estar pronta. Imprimir usa páginas A4 vetoriais sem cor; Guardar ou abrir PDF gera um PDF local sem bibliotecas externas. No iPhone/Home Screen, se a janela de impressão não abrir, abrir o PDF e usar Partilhar → Imprimir. A impressão e partilha em dispositivos físicos continuam por verificar. O PDF tem texto WinAnsi e fontes PDF normalizadas, não imagens rasterizadas. Os URLs temporários são revogados ao fechar ou alterar as opções.

`paper-data.js` contém as definições imutáveis `paper-v1` e a extensão de impressão `paper-print-v2`; `paper.js` seleciona desafios e gera PDF/HTML. O gerador de desenvolvimento `python3 scripts/build-paper-pack.py --catalogue` verifica/regenera os mesmos bytes e recusa substituir um catálogo existente por conteúdo diferente. Uma expansão requer novos identificadores/versão, mantendo as definições antigas. Não alterar respostas ou pistas publicadas, pois são usadas para retomar e validar backups.

Testes adicionais: `node scripts/test-paper.cjs` e `node scripts/test-paper-browser.cjs` (com Playwright/Chromium apenas no desenvolvimento). A exportação direta não precisa de Python, ReportLab, Node ou acesso a outro site no dispositivo do jogador.

## Catálogo de 400 folhas — 1.2.1

O catálogo de impressão tem 400 puzzles distintos: 80 para cada tamanho de 4–8 letras. Mantém os 60 puzzles originais sem qualquer alteração e acrescenta 340 com novos identificadores de impressão. Cada um tem uma única resposta na sua lista e todas as pistas são necessárias. Nova seleção continua a preparar 4/12 puzzles localmente; não faz buscas combinatórias no navegador.

Para preservar partidas e backups existentes, o seletor dos desafios jogados no ecrã mantém a sequência original `paper-v1`. O seletor de impressão usa todos os 400. `scripts/fixtures/paper-v1.json` fixa os 60 originais; o gerador recusa reescrever definições existentes. O gerador completo continua disponível em desenvolvimento através de `python3 scripts/build-paper-pack.py --catalogue`.

Um gerador de puzzles inéditos no dispositivo é possível, mas exigiria processamento limitado/em segundo plano e validação de unicidade e qualidade das pistas. Esta versão amplia o catálogo pré-validado para manter a impressão imediata em dispositivos antigos.

## 1000 puzzles e histórico de pedidos — 1.3.0

O catálogo tem agora **1000 puzzles**,200 para cada tamanho4–8. Mantém os400 anteriores sem alterar ids, conteúdo ou sequência; acrescenta600 com ids paper-print-v3. A sequência dos jogos no ecrã continua a usar os60 paper-v1 originais, preservando partidas e backups. O catálogo é pré-validado; não foi acrescentado um gerador em tempo real no dispositivo.

Cada desafio e respetiva solução têm um código curto estável, por exemplo A4-001, B8-068 ou C5-120. **Jogos → Histórico de pedidos em papel** permite pesquisar esse código e consultar os pedidos de PDF/impressão, com data e25 resultados por página. O histórico começa com os novos pedidos: não é possível detetar automaticamente ficheiros ou folhas obtidos anteriormente.

Apenas preparar uma seleção não grava o histórico. Clicar Guardar ou abrir PDF, Imprimir ou usar a impressão do navegador com uma seleção ativa regista um pedido. O registo inclui pedidos cancelados; não confirma impressão física, gravação efetiva do ficheiro ou resolução. É um indicador suficiente para evitar voltar a selecionar esses puzzles. Uma falha de gravação mostra aviso; o PDF/impressão continua disponível e o registo em memória pode perder-se ao fechar.

Evitar pedidos anteriores vem marcado. Novas seleções excluem os ids registados; ao esgotar inéditos, a aplicação pede para reduzir a quantidade, mudar o tamanho ou desmarcar essa opção. Não mistura repetições silenciosamente. Uma seleção aberta é invalidada se outra janela entretanto pedir puzzles que se sobreponham. É permitido pedir PDF e impressão da mesma seleção de propósito.

O campo opcional paperHistory faz parte do JSON verbal/schema1, no mesmo registo atómico, com validação de ids e datas e o mesmo bloqueio de escritas desatualizadas. Ao restaurar um backup antigo sem o campo, preserva-se o histórico atual. Um backup novo com histórico explícito substitui-o, independentemente de Restaurar preferências. Apagar os dados do site apaga também este registo; exportar um backup é a forma de o conservar noutro dispositivo.

`scripts/fixtures/paper-print-400.json` fixa os400 antigos e a geração recusa alterá-los. Teste adicional: `node scripts/test-paper-history.cjs`, incluindo uma passagem pelos1000 sem repetições, esgotamento, códigos e compatibilidade dos backups.

## Catálogo de 1700 puzzles — 1.3.1

A impressão passa a dispor de1700 puzzles com1700 respostas diferentes, aproximando-se do total de1732 palavras dos bancos editoriais existentes. A distribuição por tamanho deixa de ser uniforme, pois o banco de4 letras só tem284 palavras. Mantêm-se os1000 anteriores, os seus códigos e registos, acrescentando700 ids paper-print-v4 (códigos D). Os jogos no ecrã continuam na sequência v1 estável.

O histórico e a exclusão dos já pedidos aplicam-se aos1700. A mistura de tamanhos usa as quantidades disponíveis sem repetir silenciosamente. Para2000 respostas diferentes seria necessário ampliar os bancos; puzzles com respostas repetidas mas pistas/listas diferentes seriam outra opção, não usada nesta expansão.
