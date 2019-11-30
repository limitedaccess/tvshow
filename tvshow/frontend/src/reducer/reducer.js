const initialState = {
    user: null,
    errors: {},
    candidates: null,
    teams: null,
    selectedCandidate: null,
    selectedTeam: null,
  };
  
  export default function Reducer(state = initialState, action) {
    switch (action.type) {
    case 'LOGIN_SUCCESSFUL':
      return {
          ...state,
          user: action.data,
      }
  
    case 'LOGIN_ERROR':
      return Object.assign({}, state, {
        errors: action.data,
        user: null,
      });
    case 'CANDIDATES_SUCCESSFUL':
        return {
            ...state,
            candidates: action.data,
        }
    case 'TEAMS_SUCCESSFUL':
        return {
            ...state,
            teams: action.data,
        }
    case 'SELECT_CANDIDATE':
        return {
            ...state,
            selectedCandidate: action.data,
        }
    case 'SELECT_TEAM':
        return {
            ...state,
            selectedTeam: action.data,
        }
    default:
      return state;
    }
  }