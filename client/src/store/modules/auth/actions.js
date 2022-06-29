export default {
    loginRequest(context, payload) {
        // handle login request
        // communicate with backend to check credentials
        // if ok - change state via mutations (store token, user id) + return status
        // if failed - return status
        console.log('login request received by vuex');
        console.log('payload received: ' + payload['username'] + payload['password']);
        return null;
    },
};