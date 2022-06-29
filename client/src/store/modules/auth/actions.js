export default {
    loginRequest(context, payload) {
        // handle login request
        // communicate with backend to check credentials
        // if ok - change state via mutations (store token, user id) + return status
        // if failed - return status
        console.log('login request received by vuex');
        console.log('payload received: ' + payload['username'] + payload['password']);

        // REST API query goes here:
        const restResponse = true // placeholder
        if (!restResponse) { // response validation goes here
            throw Error('Authentication failed!')
        }

        // if no auth error, commit token to vuex
        context.commit('setAuthenticatedStatus', {
            username: payload['username'],
            authToken: 'token', // main token received from backend
            refreshToken: 'reftoken', // refresh token received from backend
            userId: 0, // placeholder for now
            isAdmin: false, // placeholder for now
        });
        return null;
    },
};