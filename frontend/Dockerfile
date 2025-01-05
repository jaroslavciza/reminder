# První fáze: Build aplikace pomocí Node.js
FROM node:23 AS build-stage

# Nastavení pracovního adresáře
WORKDIR /app

# Kopírování package.json a package-lock.json (pokud existuje)
COPY package*.json ./

# Instalace závislostí
RUN npm install

# Kopírování zbytku aplikace
COPY . .

# Vytvoření produkční verze aplikace (static build)
RUN npm run build


# Druhá fáze: Servírování aplikace pomocí Nginx
FROM nginx:alpine AS production-stage

# Kopírování buildovaných souborů z první fáze do Nginx
COPY --from=build-stage /app/dist/ /usr/share/nginx/html

# Exponování portu 80 (Nginx)
EXPOSE 80

# Spuštění Nginx, který servíruje aplikaci
CMD ["nginx", "-g", "daemon off;"]
