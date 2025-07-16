// gateway.js
import { ApolloServer } from '@apollo/server';
import { startStandaloneServer } from '@apollo/server/standalone';
import { ApolloGateway } from '@apollo/gateway';

const gateway = new ApolloGateway({
  serviceList: [
    { name: 'user', url: 'http://127.0.0.1:8000/graphql' },
    { name: 'blog', url: 'http://127.0.0.1:8001/graphql' },
  ],
});

const server = new ApolloServer({
  gateway,
  // Required for gateway mode
  subscriptions: false,
});

const { url } = await startStandaloneServer(server, {
  listen: { port: 4000 },
});
console.log(`🚀 Gateway ready at ${url}`);
