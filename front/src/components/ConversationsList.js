import React, { Component } from 'react'
import {Hint, RadialChart, XYPlot,DiscreteColorLegend, XAxis, YAxis, VerticalGridLines, HorizontalGridLines, VerticalBarSeries} from 'react-vis'
import '../../node_modules/react-vis/dist/style.css'
import API from '../api'
import formatNumbers from '../utils'

class ConversationsList extends Component {
    constructor(props) {
        super(props)
        this.state = {
            conversations: [],
            conversation_id: "",
            conversation_title: null,
            value: false,
            current_conversation: null,
            calls: null,
            page: "message",
            search_query: '',
            messages_per_hour: null,
            languages: null
        }
    }

    /* API CALLS */
    componentDidMount() {
        API.get("/conversation?data=conversation_list")
        .then(response => {
            this.setState({conversations: response.data})
        })
        .catch(error => {
            console.log(error)
        })
    }

    updateConversationInfo = (conversation_id) => {
        API.get("/conversation/" + conversation_id + '?data=info')
        .then(response => {
            response.data.is_still_participant = Boolean(response.data.is_still_participant)
            this.setState({current_conversation: response.data})
        })
        .catch(error => {
            console.log(error)
        })
    }

    updateConversationPerHour = (conversation_id) => {
        API.get("/conversation/" + conversation_id + '/messages?data=message_per_hour')
        .then(response => {
            this.setState({messages_per_hour: response.data.messages_per_hour})
        })
        .catch(error => {
            console.log(error)
        })
    }

    updateLanguages = (conversation_id) => {
        API.get("/conversation/" + conversation_id + '?data=languages')
        .then(response => {
            this.setState({languages: response.data})
        })
        .catch(error => {
            console.log(error)
        })
    }

    updateCall = (conversation_id) => {
        API.get("/conversation/" + conversation_id + '/call')
        .then(response => {
            this.setState({calls: response.data})
            console.log(this.state.calls)
        })
        .catch(error => {
            console.log(error)
        })
    } 

    selectConversation = (conversation_id, conversation_title) => {
        this.setState({
            conversation_id: conversation_id,
            conversation_title: conversation_title,
            messages_per_hour: null,
            current_conversation: null,
            languages: null
        })
        this.setState({page: "message"})
        this.updateConversationInfo(conversation_id)
        this.updateConversationPerHour(conversation_id)
        this.updateLanguages(conversation_id)
        this.updateCall(conversation_id)
    }

    /* SETTTERS */
    queryConversations = query =>  this.setState({ search_query: query.target.value })

    setTab = page => this.setState({page: page})

    showLabels = (v) => {
        if (v === false)
            this.setState({value: false})
        else
            delete v['angle0']
            delete v['angle']
            delete v['radius']
            delete v['radius0']
            delete v['y']
            delete v['x']
            delete v['color']
            this.setState({value: v})
    }

    /* RENDERING FUNCTIONS */
    renderConversationList = (conversation) => {
        const search_query = this.state.search_query

        if (search_query !== "" && conversation.title.toLowerCase().indexOf(search_query.toLocaleLowerCase()) === -1)
            return null
        return (
            <li onClick={() => this.selectConversation(conversation.conversation_id, conversation.title)} className="list-group-item d-flex justify-content-between align-items-center list-group-item-action">
                {conversation.title}
                {conversation.is_still_participant === 1 &&
                    <span className="badge badge-primary badge-pill">
                        {formatNumbers(conversation.nb_messages)}
                    </span>
                }
                {conversation.is_still_participant === 0 &&
                    <span className="badge badge-danger badge-pill">
                        {formatNumbers(conversation.nb_messages)}
                    </span>
                }
            </li>
        )
    }

