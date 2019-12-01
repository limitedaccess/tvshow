
import React from 'react';
import ReactDOM from 'react-dom';
import { createStore, applyMiddleware, compose } from 'redux';
import thunk from 'redux-thunk';
import { Provider } from 'react-redux';
import App from './components/app.jsx';
import Reducer from './reducer/reducer';
// import 'bootstrap/dist/css/bootstrap.min.css';

/* eslint-disable no-underscore-dangle */
const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;
const store = createStore(
  Reducer,
  composeEnhancers(
    applyMiddleware(thunk), /* preloadedState, */
  ),
);
/* eslint-enable */

ReactDOM.render((
  <Provider store={store}>
    <App />
  </Provider>
), document.getElementById('react-app'));