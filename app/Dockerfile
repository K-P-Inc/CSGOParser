FROM node:20-alpine
WORKDIR /app/
COPY app/. .
RUN npm install

# Run the build without sourcemaps for production
RUN npm run build

EXPOSE 3000

CMD ["npm", "run", "start"]