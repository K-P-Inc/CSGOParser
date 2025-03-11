FROM node:20-alpine
WORKDIR /app/
COPY app/. .
RUN npm install
# Set NODE_ENV to production for the build
ENV NODE_ENV=production
# Explicitly disable sourcemaps for production build
ENV GENERATE_SOURCEMAP=false
# Run the build without sourcemaps for production
RUN npm run build
EXPOSE 3000
CMD ["npm", "run", "start"]