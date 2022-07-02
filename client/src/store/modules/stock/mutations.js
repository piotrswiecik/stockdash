export default {
    setStockData(state, payload) {
        console.log('received payload: ' + payload);
        state.name = payload['name'];
        state.description = payload['description'];
        state.exchange = payload['exchange'];
        state.sector = payload['sector'];
        state.industry = payload['industry'];
    }
}