import React, { Component } from 'react';
import ConversationsList from './ConversationsList';

class RootPage extends Component {
  render() {
    return (
        <div className="container-fluid">
            <ConversationsList />
        </div>
    );
  }
}

export default RootPage;
