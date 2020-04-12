import React, { Component } from 'react'
import {
    Hint, 
    RadialChart, 
    XYPlot,DiscreteColorLegend, 
    XAxis, YAxis, 
    VerticalGridLines, 
    HorizontalGridLines, 
    VerticalBarSeries,
    LineSeries,
    VerticalBarSeriesCanvas} from 'react-vis'
import '../../node_modules/react-vis/dist/style.css'
import API from '../api'
import formatNumbers from '../utils'

class ConversationsList extends Component {
    constructor(props) {
        super(props)
        this.state = {
            conversations: null,
            conversation_id: "",
            conversation_title: null,
            value: false,
            current_conversation: null,
            calls: null,
            page: "message",
            search_query: '',
            messages_per_hour: null,
            messages_per_month: null,
            messages_per_day: null,
            emojis: null,
            content: null,
            languages: null,
            events: null
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
            response.data.is_group_conversation = Boolean(response.data.is_group_conversation)
            this.setState({current_conversation: response.data})
            console.log(this.state.current_conversation)
        })
        .catch(error => {
            console.log(error)
        })
    }

    updateMessagesPerHour = (conversation_id) => {
        API.get("/conversation/" + conversation_id + '/messages?data=message_per_hour')
        .then(response => {
            this.setState({messages_per_hour: response.data.messages_per_hour})
        })
        .catch(error => {
            console.log(error)
        })
    }

    updateMessagesPerDay = (conversation_id) => {
        API.get("/conversation/" + conversation_id + '?data=message_per_day')
        .then(response => {
            this.setState({messages_per_day: response.data})
        })
        .catch(error => {
            console.log(error)
        })
    }

    updateEvents = (conversation_id) => {
        API.get("/conversation/" + conversation_id + '?data=events')
        .then(response => {
            // if (response.data.length)
            this.setState({events: response.data})
            // else
            //     this.setState({events: null})
            console.log(this.state.events)
        })
        .catch(error => {
            console.log(error)
        })
    }

    updateContent = (conversation_id) => {
        API.get("/conversation/" + conversation_id + '/messages?data=content')
        .then(response => {
            this.setState({content: response.data})
            console.log(this.state.content)
        })
        .catch(error => {
            console.log(error)
        })
    }

    updateEmojis = (conversation_id) => {
        API.get("/conversation/" + conversation_id + '/messages?data=emojis')
        .then(response => {
            this.setState({emojis: response.data})
            console.log(this.state.content)
        })
        .catch(error => {
            console.log(error)
        })
    }

    updateMessagesPerMonth = (conversation_id) => {
        API.get("/conversation/" + conversation_id + '/messages?data=message_per_month')
        .then(response => {
            var tmp = []
            for (var item in response.data.messages_per_month) {
                tmp.push({
                    "x": new Date(response.data.messages_per_month[item].x),
                    "y": response.data.messages_per_month[item].y
                })
            }
            this.setState({messages_per_month: tmp})
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
            messages_per_month: null,
            messages_per_day: null,
            current_conversation: null,
            languages: null,
            content: null,
            emojis: null,
            events: null
        })
        this.setState({page: "message"})
        this.updateConversationInfo(conversation_id)
        this.updateMessagesPerHour(conversation_id)
        this.updateMessagesPerMonth(conversation_id)
        this.updateMessagesPerDay(conversation_id)
        this.updateLanguages(conversation_id)
        this.updateEvents(conversation_id)
        this.updateContent(conversation_id)
        this.updateEmojis(conversation_id)
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
    renderConversationList = () => {
        const search_query = this.state.search_query
        const conversations = this.state.conversations
        var tmp_conversations = conversations

        if (conversations === null)
            return null
        if (search_query !== "")
            tmp_conversations = conversations.filter(conversation => conversation.title.toLowerCase().indexOf(search_query.toLocaleLowerCase()) !== -1)
        return (
            <div>
                <div className="input-group mb-3">
                    <input onChange={this.queryConversations} value={search_query} type="text" className="form-control" placeholder="Search" aria-label="Filter the conversations" aria-describedby="button-addon1"/>
                </div>
                <ul className="list-group">
                    {
                        tmp_conversations.length ? tmp_conversations.map(conversation =>
                            <li onClick={() => this.selectConversation(conversation.conversation_id, conversation.title)} className="list-group-item d-flex justify-content-between align-items-center list-group-item-action font-weight-light">
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
                        ) : <p className="font-weight-light">No result.</p>
                    }
                </ul>
            </div>
        )
    }

    renderMessages = () => {
        const current_conversation = this.state.current_conversation
        const messages_per_hour = this.state.messages_per_hour
        const messages_per_month = this.state.messages_per_month
        const messages_per_day = this.state.messages_per_day
        const conversation_title = this.state.conversation_title
        const languages = this.state.languages
        const content = this.state.content
        const emojis = this.state.emojis
        const {value} = this.state
        const events = this.state.events

        const useCanvas = false;
        const BarSeries = useCanvas ? VerticalBarSeriesCanvas : VerticalBarSeries;

        if (conversation_title === null)
            return null
        return (
            <div>
                {/* Info */}
                <h3 className="font-weight-light">Info</h3>
                {
                    current_conversation !== null ?
                    <div>
                        <div className="card">
                            <ul className="list-group list-group-flush">
                                <li className="list-group-item">
                                    <b>Number of messages:</b> {"     "}{formatNumbers(current_conversation.nb_messages)}
                                </li>
                                <li className="list-group-item">
                                    <b>First message:</b>{"     "}{current_conversation.first_message}
                                </li>
                                <li className="list-group-item">
                                    <b>Last message:</b>{"     "}{current_conversation.last_message}
                                </li>
                                <li className="list-group-item">
                                    <b>Still in conversation:</b>
                                    {
                                        current_conversation.is_still_participant === true ?
                                            <span className="badge badge-success">{"     "}{current_conversation.is_still_participant.toString()}</span>
                                        :
                                            <span className="badge badge-danger">{"     "}{current_conversation.is_still_participant.toString()}</span>
                                    }
                                </li>
                                <li className="list-group-item">
                                    <b>Group conversation:</b>
                                    {
                                        current_conversation.is_group_conversation === true ?
                                            <span className="badge badge-success">{"     "}{current_conversation.is_group_conversation.toString()}</span>
                                        :
                                            <span className="badge badge-danger">{"     "}{current_conversation.is_group_conversation.toString()}</span>
                                    }
                                </li>
                                <li className="list-group-item">
                                    <b>Messages per day:</b>{"   "}{current_conversation.message_per_day}
                                </li>
                            </ul>
                        </div>
                        <br />

                        {/* Messages per user */}
                        <h3 className="font-weight-light">Messages per user</h3>
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
                                width={910}
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
                    <div className="text-center">
                        <div className="spinner-border text-primary" role="status">
                            <span className="sr-only"></span>
                        </div>
                    </div>
                }
                {/* Messages Per Hour */}
                <h3 className="font-weight-light">Messages Per Hour</h3>
                { messages_per_hour !== null ?
                    <div>
                        <XYPlot margin={{bottom: 70, left: 60, top: 50}} xType="ordinal" width={910} height={400}>
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
                    <div className="text-center">
                        <div className="spinner-border text-primary" role="status">
                            <span className="sr-only"></span>
                        </div>
                    </div>
                }
                {/* Messages Per day */}
                <h3 className="font-weight-light">Messages Per Day</h3>
                { messages_per_day !== null ?
                    <div>
                        <XYPlot margin={{bottom: 70, left: 60, top: 50}} stackBy="y" xType="ordinal" width={910} height={400}>
                        <DiscreteColorLegend
                                style={{position: 'absolute', left: '60px', top: '0px'}}
                                orientation="horizontal"
                                items={messages_per_day}
                            />
                        <VerticalGridLines />
                        <HorizontalGridLines />
                        <XAxis />
                        <YAxis />
                        { 
                            messages_per_day.length ? messages_per_day.map(row =>
                                <BarSeries data={row.data} color={row.color}/>
                            ) : null
                        }
                        </XYPlot>
                    </div>:
                    <div className="text-center">
                        <div className="spinner-border text-primary" role="status">
                            <span className="sr-only"></span>
                        </div>
                    </div>
                }

                {/* Messages Per Month */}
                <h3 className="font-weight-light">Messages Per Month</h3>
                { messages_per_month !== null ?
                    <XYPlot xType="time" margin={{bottom: 70, left: 50}} width={910} height={400}>
                        <HorizontalGridLines />
                        <VerticalGridLines />
                        <XAxis title="Months" tickLabelAngle={-45}/>
                        <YAxis title="Messages" />
                        <LineSeries data={messages_per_month} color="#575fcf"/>
                    </XYPlot>
                    :
                    <div className="text-center">
                        <div className="spinner-border text-primary" role="status">
                            <span className="sr-only"></span>
                        </div>
                    </div>
                }
                {/* Languages */}
                <h3 className="font-weight-light">Languages</h3>
                <div className="alert alert-warning font-weight-light" role="alert">
                    Only messages with at least 30 characters and 5 words are processed.
                </div>
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
                    <div className="text-center">
                        <div className="spinner-border text-primary" role="status">
                            <span className="sr-only"></span>
                        </div>
                    </div>
                }
                {/* Content */}
                <h3 className="font-weight-light">Content</h3>
                {
                    content !== null ?
                    <table className="table table-hover">
                        <thead>
                            <tr>
                                <th>Type</th>
                                <th>Messages</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><span role="img" aria-label="Audios">🎤</span>{"   "}Audios</td>
                                <td>{formatNumbers(content.audios)}</td>
                            </tr>
                            <tr>
                                <td><span role="img" aria-label="Videos">🎥</span>{"   "}Videos</td>
                                <td>{formatNumbers(content.videos)}</td>
                            </tr>
                            <tr>
                                <td><span role="img" aria-label="Photos">📷</span>{"   "}Photos</td>
                                <td>{formatNumbers(content.photos)}</td>
                            </tr>
                            <tr>
                                <td><span role="img" aria-label="Stickers">🙂</span>{"   "}Stickers</td>
                                <td>{formatNumbers(content.stickers)}</td>
                            </tr>
                            <tr>
                                <td><span role="img" aria-label="Shares">🌐</span>{"   "}Shares</td>
                                <td>{formatNumbers(content.shares)}</td>
                            </tr>
                            <tr>
                                <td><span role="img" aria-label="Gifs">🐱</span>{"   "}Gifs</td>
                                <td>{formatNumbers(content.gifs)}</td>
                            </tr>
                        </tbody>
                    </table>
                    :
                    <div className="text-center">
                        <div className="spinner-border text-primary" role="status">
                            <span className="sr-only"></span>
                        </div>
                    </div>
                }
                {/* Emojis */}
                <h3 className="font-weight-light">Emojis</h3>
                {
                    emojis !== null ?
                    <table className="table table-hover">
                        <thead>
                            <tr>
                                <th>Sender</th>
                                <th>Top 10 most used emojis</th>
                            </tr>
                        </thead>
                        <tbody>
                            {
                                emojis.length ? emojis.map(sender  =>
                                    <tr>
                                        <th scope="row">{sender.sender}</th>
                                        <td>
                                            {
                                                sender.emoji ? sender.emoji.map(data  =>
                                                    <span>
                                                        <span className="badge badge-light">{data.emoji}: {data.nb_messages}</span>
                                                        {"        "}
                                                    </span>
                                                )
                                                :
                                                null
                                            }
                                        </td>
                                    </tr>
                                )
                                :
                                null
                            }
                        </tbody>
                    </table>
                    :
                    <div className="text-center">
                        <div className="spinner-border text-primary" role="status">
                            <span className="sr-only"></span>
                        </div>
                    </div>
                }
                {/* Events */}
                <h3 className="font-weight-light">Events</h3>
                {
                    current_conversation !== null && current_conversation.is_group_conversation == false ?
                    <div className="alert alert-danger font-weight-light" role="alert">
                        <p className="font-weight-light">Only group conversations have events.</p>
                    </div>
                    :
                    <div>
                        {
                            events !== null ?
                                <div className="card">
                                    <div className="card-body">
                                        {
                                            events.length ? events.map(event  =>
                                                <p className="font-weight-light">
                                                    <span className="badge badge-pill badge-light">{event.sent_at}</span>
                                                    {"   "}
                                                    {
                                                        event.change === "+1" ?
                                                            <span className="badge badge-pill badge-success">{event.change}</span>
                                                        :
                                                            <span className="badge badge-pill badge-danger">{event.change}</span>
                                                    }
                                                    {"   "}
                                                    {event.content}
                                                </p>
                                            )
                                            :
                                            <p className="font-weight-light"> No events in this conversation.</p>
                                        }
                                    </div>
                                </div>
                            :
                                <div className="text-center">
                                    <div className="spinner-border text-primary" role="status">
                                        <span className="sr-only"></span>
                                    </div>
                                </div>
                        }
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
                <h3 className="font-weight-light">Info</h3>
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
                <h3 className="font-weight-light">Calls per user</h3>
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
        const conversation_title = this.state.conversation_title
        const page = this.state.page
        const conversations = this.state.conversations

        return (
            <div>
                {conversations === null &&
                <div>
                        <div className="text-center">
                            <br />
                            <br />
                            <br />
                            <div className="spinner-border text-primary" role="status">
                                <span className="sr-only"></span>
                            </div>
                            <p className="font-weight-light">Loading conversations</p>
                        </div>
                    </div>
                }
                <div className="container-fluid">
                    <div className="row">
                        <div className="col-3">
                            {this.renderConversationList()}
                        </div>
                        <div className="col-6">
                            {conversation_title !== null &&
                                <div>
                                    <h1 className="font-weight-normal">{conversation_title}</h1>
                                    <ul className="nav nav-tabs justify-content-end">
                                        <li onClick={() => this.setTab("message")} className="nav-item ">
                                            <a className="nav-link font-weight-light">Messages</a>
                                        </li>
                                        <li onClick={() => this.setTab("call")} className="nav-item">
                                            <a className="nav-link font-weight-light">Calls</a>
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
            </div>
        )
    }
}

export default ConversationsList
