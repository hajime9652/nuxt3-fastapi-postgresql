FROM node:16-alpine

WORKDIR /app

COPY package.json /app

RUN npm install -g --force yarn
RUN yarn install

COPY ./ /app/

ARG FRONTEND_ENV=dev
ENV VUE_APP_ENV=${FRONTEND_ENV}
ENV NODE_ENV=development
ENV HOST 0.0.0.0

CMD ["yarn", "dev", "--host", "0.0.0.0", "--port", "80"]

# https://github.com/bitkanlabs/nuxt/blob/master/Dockerfile
