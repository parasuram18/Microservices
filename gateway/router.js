// gateway.js
import { ApolloServer } from '@apollo/server';
import { startStandaloneServer } from '@apollo/server/standalone';
import { ApolloGateway, RemoteGraphQLDataSource, IntrospectAndCompose } from '@apollo/gateway';

class AuthHeader extends RemoteGraphQLDataSource {
  willSendRequest({ request, context }) {
    if (context.auth){
      request.http.headers.set('Authorization', context.auth);
    }
  }
}


const gateway = new ApolloGateway({
  supergraphSdl: new IntrospectAndCompose({
    subgraphs: [
      { name: 'user',    url: 'http://127.0.0.1:8000/graphql' },
      { name: 'blog',  url: 'http://127.0.0.1:8001/graphql' },
    ],
  }),
  buildService: ({ url }) => new AuthHeader({ url })
});

const server = new ApolloServer({
  gateway,
  // Required for gateway mode
  subscriptions: false,
});

const { url } = await startStandaloneServer(server, {
  listen: { port: 4000 },
  context: async ({ req }) => {
    return {
      auth: req.headers.authorization || '',
    };
  },
});

console.log(`🚀 Gateway ready at ${url}`);
