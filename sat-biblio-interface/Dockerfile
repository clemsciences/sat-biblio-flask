# Stage 1: Build stage
FROM node:20-alpine AS build-stage

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies (clean install honoring the lockfile)
RUN npm ci

# Copy project files
COPY . .

# Build the app for production
# VITE_APP_SITE_API_URL can be provided at build time
ARG VITE_APP_SITE_API_URL
ENV VITE_APP_SITE_API_URL=$VITE_APP_SITE_API_URL

RUN npm run build

# Stage 2: Production stage
FROM nginx:stable-alpine AS production-stage

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