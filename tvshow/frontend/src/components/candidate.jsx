
import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';

class CandidateDetails extends Component {
    constructor(props) {
        super(props);
    }
    render() {
        if(!this.props.candidate) {
            return null;
        }
        this.items = this.props.candidate.performances.map((item, key) =>
            <li className="list-group-item" key={item.pk}>{item.name} at {item.date} Average Score:{item.average_score}</li>
        );
        return (
            <div key={this.props.candidate.pk}>
                <b>{this.props.candidate.first_name} {this.props.candidate.last_name}</b> <br/>
                <span>Personal Average: {this.props.candidate.personal_average}</span> <br/>
                <span>Team Average: {this.props.candidate.team_average}</span> <br/>
                Performances: <br/>
                <ul className="list-group">
                    {this.items}
                </ul>
          </div>
        )
    }
}

const mapStateToProps = (state) => {
    return {
      candidate: state.selectedCandidate
    }
  }
export default connect(mapStateToProps)(CandidateDetails);