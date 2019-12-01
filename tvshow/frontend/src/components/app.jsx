import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';
import { login } from '../actions/auth';
import { getCandidates, getTeams, selectCandidate, selectTeam } from '../actions/data';
import CandidateDetails from './candidate.jsx';
import TeamDetails from './team.jsx';

class App extends Component {
  static propTypes = {
    login: PropTypes.func.isRequired,
  }

  constructor(props) {
    super(props);
    this.state = {
      username: '',
      password: '',
      showCandidateModalBox: false,
      showTeamModalBox: false,
    };
    this.showCandidateModal = this.showCandidateModal.bind(this);
    this.hideCandidateModal = this.hideCandidateModal.bind(this);
    this.showTeamModal = this.showTeamModal.bind(this);
    this.hideTeamModal = this.hideTeamModal.bind(this);
  }
  componentDidUpdate(prevProps) {
    if (this.props.user && this.props.user.user_type == 2 && !this.props.candidates ) {
        this.props.getCandidates(this.props.user.token);
    }
    if (this.props.user && this.props.user.user_type == 1 && !this.props.teams ) {
      this.props.getTeams(this.props.user.token);
    }
   }

  onSubmit = (e) => {
    e.preventDefault();
    const { username, password } = this.state;
    const { login } = this.props;
    login(username, password);
  }

  loginForm() {
    if (this.props.user) {
      return null;
    }
    const content = (
      <form onSubmit={this.onSubmit}>
        <div className="col-md-offset-5 col-md-3">
          <h4> Login</h4>
          <div className="input-group mb-3">
            <input
              type="text"
              className="form-control input-sm chat-input"
              placeholder="username"
              onChange={e => this.setState({ username: e.target.value })}
            />
            <input
              type="password"
              className="form-control input-sm chat-input"
              placeholder="password"
              onChange={e => this.setState({ password: e.target.value })}
            />
          </div>
          <button type="submit" className="btn btn-primary btn-md">
            Login
          </button>
        </div>
      </form>
    );
    return content;
  }

  candidateList() {
    if (!this.props.candidates) {
      return null;
    }
    this.items = this.props.candidates.map((item, key) =>
      <li className="list-group-item" key={item.pk}
        onClick={() => this.showCandidateModal(item)}
      >{item.team}: {item.first_name} {item.last_name}</li>
    );
    return (
      <div>
        <h2>Candidate List</h2>
        <ul className="list-group">
          {this.items}
        </ul>
      </div>
    )

  }

  teamList() {
    if (!this.props.teams) {
      return null;
    }
    this.items = this.props.teams.map((item, key) =>
      <li className="list-group-item" key={item.pk}
        onClick={() => this.showTeamModal(item)}
      >{item.team_name} Mentor: {item.mentor_name} Average Score:{item.team_average}</li>
    );
    return (
      <div>
        <h2>Team List</h2>
        <ul className="list-group">
          {this.items}
        </ul>
      </div>
    )

  }
  showCandidateModal(candidate) {
    this.props.selectCandidate(candidate);
    this.setState(
        {
          showCandidateModalBox: true
        }
    )
  }

  hideCandidateModal() {
    this.setState(
      {
        selectCandidate: null,
        showCandidateModalBox: false
      }
    )
} 

showTeamModal(team) {
  this.props.selectTeam(team);
  this.setState(
      {
        showTeamModalBox: true
      }
  )
}

hideTeamModal() {
  this.setState(
    {
      showTeamModalBox: false
    }
  )
} 

  candidateDetailModal() {
    const modalBox = (
      <Modal show={this.state.showCandidateModalBox} onHide={this.hideCandidateModal}>
      <Modal.Header closeButton>
        <Modal.Title>Candidate Details</Modal.Title>
      </Modal.Header>
      <Modal.Body>
          <CandidateDetails />
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={this.hideCandidateModal}>
          Close
        </Button>
      </Modal.Footer>
    </Modal>
    );
    return modalBox;
  }

  teamDetailModal() {
    const modalBox = (
      <Modal show={this.state.showTeamModalBox} onHide={this.hideTeamModal}>
      <Modal.Header closeButton>
        <Modal.Title>Team Details</Modal.Title>
      </Modal.Header>
      <Modal.Body>
          <TeamDetails />
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={this.hideTeamModal}>
          Close
        </Button>
      </Modal.Footer>
    </Modal>
    );
    return modalBox;
  } 
  render() {
    return (
      <div>
        {this.loginForm()}
        {this.candidateList()}
        {this.teamList()}
        {this.candidateDetailModal()}
        {this.teamDetailModal()}
      </div>
    );
  }
}

const mapDispatchToProps = (dispatch) => {
  return {
    login(username, password) {
      return dispatch(login(username, password));
    },
    getCandidates(token) {
      return dispatch(getCandidates(token));
    },
    getTeams(token) {
      return dispatch(getTeams(token));
    },
    selectTeam(team) {
      return dispatch(selectTeam(team));
    },
    selectCandidate(candidate) {
      return dispatch(selectCandidate(candidate));
    },
  };
};

const mapStateToProps = (state) => {
  return {
    user: state.user,
    candidates: state.candidates,
    teams: state.teams,
  }
}
export default connect(mapStateToProps, mapDispatchToProps)(App);