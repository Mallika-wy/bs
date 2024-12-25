import axios from "@/axios"


export function login(name, password) {
    return axios.post("/login", {
        name,
        password
    })
}


export function modifyUser(id, modifiedUser) {
    return axios.post("/modifyUser", {
        id,
        modifiedUser
    })
}


export function addTb(user_id) {
    return axios.post("/addTb", {
        user_id
    })
}


export function searchItems(id, searchText) {
    return axios.get("/search", {
        params: {
            id: id,
            searchText: searchText
        }
    })
}

export function searchItem(user_id, item_id) {
    return axios.get("/searchItem", {
        params: {
            user_id: user_id,
            item_id: item_id
        }
    })
}

export function subscribeItem(user_id, item_id) {
    return axios.post("/subscribe", {
        user_id,
        item_id
    })
}

export function addJd(user_id) {
    return axios.post("/addJd", {
        user_id
    })
}

export function getQrcode() {
    return axios.get("/getQrcode", {
        params: {
        }
    })
}

export function getDoc() {
    return axios.get("/getDoc", {
        params: {
        }
    })
}

export function register(user_info_dict) {
    return axios.post("/register", {
        user_info_dict
    })
}


export function history(user_id) {
    return axios.get("/history", {
        params: {
            user_id: user_id
        }
    })
}

export function getUserFromToken(token) {
    return axios.get("/getUserFromToken", {
        params: {
            token: token
        }
    })
}

export function getItemsFromSearchID(user_id, search_id) {
    return axios.get("/getItemsFromSearchID", {
        params: {
            user_id: user_id,
            search_id: search_id
        }
    })
}

export function getItem(item_id) {
    return axios.get("/getItemFromItemID", {
        params: {
            item_id: item_id
        }
    })
}

export function getSubscribe(user_id) {
    return axios.get("/getSubscribe", {
        params: {
            user_id: user_id
        }
    })
}


export function deleteSubscribe(user_id, subscribe_id) {
    return axios.post("/deleteSubscribe", {
        user_id,
        subscribe_id
    })
}


export function checkSubscribe(user_id, subscribe_id) {
    return axios.post("/checkSubscribe", {
        user_id,
        subscribe_id
    })
}


export function checkSubscribes(user_id) {
    return axios.post("/checkSubscribes", {
        user_id
    })
}