    renderMessages = () => {
        const current_conversation = this.state.current_conversation
        const messages_per_hour = this.state.messages_per_hour
        const conversation_title = this.state.conversation_title
        const languages = this.state.languages
        const {value} = this.state

        if (conversation_title === null)
            return null
        return (
            <div>
                {/* Info */}
                <h3>Info</h3>
                {
                    current_conversation !== null ?
                    <div>
                        <div className="card">
                            <ul className="list-group list-group-flush">
                                <li className="list-group-item"><b>Number of messages:</b> {formatNumbers(current_conversation.nb_messages)}</li>
                                <li className="list-group-item"><b>First message:</b> {current_conversation.first_message}</li>
                                <li className="list-group-item"><b>Last message:</b> {current_conversation.last_message}</li>
                                <li className="list-group-item"><b>Still in conversation:</b> {current_conversation.is_still_participant.toString()}</li>
                                <li className="list-group-item"><b>Messages per day:</b> {current_conversation.message_per_day}</li>
                            </ul>
                        </div>
                        <br />

                        {/* Messages per user */}
                        <h3>Messages per user:</h3>
                        <table className="table table-hover">
                            <thead>
                                <tr>
                                    <th>#</th>
                                    <th>Participants</th>
                                    <th>Number of calls</th>
                                    <th>Rate (%)</th>
                                </tr>
                            </thead>
                            <tbody>
                                { 
                                    current_conversation.nb_messages_per_user.length ? current_conversation.nb_messages_per_user.map((user, index) =>
                                        <tr>
                                            <th scope="row">{index + 1}</th>
                                            <td>{user.user}</td>
                                            <td>{formatNumbers(user.nb_message)}</td>
                                            <td>{user.rate}%</td>
                                        </tr>
                                    ) : null
                                }
                            </tbody>
                        </table>
                        <div>
                            <RadialChart
                                className={'donut-chart-example'}
                                innerRadius={150}
                                colorType={'literal'}
                                radius={200}
                                getAngle={d => d.nb_message}
                                getLabel={d => d.label}
                                data={current_conversation.nb_messages_per_user}
                                onValueMouseOver={v => this.showLabels(v)}
                                onSeriesMouseOut={v => this.showLabels(false)}
                                width={900}
                                height={500}
                                padAngle={0.04}
                                showLabels
                                labelsStyle={{fontSize: 16, fill: '#22'}}
                            >
                            {value !== false && <Hint value={value} />}
                            </RadialChart>
                        </div>
                    </div>
                    : 
                    <div class="text-center">
                        <div class="spinner-border text-primary" role="status">
                            <span class="sr-only">Loading...</span>
                            <br />
                        </div>
                    <br />
                    </div>
                }
                {/* Messages over the time */}
                <h3>Messages over the time</h3>
                { messages_per_hour !== null ?
                    <div>
                        <XYPlot margin={{bottom: 70, left: 50}} xType="ordinal" width={900} height={400}>
                            <DiscreteColorLegend
                                style={{position: 'absolute', left: '60px', top: '10px'}}
                                orientation="horizontal"
                                items={[
                                    {
                                        title: 'Number of messages',
                                        color: "#575fcf"
                                    },
                                ]}
                            />
                            <VerticalGridLines />
                            <HorizontalGridLines />
                            <XAxis tickLabelAngle={-45} />
                            <YAxis/>
                            <VerticalBarSeries
                                data={messages_per_hour}
                                color="#575fcf"
                            />
                        </XYPlot>
                    </div>
                    :
                    <div class="text-center">
                        <div class="spinner-border text-primary" role="status">
                            <span class="sr-only">Loading...</span>
                            <br />
                        </div>
                    <br />
                    </div>
                }
                {/* Languages */}
                <h3>Languages</h3>
                { languages !== null ? 
                    <table className="table table-hover">
                    <thead>
                        <tr>
                            <th>#</th>
                            <th> </th>
                            <th>Language</th>
                            <th>Messages</th>
                        </tr>
                    </thead>
                    <tbody>
                        {
                            languages.length ? languages.map((language, index) =>
                                <tr>
                                    <th scope="row">{index + 1}</th>
                                    <td>{language.flag}</td>
                                    <td>{language.language_pretty}</td>
                                    <td>{formatNumbers(language.nb_messages)}</td>
                                </tr>
                            )
                            :
                            null
                        }
                    </tbody>
                </table>
                    : 
                    <div class="text-center">
                        <div class="spinner-border text-primary" role="status">
                            <span class="sr-only">Loading...</span>
                            <br />
                        </div>
                    <br />
                    </div>
                }
            </div>
        )
    }

    renderCalls = () => {
        const calls = this.state.calls
        if (calls === null)
            return null
        return (
            <div>
                {/* Calls */}
                <h3>Info</h3>
                <div className="card">
                    <ul className="list-group list-group-flush">
                        <li className="list-group-item"><b>Number of calls:</b> {calls.nb_call}</li>
                        <li className="list-group-item"><b>Number of calls missed:</b> {calls.nb_call_missed}</li>
                        <li className="list-group-item"><b>Total duration of calls:</b> {calls.total_duration_pretty}</li>
                        <li className="list-group-item"><b>Average duration of calls:</b> {calls.average_duration_pretty}</li>
                    </ul>
                </div>
                <br />
                {/* Messages per user */}
                <h3>Calls per user</h3>
                <table className="table table-hover">
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Participants</th>
                            <th>Number of messages</th>
                            <th>Rate (%)</th>
                        </tr>
                    </thead>
                    <tbody>
                        { calls.participants.length ?
                        calls.participants.map((participants, index) =>
                            <tr>
                                <th scope="row">{index + 1}</th>
                                <td>{participants.name}</td>
                                <td>{participants.nb_call}</td>
                                <td>{participants.rate}%</td>
                            </tr>
                        ) : null}
                    </tbody>
                </table>
            </div>
        )
    }

    render() {
        const conversations = this.state.conversations
        const conversation_title = this.state.conversation_title
        const page = this.state.page
        const search_query = this.state.search_query

        return (
            <div className="container-fluid">
                <div className="row">
                    <div className="col-3">
                        <div className="input-group mb-3">
                            <input onChange={this.queryConversations} value={search_query} type="text" className="form-control" placeholder="Search" aria-label="Filter the conversations" aria-describedby="button-addon1"/>
                        </div>
                        <ul className="list-group">
                            {
                                conversations.length ?
                                conversations.map(conversation => this.renderConversationList(conversation)) :
                                null
                            }
                        </ul>
                    </div>
                    <div className="col-6">
                        {conversation_title !== null &&
                            <div>
                                <h1>{conversation_title}</h1>
                                <ul className="nav nav-tabs justify-content-end">
                                    <li onClick={() => this.setTab("message")} className="nav-item ">
                                        <a className="nav-link" href="#">Messages</a>
                                    </li>
                                    <li onClick={() => this.setTab("call")} className="nav-item">
                                        <a className="nav-link" href="#">Calls</a>
                                    </li>
                                </ul>
                                <br />
                            </div>
                        }
                        {
                            page === "message" && this.renderMessages()
                        }
                        {
                            page === "call" && this.renderCalls()
                        }
                    </div>
                </div>
            </div>
        )
    }
}

export default ConversationsList
