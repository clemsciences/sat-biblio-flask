# Stage 1: Build stage
FROM node:20-alpine AS build-stage

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies (clean install honoring the lockfile)
RUN npm ci

# Copy project files
COPY . .

# Build the app for production.
# VITE_APP_SITE_API_URL can be overridden at build time:
#   docker build --build-arg VITE_APP_SITE_API_URL=https://… .
# Left unset, the build falls back to the value in .env.production.
#
# Do NOT turn this into `ENV VITE_APP_SITE_API_URL=$VITE_APP_SITE_API_URL`: an ARG
# with no default is the empty string, ENV would then define the variable *empty*,
# and Vite prioritises real env vars over .env files — silently baking an empty API
# URL into the bundle. A bare ARG is simply absent from the environment when it is
# not passed, which is what makes the .env.production fallback work.
ARG VITE_APP_SITE_API_URL

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

# Set ownership to non-root user.
# /var/run is deliberately absent: it is a symlink to /run, so `chown -R` would
# retarget the link itself and leave /run root-owned. The pid file is moved to /tmp
# below instead.
RUN chown -R satbiblio:satbiblio /usr/share/nginx/html /var/cache/nginx /var/log/nginx

# Use a custom pid file location that the non-root user can write to.
# Match the `pid` directive itself rather than a hardcoded path: the image declares
# `pid /run/nginx.pid;`, so a substitution on "/var/run/nginx.pid" silently matches
# nothing and nginx dies at startup with
#   [emerg] open() "/run/nginx.pid" failed (13: Permission denied)
RUN sed -i 's|^pid .*;|pid /tmp/nginx.pid;|' /etc/nginx/nginx.conf && \
    grep -q '^pid /tmp/nginx.pid;' /etc/nginx/nginx.conf

USER satbiblio

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:8080/ || exit 1

CMD ["nginx", "-g", "daemon off;"]