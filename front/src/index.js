import React from 'react';
import ReactDOM from 'react-dom';
import RootPage from './components/RootPage';
import { BrowserRouter, Route, Switch } from 'react-router-dom';

const Root = () => (
    <BrowserRouter>
        <Switch>
            <Route exact path='/'component={RootPage}/>
        </Switch>
    </BrowserRouter>
)
ReactDOM.render(<Root />, document.getElementById('root'))
