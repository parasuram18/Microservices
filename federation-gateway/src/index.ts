// index.ts  (ESM)
import { ApolloGateway, IntrospectAndCompose, RemoteGraphQLDataSource, GraphQLDataSourceProcessOptions } from '@apollo/gateway';
import { ApolloServer } from '@apollo/server';
import { startStandaloneServer } from '@apollo/server/standalone';

//------------   WORKFLOW    ------------//

// [Client] → [Apollo Gateway (port 4000)]
//          └─> Context: Extracts Authorization header
//          └─> Calls subgraph using AuthHeader
//              └─> Sets Authorization header on request
//              └─> Forwards request to:
//                  - http://127.0.0.1:8000/graphql (user)
//                  - http://127.0.0.1:8001/graphql (blog)
//          ⇐ Result is merged & sent back to client

type MyContext = {
  auth?: string;
};

//Customizes requests with a class AuthHeader that adds an Authorization header.
class AuthHeader extends RemoteGraphQLDataSource {
  willSendRequest(options: GraphQLDataSourceProcessOptions<MyContext>) {
    const { request, context } = options
    if (context.auth) {
      // console.log('Auth Header:', context.auth);
      request.http!.headers.set('Authorization', context.auth);
    }
  }
  }

// ApolloGateway tracks all the schemas of subgraphs and builds a federated schema. 
// also attach auth header for each service
const gateway = new ApolloGateway({
  supergraphSdl: new IntrospectAndCompose({
    subgraphs: [
      { name: 'user',    url: 'http://user_service:8000/graphql' }, // change port for local run 
      { name: 'blog',  url: 'http://blog_service:8000/graphql' }, // change port for local run 
    ],
  }),
  buildService: ({ url }) => new AuthHeader({ url }),
});

// start single server acts as a gateway to all services
const server = new ApolloServer({
    gateway,
});

//When a client sends a GraphQL request to the gateway, context() function extracts and  injects the Authorization header as "auth"
const { url } = await startStandaloneServer(server, {
  listen: { port: 4000 },
  context: async ({ req }) => {
    return {
      auth: req.headers.authorization || '',
    };
  },
});
 
console.log(`🚀  Gateway ready at ${url}`);
