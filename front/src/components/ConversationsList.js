import React, { Component } from 'react';
import axios from 'axios'

class ConversationsList extends Component {
  constructor(props) {
    super(props);
    this.state = {
      conversations: []
    }
  }

  componentDidMount() {
    var config = {
      headers: {'Access-Control-Allow-Origin': '*'}
    };
    axios.get('http://127.0.0.1:7000/conversation', config)
    .then(response => {
      this.setState({conversations: response.data});
    })
    .catch(error => {
      console.log(error)
    })
  }

  render() {
    const conversations = this.state.conversations;
    return (
      <div class="col-sm-6 col-md-6 sidebar">
        <ul class="list-group">
        {
            conversations.length ?
            conversations.map(conversation => <li class="list-group-item d-flex justify-content-between align-items-center">{conversation.title}<span class="badge badge-primary badge-pill">{conversation.nb_messages}</span></li>) :
            null
          }
        </ul>
      </div>
    );
  }
}

export default ConversationsList;
