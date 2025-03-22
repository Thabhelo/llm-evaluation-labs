FROM node:20-slim

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy application code
COPY . .

# Build the application
RUN npm run build

# Install serve to run the application
RUN npm install -g serve

# Start the application
CMD ["serve", "-s", "dist", "-p", "3000"] 