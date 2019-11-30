export function getCandidates(token) {
    return (dispatch, state) => {
        return fetch(`/api/candidates/`, {
            credentials: 'include',
            headers: {
                Accept: 'application/json',
                Authorization: `Token ${token}`
            }
        })
        .then((response) => {
            return response.json().then((data) => {
              return {
                status: response.status,
                data,
              };
            },
            );
          })
          .then((response) => {
            if (response.status !== 200) {
              dispatch({ type: 'CANDIDATES_ERROR', data: response.status });
            }
            if (response.status === 200) {
              dispatch({ type: 'CANDIDATES_SUCCESSFUL', data: response.data });
            }
          });
      };
}

export function getTeams(token) {
    return (dispatch, state) => {
        return fetch(`/api/teams/`, {
            credentials: 'include',
            headers: {
                Accept: 'application/json',
                Authorization: `Token ${token}`
            }
        })
        .then((response) => {
            return response.json().then((data) => {
              return {
                status: response.status,
                data,
              };
            },
            );
          })
          .then((response) => {
            if (response.status !== 200) {
              dispatch({ type: 'TEAMS_ERROR', data: response.status });
            }
            if (response.status === 200) {
              dispatch({ type: 'TEAMS_SUCCESSFUL', data: response.data });
            }
          });
      };
}

export function selectCandidate(candidate) {
    return (dispatch, state) => {
        dispatch({ type: 'SELECT_CANDIDATE', data: candidate });
    };
}

export function selectTeam(team) {
    return (dispatch, state) => {
        dispatch({ type: 'SELECT_TEAM', data: team });
    };
}