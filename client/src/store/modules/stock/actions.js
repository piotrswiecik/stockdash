export default {
    async getApiData(context) {
        // called from main dashboard component
        // queries REST API for stock data and handles it depending on response type

        // todo fetch url should be handled from env vars
        const stock = context.state.ticker;
        const url = 'http://localhost:5000/stock/' + stock;
        const restResponse = await fetch(url, {
            method: 'GET',
            mode: 'cors',
        });

        if (!restResponse.ok) {
            // todo handle err
        }

        const restResponseData = await restResponse.json()
        // todo verify if data needs additional safety checking
        await context.commit('setStockData', restResponseData)

    }
}