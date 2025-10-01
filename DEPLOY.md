# Guia de Deploy — API de Autorizações Governamentais

## Pré-requisitos
- **Docker Engine** >= 26.0 com modo Swarm habilitado (necessário para stacks no Portainer).
- **Docker Compose** Plugin >= 2.24 (para builds locais antes de publicar a imagem).
- **Portainer** CE/Business >= 2.19 com acesso ao endpoint Swarm/Agent.
- Hardware mínimo recomendado: 2 vCPUs, 2 GB de RAM, 10 GB de armazenamento livre para volumes.
- Acesso de rede liberado para a porta **8000/TCP** (API) e comunicação interna da rede overlay.

## Configuração Inicial
1. **Clonar o repositório**
   ```bash
   git clone https://example.com/att_govfed.git
   cd att_govfed
   ```
2. **Configurar variáveis de ambiente**
   - Crie um arquivo `.env.deploy` (não versionado) contendo pelo menos:
     ```env
     AUTORIZACOES_IMAGE=registry.example.com/autorizacoes-api:latest
     ```
   - O serviço lê opcionalmente `DATA_ROOT` (já definido no `docker-compose.yml`). Ajuste apenas se desejar outra hierarquia interna.
3. **Construir e publicar a imagem**
   ```bash
   docker build -t $AUTORIZACOES_IMAGE .
   docker push $AUTORIZACOES_IMAGE
   ```
   > Decisão: a stack usa somente `image:` para compatibilidade com Portainer/Swarm; por isso a publicação prévia é obrigatória.
4. **Criar volumes persistentes (opcional localmente, obrigatório no Swarm)**
   ```bash
   docker volume create autorizacoes_raw
   docker volume create autorizacoes_processed
   ```

## Deploy via Portainer
1. **Importar a stack**
   - Acesse Portainer → *Stacks* → *Add Stack* → *Web editor*.
   - Cole o conteúdo de `docker-compose.yml`. Ajuste `image:` conforme o registro utilizado.
2. **Configurar variáveis**
   - Em *Environment variables*, defina `AUTORIZACOES_IMAGE` caso tenha usado placeholder na stack.
   - Verifique se `DATA_ROOT` permanece `/var/lib/autorizacoes` (padrão).
3. **Criar rede e volumes pela UI (se ainda não existirem)**
   - *Volumes* → *Add volume* → `autorizacoes_raw` e `autorizacoes_processed`.
   - *Networks* → *Add network* → `autorizacoes_network` com driver `overlay`.
4. **Implantar**
   - Clique em *Deploy the stack* e aguarde o status `Running`.
5. **Verificar saúde**
   - Portainer mostrará `healthy` graças ao endpoint `/health`.
   - Teste manualmente:
     ```bash
     curl http://<host>:8000/health
     curl http://<host>:8000/data?skip=0&limit=5
     ```
6. **Troubleshooting**
   - Logs: Portainer → serviço → *Logs* ou `docker service logs stack_autorizacoes-api`.
   - Health check falhando: confirme conectividade na porta 8000 e existence of processed data.
   - Reconstruir imagem após alterações: repetir etapa de build/push e use *Recreate* na stack.

## Manutenção
- **Atualizar a aplicação**
  1. Atualize o código fonte.
  2. `docker build -t $AUTORIZACOES_IMAGE . && docker push $AUTORIZACOES_IMAGE`.
  3. Em Portainer, use *Update the stack* para aplicar nova imagem (optionally use digest/tag versionado).
- **Backup dos dados**
  - Faça snapshot dos volumes `autorizacoes_raw` e `autorizacoes_processed`:
    ```bash
    docker run --rm -v autorizacoes_processed:/data -v $(pwd):/backup \
      busybox tar czf /backup/processed-$(date +%F).tgz -C /data .
    ```
  - Repita para `autorizacoes_raw` conforme necessidade dos arquivos fonte.
- **Monitoramento básico**
  - Verifique periodicamente logs de processamento para falhas ao ler planilhas.
  - Configure alertas no Portainer ou Prometheus (caso disponível) para reinícios excessivos.
- **Logs importantes**
  - `uvicorn` emite logs de requisições no stdout (visíveis via Portainer).
  - Mensagens de `process_data` informam arquivos processados e erros de parsing.
  - Em caso de exceções de banco/arquivo ausente, a API retorna HTTP 404 explicativo.

## Decisões Técnicas Registradas
- Uso de imagem base `python:3.12-slim` para compatibilidade com wheels científicos e menor tempo de build.
- Definição do diretório de dados via `DATA_ROOT`, permitindo volumes dedicados.
- Inclusão de endpoint `/health` para health checks automatizados.
- Persistência separada (`raw` e `processed`) para facilitar backups seletivos e rotação de dados.
