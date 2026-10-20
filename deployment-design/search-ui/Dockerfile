# Stage 1: build the React app into static files
FROM node:22-alpine AS build
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: serve the built files with nginx
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html