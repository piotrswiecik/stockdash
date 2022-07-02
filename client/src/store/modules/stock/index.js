/*
Stock dashboard module for vuex.
Stores & updates stock data.

Vuex store contains all stock data. Might reconsider this later - maybe 'static' price data can be stored in normal
array inside dashboard component - to be verified.

When dashboard is loaded (beforeMount) or refreshed (beforeUpdate), the getApiData() action is called from relevant
component - fetch() via /stock/<name> REST endpoint.
Content is handled depending on response type.
'cache-fresh' response -> data from cache, up-to-date - commit mutation and display with 'CACHE' flag.
'api-fresh' response -> data from AlphaVantage, up-to-date - commit mutation and display with 'API' flag.
'cache-stale' response -> data from cache, cannot be refreshed due to some error - commit mutation, display with 'OUT OF SYNC'
flag - and maybe handle this error via popups etc.

 */
import getters from "@/store/modules/stock/getters";
import mutations from "@/store/modules/stock/mutations";
import actions from "@/store/modules/stock/actions";

export default {
    state() {
        return {
            ticker: 'XOM',
            name: '',
            exchange: 'NYSE',
            description: 'blank',
            sector: '',
            industry: '',
            market_cap: '',
            no_shares: '',
            trail_pe_ratio: '',
            fwd_pe_ratio: '',
            d_yield: '',
            high_52w: '',
            low_52w: '',
            eps: '',
            last_cache_time: '',
            cache_response: '',
            timeseries: '',
        }
    },
    namespaced: true,
    getters: getters,
    mutations: mutations,
    actions: actions,
}