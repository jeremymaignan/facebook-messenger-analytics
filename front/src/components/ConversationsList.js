import React, { Component } from 'react';
import axios from 'axios'

class ConversationsList extends Component {
    constructor(props) {
        super(props);
        this.state = {
            conversations: [],
            current_user: "",
            number_messages: 0
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

    handleClick = (current_user, number_messages) => {
        this.setState({current_user: current_user});
        this.setState({number_messages: number_messages});
    }

    render() {
        const conversations = this.state.conversations;
        const current_user = this.state.current_user
        const number_messages = this.state.number_messages
        return (
            <div className="container-fluid">
                <div className="row">
                    <div className="col-sm">
                        <div className="col-sm-6 col-md-8 sidebar">
                            <ul className="list-group">
                                {
                                    conversations.length ?
                                    conversations.map(conversation => 
                                    <li onClick={() => this.handleClick(conversation.title, conversation.nb_messages)} className="list-group-item d-flex justify-content-between align-items-center">
                                        {conversation.title}
                                        <span className="badge badge-primary badge-pill">
                                           {conversation.nb_messages}
                                        </span>
                                    </li>):
                                null
                                }
                            </ul>
                        </div>
                    </div>
                    <div className="col-sm">
                        {current_user !== "" &&
                        <div>
                            <h1>{current_user}</h1>
                            <p>Number of messages: {number_messages}</p>
                        </div>
                        }
                    </div>
            </div>
        </div>
    );
  }
}

export default ConversationsList;
