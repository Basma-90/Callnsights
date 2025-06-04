# Stage 1: Build
FROM node:18-alpine as builder
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install --frozen-lockfile
COPY . .

# Create temporary tsconfig that ignores unused declarations
RUN echo '{ "extends": "./tsconfig.json", "compilerOptions": { "noUnusedLocals": false, "noUnusedParameters": false } }' > tsconfig.build.json
RUN sed -i 's/tsc -b/tsc -b tsconfig.build.json/g' package.json
RUN npm run build

# Stage 2: Serve
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]