# Verbal — v1.0.0

Jogo de palavras instalável, local e offline. Palavras portuguesas de 4, 5, 6, 7 ou 8 letras, seis tentativas, desafio diário por tamanho, modo livre, estatísticas por tamanho e partilha sem revelar a resposta. Interface em português europeu e inglês. **Mudar a interface para inglês mantém as palavras portuguesas.** As listas iniciais não são um dicionário completo.

## Colocar no repositório

Extrair o conteúdo desta pasta para `/Users/nfp/github/pwa/verbal`, preservando o `.git` que já existe. Não copiar para uma subpasta adicional. O pacote não inclui a identidade ou autenticação do protótipo Sites.

```bash
cd /Users/nfp/github/pwa/verbal
python3 -m http.server 8000 --directory public
```

Abrir `http://localhost:8000`. Não é necessário instalar npm ou dependências. O service worker funciona em localhost ou HTTPS; `file://` não serve para testar a PWA. Para testar num iPhone, usar um alojamento HTTPS; HTTP através do endereço LAN do Mac não permite service workers.

Depois de verificar, fazer commit e push pelos meios habituais. Não foram feitos commits ou pushes no teu GitHub por esta entrega.

## DreamHost

Destino previsto: `https://verbal.basecentral.link`. Criar o domínio e HTTPS no painel. O checkout Git do servidor deve ficar **fora** do diretório público. Precisa de Bash, Git e Python 3; nenhum runtime Node/PHP é necessário.

No servidor, clonar o teu repositório e configurar uma branch com upstream, usando as tuas credenciais habituais. A partir desse checkout:

```bash
bash scripts/deploy.sh /home/basecentral/verbal.basecentral.link
```

O diretório de destino deve já existir. Adaptar o caminho ao utilizador/domínio configurados. O script faz fetch e `git pull --ff-only`, recusa alterações locais, ficheiros não rastreados, branch detached, divergência ou commits apenas no servidor. Não altera credenciais e nunca faz reset/clean/stash/push.

Publica apenas os 14 ficheiros da lista `FILES` em `scripts/deploy.py`, todos presentes em `public/`. Verifica fontes e destinos antes de publicar, recusa symlinks e diretórios sobrepostos, prepara cópias no destino e usa substituição atómica **por ficheiro**, com permissões 0644. O conjunto da publicação não é uma transação: uma falha durante as substituições pode deixar recursos de versões diferentes. `sw.js` é o último ficheiro, e a cache de instalação só fica pronta se todos os recursos forem obtidos e os seus hashes SHA-256 corresponderem à release. Publicar numa janela calma e voltar a executar após corrigir uma falha. Preserva ficheiros alheios e o `.htaccess` existente.

`hosting/dreamhost.htaccess` é um exemplo opcional. Rever e copiar manualmente para o webroot como `.htaccess`; o deploy não o instala nem substitui. A pasta hosting nunca deve ser pública. Não é preciso reescrever rotas: é uma aplicação de uma só página sem rotas no servidor.

## Dados, privacidade e portabilidade

Dados num só registo `verbal:data:v1` de localStorage. Sem conta, analytics, CDN ou transmissão de jogos. As respostas estão no código local: sem proteção contra batota. Dados pertencem ao dispositivo/navegador/origem; o protótipo privado e o domínio final não partilham armazenamento. O novo pacote não migra automaticamente dados do protótipo Letra.

Definições → Dados e cópias de segurança: exportar JSON antes de mudar de navegador/dispositivo ou limpar dados. O backup `format: verbal`, `schema: 1` inclui todos os jogos concluídos/em curso, rascunhos, preferências de modo/tamanho/idioma e contador do modo livre. Resultados e estatísticas são reconstruídos a partir desses jogos. Não inclui caches, permissões nem o momento da última exportação da sessão. Importação até 5 MiB/10 000 jogos, com validação e pré-visualização. **Substitui** a coleção; não faz fusão. Restaurar preferências vem marcado; desmarcar preserva as preferências atuais. Backups com outro formato/versão são recusados, sem modificação. Dados com falha de gravação podem ser exportados da sessão.

## Instalação, offline e atualizações

iPhone: Safari → Partilhar → Adicionar ao ecrã principal. Nos restantes navegadores, usar Instalar quando existir. A interface verifica os recursos antes de mostrar Pronto para jogar offline; sem service worker é possível jogar online, mas não há promessa de offline.

Definições → Procurar atualizações. Atualizar aplicação só aparece quando há uma versão instalada em espera. A ativação é explícita e preserva o progresso guardado; janelas com trabalho não gravado não são recarregadas automaticamente. Antes de cada release alterar VERSION em app.js e sw.js em conjunto. Executar `python3 scripts/prepare-release.py` depois de qualquer alteração aos recursos públicos e antes de fazer commit. Esta operação regenera `release.json` e o hash esperado pelo service worker, sem dependências externas. Cada cache contém uma release completa; as anteriores são conservadas para janelas antigas e podem ocupar espaço. Não há remoção automática de dados ou caches para corrigir problemas.

## Palavras e testes

Listas em `public/words.js`, selecionadas manualmente para este projeto. Acentos/cedilhas são normalizados. As tentativas de 5 letras usam uma lista alargada; nos outros tamanhos, respostas e palavras aceites usam a mesma lista inicial. Expandir o vocabulário com revisão editorial antes de uma divulgação ampla. O desafio usa uma função determinística da data em Lisboa e do tamanho; sem dependência de serviços externos.

```bash
node scripts/test-core.cjs
python3 scripts/test-deploy.py
```

Os testes precisam de Node apenas na máquina de desenvolvimento; não no alojamento. Ver `docs/VERIFICATION.md` para evidência e limitações. Alvo: iPhone 6 / iOS 12.5.x / Safari 12. A compatibilidade com esse dispositivo físico ainda não foi verificada.
