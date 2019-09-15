import React, { Component } from 'react';
import axios from 'axios'

class UsersList extends Component {
  constructor(props) {
    super(props);
    this.state = {
      users: []
    }
  }

  componentDidMount() {
    var config = {
      headers: {'Access-Control-Allow-Origin': '*'}
    };
    axios.get('http://127.0.0.1:5000/users', config)
    .then(response => {
      this.setState({users: response.data.users})
    })
    .catch(error => {
      console.log(error)
    })
  }

  render() {
    const users = this.state.users
    return (
      <div>
          {
            users.length ?
            users.map(user => <div>{user.username}</div>) :
            null
          }
      </div>
    );
  }
}

export default UsersList;
