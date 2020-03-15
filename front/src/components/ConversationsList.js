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
      console.log("---->", response.data)
      this.setState({conversations: response.data});
    })
    .catch(error => {
      console.log(error)
    })
  }

  render() {
    const conversations = this.state.conversations;
    return (
      <div>
          {
            conversations.length ?
            conversations.map(conversation => <div>{conversation.title} {conversation.nb_messages}</div>) :
            null
          }
      </div>
    );
  }
}

export default ConversationsList;
