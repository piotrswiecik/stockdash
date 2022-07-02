export default {
    setStockData(state, payload) {
        console.log('received payload: ' + payload);
        state.name = payload['name'];
        state.description = payload['description'];
    }
}