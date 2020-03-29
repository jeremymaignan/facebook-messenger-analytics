import React, { Component } from 'react';
import {Hint, RadialChart, XYPlot,DiscreteColorLegend, XAxis, YAxis, VerticalGridLines, HorizontalGridLines, VerticalBarSeries} from 'react-vis';
import '../../node_modules/react-vis/dist/style.css';
import API from '../api';

class ConversationsList extends Component {
    constructor(props) {
        super(props);
        this.state = {
            conversations: [],
            conversation_id: "",
            conversation_title: null,
            value: false,
            current_conversation: null,
            calls: null,
            page: "message"
        }
    }

    componentDidMount() {
        API.get("/conversation")
        .then(response => {
            this.setState({conversations: response.data});
        })
        .catch(error => {
            console.log(error);
        })
    }

    update_conversation = (conversation_id) => {
        API.get("/conversation/" + conversation_id)
        .then(response => {
            response.data.is_still_participant = Boolean(response.data.is_still_participant)
            this.setState({current_conversation: response.data});
            console.log(this.state.current_conversation)
        })
        .catch(error => {
            console.log(error);
        })
    }

    update_call = (conversation_id) => {
        API.get("/conversation/" + conversation_id + '/call')
        .then(response => {
            this.setState({calls: response.data});
            console.log(this.state.calls)
        })
        .catch(error => {
            console.log(error);
        })
    } 

    handleClick = (conversation_id, conversation_title) => {
        this.setState({
            conversation_id: conversation_id,
            conversation_title: conversation_title
        });
        this.setState({page: "message"})
        this.update_conversation(conversation_id);
        this.update_call(conversation_id);
    }

    set_page = (page) => {
        this.setState({page: page})
    }

    show_labels = (v) => {
        if (v === false)
            this.setState({value: false});
        else
            delete v['angle0'];
            delete v['angle'];
            delete v['radius'];
            delete v['radius0'];
            delete v['y'];
            delete v['x'];
            delete v['color'];
            this.setState({value: v});
    }

    render() {
        const conversations = this.state.conversations;
        const current_conversation = this.state.current_conversation
        const conversation_title = this.state.conversation_title
        const calls = this.state.calls
        const page = this.state.page
        const pages = this.state.pages
        const {value} = this.state;
        return (
            <div class="container-fluid">
                <div className="row">
                    <div className="col-3">
                        <ul className="list-group">
                            {
                                conversations.length ?
                                conversations.map(conversation =>
                                <li onClick={() => this.handleClick(conversation.conversation_id, conversation.title)} className="list-group-item d-flex justify-content-between align-items-center list-group-item-action">
                                    {conversation.title}
                                    {conversation.is_still_participant === 1 &&
                                        <span className="badge badge-primary badge-pill">
                                        {conversation.nb_messages}
                                        </span>
                                    }
                                    {conversation.is_still_participant === 0 &&
                                        <span className="badge badge-danger badge-pill">
                                        {conversation.nb_messages}
                                        </span>
                                    }
                                </li>):
                            null
                            }
                        </ul>
                    </div>
                    <div className="col-6">
                        {conversation_title !== null &&
                            <div>
                                <h1>{conversation_title}</h1>
                                <ul class="nav nav-tabs justify-content-end">
                                    <li onClick={() => this.set_page("message")} class="nav-item ">
                                        <a class="nav-link {pages.message}" href="#">Messages</a>
                                    </li>
                                    <li onClick={() => this.set_page("call")} class="nav-item">
                                        <a class="nav-link {pages.call}" href="#">Calls</a>
                                    </li>
                                </ul>
                                <br />
                            </div>
                        }
                        {page === "message" &&  current_conversation !== null &&
                            <div>

                                {/* Info */}
                                <h3>Info</h3>
                                <div className="card">
                                    <ul class="list-group list-group-flush">
                                        <li class="list-group-item"><b>Number of messages:</b> {current_conversation.nb_messages}</li>
                                        <li class="list-group-item"><b>First message:</b> {current_conversation.first_message}</li>
                                        <li class="list-group-item"><b>Last message:</b> {current_conversation.last_message}</li>
                                        <li class="list-group-item"><b>Still in conversation:</b> {current_conversation.is_still_participant.toString()}</li>
                                        <li class="list-group-item"><b>Messages per day:</b> {current_conversation.message_per_day}</li>
                                    </ul>
                                </div>
                                <br />

                                {/* Messages per user */}
                                <h3>Messages per user:</h3>
                                <table class="table table-hover">
                                    <thead>
                                        <tr>
                                            <th>#</th>
                                            <th>Participants</th>
                                            <th>Number of calls</th>
                                            <th>Rate (%)</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        { current_conversation.nb_messages_per_user.length ?
                                        current_conversation.nb_messages_per_user.map((user, index) =>
                                            <tr>
                                                <th scope="row">{index + 1}</th>
                                                <td>{user.user}</td>
                                                <td>{user.nb_message}</td>
                                                <td>{user.rate}%</td>
                                            </tr>
                                        ) : null}
                                    </tbody>
                                </table>
                                <div>
                                    <RadialChart
                                        className={'donut-chart-example'}
                                        innerRadius={200}
                                        colorType={'literal'}
                                        radius={250}
                                        getAngle={d => d.nb_message}
                                        getLabel={d => d.label}
                                        data={current_conversation.nb_messages_per_user}
                                        onValueMouseOver={v => this.show_labels(v)}
                                        onSeriesMouseOut={v => this.show_labels(false)}
                                        width={900}
                                        height={600}
                                        padAngle={0.04}
                                        showLabels
                                        labelsStyle={{fontSize: 16, fill: '#22'}}
                                    >
                                    {value !== false && <Hint value={value} />}
                                    </RadialChart>
                                </div>

                                {/* Messages over the time */}
                                <h3>Messages over the time</h3>
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
                                    data={current_conversation.messages_per_hour}
                                    color="#575fcf"
                                />
                                </XYPlot>
                            </div>
                        }
                        {page === "call" && calls !== null &&
                            <div>
                                {/* Calls */}
                                <h3>Info:</h3>
                                <div className="card">
                                    <ul class="list-group list-group-flush">
                                        <li class="list-group-item"><b>Number of calls:</b> {calls.nb_call}</li>
                                        <li class="list-group-item"><b>Number of calls missed:</b> {calls.nb_call_missed}</li>
                                        <li class="list-group-item"><b>Total duration of calls:</b> {calls.total_duration_pretty}</li>
                                        <li class="list-group-item"><b>Average duration of calls:</b> {calls.average_duration_pretty}</li>
                                    </ul>
                                </div>
                                <br />
                                {/* Messages per user */}
                                <h3>Calls per user:</h3>
                                <table class="table table-hover">
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
                        }
                    </div>
                </div>
            </div>
        );
    }
}

export default ConversationsList;
