import React from 'react';
import ReactDOM from 'react-dom';
import {PostListWithPoints, PointListWithPoints, PointListWithPoint} from './ys/point_list';
import { ApolloClient } from 'apollo-client';
import { gql } from 'graphql-tag';
import { ApolloProvider, graphql } from 'react-apollo';
import { HttpLink } from 'apollo-link-http';
import { InMemoryCache } from 'apollo-cache-inmemory';
import { BrowserRouter, Switch, Route, Redirect } from 'react-router-dom'

const client = new ApolloClient({
  link: new HttpLink({ uri: '/graphql', credentials: 'same-origin' }),
  cache: new InMemoryCache()
});

class App extends React.Component {
  render() {
    return (
        <Switch>
        <Route exact path="/pointCard/:url" component={PointListWithPoint} />
        </Switch>
    )
  }
}

ReactDOM.render(
  <BrowserRouter>
    <ApolloProvider client={client}>
      <App/>
    </ApolloProvider>
  </BrowserRouter>,
  document.getElementById('root')
);
