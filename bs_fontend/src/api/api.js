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


export function addTb(user_id, info_tb) {
    return axios.post("/addTb", {
        user_id,
        info_tb
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