// index.ts  (ESM)
import { ApolloGateway, IntrospectAndCompose, RemoteGraphQLDataSource } from '@apollo/gateway';
import { ApolloServer } from '@apollo/server';
import { startStandaloneServer } from '@apollo/server/standalone';
//Customizes requests with a class AuthHeader that adds an Authorization header.
class AuthHeader extends RemoteGraphQLDataSource {
    willSendRequest(options) {
        const { request, context } = options;
        if (context.auth) {
            // console.log('Auth Header:', context.auth);
            request.http.headers.set('Authorization', context.auth);
        }
    }
}
// ApolloGateway tracks all the schemas of subgraphs and builds a federated schema. 
// also attach auth header for each service
const gateway = new ApolloGateway({
    supergraphSdl: new IntrospectAndCompose({
        subgraphs: [
            { name: 'user', url: 'http://user_service:8000/graphql' },
            { name: 'blog', url: 'http://blog_service:8001/graphql' },
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
