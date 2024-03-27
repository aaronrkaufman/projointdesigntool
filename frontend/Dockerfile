FROM node:alpine

WORKDIR /app

COPY ./package* ./
RUN npm ci

COPY . .

RUN npm run build

CMD [ "npm", "start" ]
