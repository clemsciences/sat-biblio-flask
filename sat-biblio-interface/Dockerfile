# Stage 1: Build stage
FROM node:16-alpine as build-stage

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy project files
COPY . .

# Build the app for production
# VUE_APP_SITE_API_URL can be provided at build time
ARG VUE_APP_SITE_API_URL
ENV VUE_APP_SITE_API_URL=$VUE_APP_SITE_API_URL
# Enable legacy OpenSSL provider for Webpack 4/Vue CLI 4 on newer Node versions
ENV NODE_OPTIONS=--openssl-legacy-provider

RUN npm run build

# Stage 2: Production stage
FROM nginx:stable-alpine as production-stage

# Install curl for healthcheck
RUN apk add --no-cache curl

# Create a non-root user
RUN addgroup -S satbiblio && adduser -S satbiblio -G satbiblio

# Copy build artifacts from build-stage
# Note: package.json specifies --dest satbiblio-dist
COPY --from=build-stage /app/satbiblio-dist /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Set ownership to non-root user
RUN chown -R satbiblio:satbiblio /usr/share/nginx/html /var/cache/nginx /var/run /var/log/nginx

# Use a custom pid file location that the non-root user can write to
RUN sed -i 's/\/var\/run\/nginx.pid/\/tmp\/nginx.pid/g' /etc/nginx/nginx.conf

USER satbiblio

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:8080/ || exit 1

CMD ["nginx", "-g", "daemon off;"]