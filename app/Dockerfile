FROM node:20-alpine
WORKDIR /app/
COPY app/. .
RUN npm install
# Set NODE_ENV to production for the build
ENV NODE_ENV=production
# Run the build without sourcemaps for production
RUN npm run build || exit 1
EXPOSE 3000
CMD ["npm", "run", "start"]