FROM node:18-alpine

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm i

RUN mkdir -p /app/public/logs
COPY src/ ./src/
COPY public/ ./public/
COPY index.html vite.config.js *.json ./

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]