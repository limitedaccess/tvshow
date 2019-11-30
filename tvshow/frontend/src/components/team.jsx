
import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';

class TeamDetails extends Component {
    constructor(props) {
        super(props);
    }
    render() {
        if(!this.props.team) {
            return null;
        }
        this.items = this.props.team.candidates.map((item, key) =>
            <li className="list-group-item" key={item.pk}>{item.first_name} {item.last_name}</li>
        );
        return (
            <div key={this.props.team.pk}>
                <b>{this.props.team.mentor_name}: {this.props.team.team_name}</b> <br/>
                <span>Team Average: {this.props.team.team_average}</span> <br/>
                Candidates: <br/>
                <ul className="list-group">
                    {this.items}
                </ul>
          </div>
        )
    }
}

const mapStateToProps = (state) => {
    return {
      team: state.selectedTeam
    }
  }
export default connect(mapStateToProps)(TeamDetails);