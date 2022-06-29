export default {
    async loginRequest(context, payload) {
        // handle login request
        // communicate with backend to check credentials
        // if ok - change state via mutations (store token, user id) + return status
        // if failed - return status

        // REST API query goes here:
        // todo fetch url should be handled from env vars
        const url = 'http://localhost:5000/login'
        const restResponse = await fetch(url, {
            method: 'POST',
            mode: 'cors',
            body: JSON.stringify({
                username: payload['username'],
                password: payload['password'],
            }),
            headers: {
                'Content-Type': 'application/json',
            }
        });

        if (!restResponse.ok) { // generic validation
            throw new Error('Authentication failed!');
        }

        // if no auth error, commit token to vuex
        await context.commit('setAuthenticatedStatus', {
            username: payload['username'],
            authToken: 'token', // main token received from backend
            refreshToken: 'reftoken', // refresh token received from backend
            userId: 0, // placeholder for now
            isAdmin: false, // placeholder for now
        });
        return null; // a placeholder - response is not used at the moment
    },
};