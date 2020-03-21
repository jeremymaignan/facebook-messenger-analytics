import React from 'react';
import ReactDOM from 'react-dom';
import ConversationsList from './components/ConversationsList';
import { BrowserRouter, Route, Switch } from 'react-router-dom'

const Root = () => (
    <BrowserRouter>
        <Switch>
            <Route exact path='/'component={ConversationsList}/>
        </Switch>
    </BrowserRouter>
)
ReactDOM.render(<Root />, document.getElementById('root'))
