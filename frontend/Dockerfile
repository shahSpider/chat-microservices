# --- Base image ---
FROM node:20-alpine

# --- Set working directory inside container ---
WORKDIR /app

# --- Copy package.json + package-lock.json ---
COPY package*.json ./

# --- Install dependencies ---
RUN npm install

# --- Copy the rest of the source code ---
COPY . .

# --- Expose Vite dev server port ---
EXPOSE 5173

# --- Run development server ---
CMD ["sh", "-c", "npm install && npm run dev -- --host"]
