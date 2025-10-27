# Frontend React — Galeria Distribuída

Este projeto implementa o frontend solicitado (Upload / Listar / Mostrar) para a aplicação web distribuída descrita no enunciado.

## Pré-requisitos
- Node.js LTS (>= 18)
- npm (ou pnpm/yarn)

## Como iniciar do zero
```bash
# 1) Instale as dependências
npm install

# 2) Copie o .env de exemplo e ajuste a URL do LB (NGINX)
cp .env.example .env
# edite .env e defina VITE_API_BASE_URL, por exemplo:
# VITE_API_BASE_URL=http://IP_PUBLICO_DO_LB/api

# 3) Rode em desenvolvimento
npm run dev

# 4) Build de produção
npm run build
npm run preview
```

## Endpoints esperados do backend
- `POST /upload` → busca uma imagem numa API pública e **salva no banco**; retorna `{ id, url, tags }`
- `GET /images` → lista imagens salvas; retorna `[{ id, tags }]`
- `GET /images/:id` → retorna uma imagem específica; retorna `{ id, url, tags }`

> Ajuste `src/services/api.js` caso seus endpoints reais sejam diferentes.

## Estrutura
```
src/
  App.jsx
  index.css
  main.jsx
  components/
    ImageDisplay.jsx
    ImageList.jsx
    UploadButton.jsx
  services/
    api.js
```

## Tailwind
Já está configurado (Tailwind + PostCSS + Autoprefixer). As classes utilitárias foram usadas para um visual limpo.

## Dica de NGINX no Load Balancer
Veja `docs/DEPLOY_NGINX.md` para um exemplo de configuração.
