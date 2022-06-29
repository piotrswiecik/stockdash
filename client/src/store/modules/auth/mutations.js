export default {
    setAuthenticatedStatus(state, payload) {
        // sets user status to authenticated if auth was successful
        // store token & settings in vuex
        state.userIsAuthenticated = true;
        state.authToken = payload['authToken'];
        state.refreshToken = payload['refreshToken'];
        state.userId = payload['userId'];
        state.username = payload['username'];
        state.isAdmin = false; // todo admin status is hardcoded for now
    },
    setNotAuthenticatedStatus(state) {
        // sets user status to anonymous on logout
        // clear token & settings from vuex
        // todo: send token invalidation request to REST API
        console.log('setting user status to non-auth');
        state.userIsAuthenticated = false;
        state.authToken = null;
        state.refreshToken = null;
        state.userID = null;
        state.username = null;
        state.isAdmin = false;
        console.log('current state: ');
        console.log('state.userIsAuthenticated: ' + state.userIsAuthenticated);
        console.log('state.authToken: ' + state.authToken);
        console.log('state.refreshToken: ' + state.refreshToken);
        console.log('state.userId: '+ state.userId);
        console.log('state.usename: ' + state.username);
    }
};