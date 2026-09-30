# Build the browser bundle once; Spring Boot serves it from classpath:/static.
FROM node:22-bookworm AS frontend-build
WORKDIR /src/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

FROM maven:3.9-eclipse-temurin-21 AS backend-build
WORKDIR /src/backend
COPY backend/pom.xml ./
RUN mvn -q dependency:go-offline
COPY backend/src ./src
COPY --from=frontend-build /src/frontend/dist ./src/main/resources/static
RUN mvn -q -DskipTests package

FROM eclipse-temurin:21-jre-noble
RUN apt-get update \
  && apt-get install -y --no-install-recommends ca-certificates nodejs npm util-linux \
  && npm install --global @openai/codex \
  && useradd --system --uid 10001 --create-home app \
  && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY --from=backend-build /src/backend/target/adaptive-java-tutor-0.1.0.jar /app/app.jar
COPY java_initial_diagnostic_mvp_v2.md /app/java_initial_diagnostic_mvp_v2.md
COPY backend/docker-entrypoint.sh /usr/local/bin/adaptive-entrypoint
RUN chmod 755 /usr/local/bin/adaptive-entrypoint \
  && mkdir -p /app/data /app/codex-home \
  && chown -R app:app /app
ENV HOME=/app/codex-home \
    CODEX_HOME=/app/codex-home \
    APP_DATABASE_PATH=/app/data/adaptive-tutor.db \
    APP_DIAGNOSTIC_SOURCE=/app/java_initial_diagnostic_mvp_v2.md
EXPOSE 8080
ENTRYPOINT ["/usr/local/bin/adaptive-entrypoint"]
CMD ["java", "-jar", "/app/app.jar"]
